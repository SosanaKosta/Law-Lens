import streamlit as st
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        db="law_thinker"
    )

def save_user_chat(user_id, question, answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_chats (user_id, question, answer) VALUES (%s, %s, %s)",
        (user_id, question, answer)
    )
    conn.commit()
    conn.close()

def load_user_chats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT question, answer, created_at FROM user_chats WHERE user_id=%s ORDER BY created_at ASC",
        (user_id,)
    )
    chats = cursor.fetchall()
    conn.close()
    return chats
"""
def run_chats():
    st.header("💬 Law Thinker Chat")

    # Display previous chats if logged in
    if st.session_state.user:
        previous_chats = load_user_chats(st.session_state.user['id'])
        for chat in previous_chats:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.write(chat['question'], unsafe_allow_html=True)
            st.write(pyMAIN.bot_template.replace("{{MSG}}", chat['answer']), unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.info("Log in to see your chats.")
"""
def search_previous_question():
    if "user" not in st.session_state or not st.session_state.user:
        st.warning("⚠️ Please log in to search previous questions.")
        return

    user_id = st.session_state.user.get("id")
    search_term = st.text_input("🔎 Search your previous questions:")

    if st.button("Search"):
        if not search_term.strip():
            st.error("⚠️ Please type something to search.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT question, answer 
                FROM user_chats 
                WHERE user_id=%s AND question LIKE %s
                ORDER BY created_at DESC
                LIMIT 5
            """
            cursor.execute(query, (user_id, f"%{search_term}%"))
            results = cursor.fetchall()
            conn.close()

            if results:
                st.success(f"Found {len(results)} matching question(s):")
                for row in results:
                    st.markdown(f"**Q:** {row['question']}")
                    st.markdown(f"**A:** {row['answer']}")
                    st.markdown("---")
            else:
                st.error("❌ No matching questions found.")

        except Error as e:
            st.error(f"Database error: {str(e)}")

def sidebar_previous_questions():
    if "user" not in st.session_state or not st.session_state.user:
        st.sidebar.info("Log in to see previous questions.")
        return

    st.sidebar.subheader("📜 Previous Questions")
    user_id = st.session_state.user.get('id')
    questions = load_user_chats(user_id)

    if questions:
        with st.sidebar.expander("Show Previous Questions", expanded=False):
            for chat in questions:
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown("---")  
    else:
        st.sidebar.write("No previous questions yet.")

def run_chats():
    st.header("💬 Law Thinker Chat")

    if st.session_state.user:
        search_previous_question()

    else:
        st.info("Log in to save and search your chats.")
