import streamlit as st
from streamlit_option_menu import option_menu
import pyMAIN , acc , chats

st.set_page_config(page_title="Law Thinker", layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title="📑 Law Thinker",
        options=["Home", "Account" , "Chats" , "Search previous chat answers"],
        icons=["house-fill", "person-circle"],
        menu_icon="chat-text-fill",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "black"},
            "icon": {"color": "white", "font-size": "23px"}, 
            "nav-link": {
                "color": "white", 
                "font-size": "20px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "blue"
            },
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

if selected == "Home":
    pyMAIN.run_home()
   
elif selected == "Account":
    acc.run_account()

elif selected == "Chats":
    if "user" not in st.session_state or not st.session_state.user:
        st.warning("⚠️ Please log in to see your chats.")
    else:
        user_id = st.session_state.user["id"]
        chats_list = chats.load_user_chats(user_id)

        st.header("💬 Your Chats")
        if chats_list:
            for chat in chats_list:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"**Q:** {chat['question']}")
                st.markdown(f"**A:** {chat['answer']}")
            st.markdown("<hr>", unsafe_allow_html=True)
        else:
            st.info("No chats found yet.")

elif selected == "Search previous chat answers":  
    if "user" not in st.session_state:
        st.session_state.user = None       
    chats.run_chats()
    chats.sidebar_previous_questions()
