import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
# PDF parsing
try:
    import pdfplumber
    USE_PDFPLUMBER = True
except ImportError:
    from PyPDF2 import PdfReader
    USE_PDFPLUMBER = False

# LangChain
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from htmlTemplates import css, bot_template, user_template
from chats import save_user_chat

DATA_PATH = "pdf"

def load_pdfs_from_folder(folder_path):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    return pdf_files

def get_pdf_text(pdf_docs):
    texts = []
    if USE_PDFPLUMBER:
        for pdf in pdf_docs:
            with pdfplumber.open(pdf) as p:
                page_texts = [page.extract_text() or "" for page in p.pages]
            texts.append("\n".join(page_texts))
    else:
        for pdf in pdf_docs:
            reader = PdfReader(pdf)
            page_texts = [page.extract_text() or "" for page in reader.pages]
            texts.append("\n".join(page_texts))
    text = "\n\n".join(texts)
    return normalize_text(text)
    
def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00A0", " ")   # NBSP
    text = text.replace("\u00ad", "")    # soft hyphen
    text = text.replace("–", "-").replace("—", "-")

    # 🔑 Ensure "Neni X" always starts on a new line
    text = re.sub(r'\s*(Neni\s+\d+)', r'\n\1', text)

    return text

HEADING_REGEX = re.compile(
    r'^\s*(Neni)\s+(\d+(?:/\d+)?)(?:\s*[:\-]\s*[^\n]*)?\s*$',
    flags=re.IGNORECASE | re.MULTILINE
)

def extract_articles(raw_text: str, source_name="document"):
    text = normalize_text(raw_text)
    matches = list(HEADING_REGEX.finditer(text))

    if not matches:
        return [Document(page_content=text, metadata={"source": source_name})], {}

    docs = []
    index_by_article = {}

    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading_line = m.group(0).strip()
        article_num = m.group(2).strip()
        body = text[start:end].strip()
        full_text = f"{heading_line}\n{body}".strip()

        doc = Document(
            page_content=full_text,
            metadata={"article": article_num, "heading": heading_line, "source": source_name}
        )
        docs.append(doc)
        index_by_article[article_num] = doc

    return docs, index_by_article

def get_vectorstore(documents):
    #uncomment to use Ollama
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )
    return FAISS.from_documents(documents=documents, embedding=embeddings)

    #embeddings = OpenAIEmbeddings()
    #vectorstore = FAISS.from_documents(documents , embeddings)
    #return vectorstore

AL_PROMPT = PromptTemplate(
    template=(
        "Je një asistent juridik që përgjigjet vetëm në gjuhën shqipe.\n"
        "Përdor vetëm informacionin nga dokumentet e mëposhtme. "
        "Nëse nuk gjen përgjigje, thuaj qartë se nuk gjendet.\n\n"
        "Historiku i bisedës:\n{chat_history}\n\n"
        "Përmbajtja e dokumenteve:\n{context}\n\n"
        "Pyetja: {question}\n\n"
        "Përgjigju qartë në shqip dhe përmend numrin e nenit nëse është e aplikueshme."
        "E RËNDËSISHME: Duhet të përgjigjeni gjithmonë VETËM në shqip, edhe nëse përdoruesi pyet në anglisht."
    ),
    input_variables=["chat_history", "context", "question"]
)

EN_PROMPT = PromptTemplate(
    template=(
        "You are a legal assistant that answers only in English.\n"
        "Use only the information from the provided documents. "
        "If the answer is not found, clearly say so.\n\n"
        "Conversation history:\n{chat_history}\n\n"
        "Document content:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer clearly in English and mention the article number if applicable."
        "IMPORTANT: You must always answer ONLY in English, even if the user asks in Albanian."
    ),
    input_variables=["chat_history", "context", "question"]
)


def get_conversation_chain(vectorstore, lang_choice="Shqip"):
    llm = Ollama(model="llama3")
    #llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",
        output_key="answer",
        return_messages=True
    )

    prompt = AL_PROMPT if lang_choice == "Shqip" else EN_PROMPT

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        output_key="answer"
    )
    return chain

def try_direct_article_answer(user_q, by_article):
    m = re.search(r'\bNeni\s+(\d+(?:/\d+)?)\b', user_q, flags=re.IGNORECASE)
    if not m:
        return None
    num = m.group(1)
    doc = by_article.get(num)
    if doc:
        return f"**{doc.metadata['heading']} (teksti i plotë):**\n\n{doc.page_content}"
    return f"Nuk gjeta tekst për Nenin {num}."

def handle_userinput(user_question):
    if not st.session_state.conversation:
        st.warning("Përpunoni dokumentet fillimisht.")
        return

    direct = try_direct_article_answer(user_question, st.session_state.index_by_article)
    if direct is not None:
        st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", direct), unsafe_allow_html=True)

        if "user" in st.session_state and st.session_state.user:
                save_user_chat(st.session_state.user["id"], user_question, direct)
        return

    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            user_msg = message.content
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            bot_msg = message.content
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    
    if user_msg and bot_msg and "user" in st.session_state and st.session_state.user:
        save_user_chat(st.session_state.user["id"], user_msg, bot_msg)

    if "source_documents" in response:
        with st.expander("Burimet e përdorura"):
            for d in response["source_documents"]:
                meta = d.metadata or {}
                st.markdown(f"- **Neni**: {meta.get('article', '—')} | **Burimi**: {meta.get('source', '—')}")
                st.code(d.page_content[:600])


def run_home():
    load_dotenv()
    st.set_page_config(page_title="🤖  Chat with Law Thinker 📜")
    st.write(css, unsafe_allow_html=True)

    # Session state initialization
    if "uploaded_docs" not in st.session_state:
        st.session_state.uploaded_docs = None
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "index_by_article" not in st.session_state:
        st.session_state.index_by_article = {}
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None


    col1, col2 = st.columns([6, 2])
    with col2:
        lang_choice = st.radio(
            "Language / Gjuha:",
            ["Shqip", "English"],
            index=0 ,
            horizontal=True
        )


    st.header("🤖  Chat with Law Thinker 📜")
    question_label = "Bëj një pyetje për një nen:" if lang_choice == "Shqip" else "Ask a question about a law:(Remember,its called Neni in AL :)"
    user_question = st.text_input(question_label)
    if user_question:
        handle_userinput(user_question)
                        

    if st.session_state.vectorstore is None:
        pdf_docs = load_pdfs_from_folder(DATA_PATH)
        if pdf_docs:
            with st.spinner(f"Duke përpunuar PDF-të nga folderi '{DATA_PATH}'... \n"
                            f"\n Proccesing the files from folder '{DATA_PATH}'"):
                raw_text = get_pdf_text(pdf_docs)
                docs, index_by_article = extract_articles(raw_text, source_name="PDF Folder")
                vectorstore = get_vectorstore(docs)

                st.session_state.vectorstore = vectorstore
                st.session_state.index_by_article = index_by_article

                with st.expander("Artikujt e gjetur"):
                    st.write(", ".join(sorted(
                        index_by_article.keys(),
                        key=lambda x: [int(p) for p in x.split('/') if p.isdigit()]
                    )))
        else:
            st.error(f"Asnjë PDF nuk u gjet në folderin '{DATA_PATH}'.")

    # Create/update conversation chain when language changes
    if st.session_state.vectorstore:
        st.session_state.conversation = get_conversation_chain(
            st.session_state.vectorstore,
            lang_choice
        )




