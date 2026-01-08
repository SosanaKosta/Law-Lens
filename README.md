# Law Lens

An AI-powered legal assistant chatbot specialized in Albanian laws. Ask questions about Albanian legal documents and get instant answers in Albanian or English.

## Features

- 🤖 **AI-Powered Chatbot**: Uses LangChain and RAG (Retrieval-Augmented Generation) to answer questions about Albanian laws
- 📜 **Document Processing**: Automatically extracts and indexes articles ("Neni") from PDF legal documents
- 🌐 **Bilingual Support**: Answer questions in Albanian (Shqip) or English
- 💬 **Chat History**: Save and search your previous questions and answers (requires login)
- 🔍 **Direct Article Lookup**: Quickly retrieve specific articles by number (e.g., "Neni 5")
- 📚 **Constitutional Documents**: Pre-loaded with Albanian constitutional documents

## Tech Stack

- **Streamlit**: Web application framework
- **LangChain**: LLM application framework
- **FAISS**: Vector database for semantic search
- **Hugging Face Embeddings**: Multilingual sentence transformers
- **Ollama**: Local LLM (Llama3) for inference
- **MySQL**: Database for user accounts and chat history
- **pdfplumber/PyPDF2**: PDF parsing

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/Law-Lens.git
cd Law-Lens
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
   - Run the SQL commands from `mysqlTables.txt` to create the necessary tables

4. Configure environment variables:
   - Create a `.env` file with your database credentials and API keys (if using OpenAI)

5. Add your PDF documents:
   - Place Albanian law PDFs in the `pdf/` folder

6. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Start the application and select your preferred language (Albanian/English)
2. The system will automatically process PDFs from the `pdf/` folder
3. Ask questions about Albanian laws in the chat interface
4. You can query specific articles by mentioning "Neni X" in your question
5. Log in to save and search your chat history

## Project Structure

```
Law-Lens/
├── app.py              # Main Streamlit application
├── pyMAIN.py           # Core chatbot logic and document processing
├── acc.py              # User authentication module
├── chats.py            # Chat history management
├── htmlTemplates.py    # HTML templates for chat UI
├── requirements.txt    # Python dependencies
├── mysqlTables.txt     # Database schema
├── pdf/                # PDF documents folder
└── README.md           # This file
```

## Notes

- The application uses local embeddings and Ollama for processing, making it fully offline-capable
- Currently optimized for Albanian constitutional documents ("Kushtetuta")
- The system extracts articles based on "Neni" patterns in the PDFs

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

