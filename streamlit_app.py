import sqlite3
import streamlit as st

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Save new user to the database
def save_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists
    conn.close()
    return True

# Verify login credentials
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

# Embed Power BI report
def embed_powerbi():
    powerbi_url = 'https://app.powerbi.com/view?r=YOUR_REPORT_URL'  # Replace with your Power BI URL
    st.markdown(
        f"""
        <iframe 
            width="100%" 
            height="650px" 
            src="{powerbi_url}" 
            frameborder="0" 
            allowFullScreen="true">
        </iframe>
        """, 
        unsafe_allow_html=True
    )

# Add Custom CSS for vibrant design
def add_custom_styling():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f7f7f7;
            padding: 20px;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
        }
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 20px;
        }
        .btn-primary {
            background-color: #008CBA;
            border: none;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Login Page
def show_login():
    st.subheader("Log In")
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("Username")
            username = st.text_input("", key="login_username")
        with col2:
            st.write("Password")
            password = st.text_input("", type="password", key="login_password")
    if st.button("Log In"):
        if verify_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()  # Rerun safely
        else:
            st.error("Invalid credentials!")

# Sign-Up Page
def show_signup():
    st.subheader("Sign Up")
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("Username")
            username = st.text_input("", key="signup_username")
        with col2:
            st.write("Password")
            password = st.text_input("", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif save_user(username, password):
            st.success("Account created successfully!")
        else:
            st.error("Username already exists.")

# Main App
def main():
    st.set_page_config(page_title="AQI Dashboard", layout="centered")
    st.markdown("<h1>AQI Dashboard</h1>", unsafe_allow_html=True)
    add_custom_styling()

    init_db()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.sidebar.title("Navigation")
        menu = st.sidebar.radio("Menu", ["Log In", "Sign Up"])
        if menu == "Log In":
            show_login()
        elif menu == "Sign Up":
            show_signup()
    else:
        st.write("Welcome to the AQI Dashboard!")
        embed_powerbi()

if __name__ == "__main__":
    main()

