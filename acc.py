import streamlit as st
import mysql.connector
import bcrypt

def get_db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        db = "law_thinker"
    )

def signup(username , email , password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "⚠️ Username already exists"

    cursor.execute("Select id from users where email=%s", (email,))
    if cursor.fetchone():
        conn.close()
        return False, "⚠️ Email already exists"
    
    # Hash password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, hashed.decode("utf-8"))
    )
    conn.commit()
    conn.close()
    return True, "✅ Account created successfully!"

def login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "User not found"

    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return True, user  
    else:
        return False, "Incorrect password"

def run_account():
    st.title("Welcome to Law Thinker")
    
    if "user" not in st.session_state:
        st.session_state.user = None
    if "show_update" not in st.session_state:
        st.session_state.show_update = False

    # ✅ Logged-in view
    if st.session_state.user:        
        col1, col2 ,col3 = st.columns([8 , 1 ,1])

        with col1:
            st.header("👤 Account")

        with col2:
            if st.button("Update Profile"):
                st.session_state.show_update = not st.session_state.show_update

        with col3:
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()

        st.success(f"Logged in as {st.session_state.user['username']}")

        if st.session_state.show_update:
            st.subheader("✏️ Update your account")

            with st.form("update_form"):
                new_username = st.text_input("New Username", st.session_state.user["username"])
                new_password = st.text_input("New Password", type="password")
                submitted = st.form_submit_button("Save Changes")

            if submitted:
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "UPDATE users SET username=%s WHERE id=%s",
                    (new_username,  st.session_state.user["id"])
                )

                if new_password:
                    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    cursor.execute(
                        "UPDATE users SET password_hash=%s WHERE id=%s",
                        (hashed.decode("utf-8"), st.session_state.user["id"])
                    )

                conn.commit()
                conn.close()

                st.session_state.user["username"] = new_username
                st.success("✅ Profile updated successfully!")
                st.rerun()

    else:
        st.header("👤 Account")
        choice = st.radio("Choose action:", ["Login", "Signup"])

        if choice == "Login":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")

            if submitted:
                ok, result = login(email, password)
                if ok:
                    st.session_state.user = result
                    st.success(f"🎉 Welcome back, {result['username']}!")
                    st.rerun()
                else:
                    st.error(result)

        elif choice == "Signup":
            with st.form("signup_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Signup")

            if submitted:
                if not username or not email or not password:
                    st.error("⚠️ Please fill in all fields.")
                else:
                    ok, result = signup(username, email, password)
                    if ok:
                        st.success(result)
                    else:
                        st.error(result)

