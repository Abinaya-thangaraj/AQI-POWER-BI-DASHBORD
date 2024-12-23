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
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzQ1NjFkNzgtMDk4Mi00MjlkLWFlM2QtYmNkM2NlMWU2ODBjIiwidCI6ImQxYWY5MTdkLWI3OGEtNGU1Zi1hOGU3LTE3ZjcwMGU4NDJjZSJ9"
    st.markdown(
        f"""
        <iframe 
            title="INFOSYS" 
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
        </style>
        """,
        unsafe_allow_html=True,
    )

# Introduction Section
def show_introduction():
    st.markdown("""
    ## 🌍 Introduction
    The AQI Dashboard helps you understand air quality patterns across various regions. 
    With this interactive tool, you can analyze trends, gain actionable insights, 
    and make informed decisions for a healthier environment.
    """)

# Conclusion Section
def show_conclusion():
    st.markdown("""
    ---
    ## 🎉 Conclusion
    This dashboard offers a comprehensive way to analyze air quality trends. 
    Stay informed and contribute to a cleaner, healthier planet!

    **Thank you for using the AQI Dashboard! 🌿**
    """)

# Login Page
def show_login():
    st.subheader("Log In")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Log In"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials!")

# Sign-Up Page
def show_signup():
    st.subheader("Sign Up")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")
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

    if st.session_state.logged_in:
        st.write(f"Welcome to the AQI Dashboard, {st.session_state.username}!")
        show_introduction()
        embed_powerbi()
        show_conclusion()
        if st.button("Log Out"):
            st.session_state.logged_in = False
    else:
        st.sidebar.title("Navigation")
        menu = st.sidebar.radio("Menu", ["Log In", "Sign Up"])
        if menu == "Log In":
            show_login()
        elif menu == "Sign Up":
            show_signup()

if __name__ == "__main__":
    main()
