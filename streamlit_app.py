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
        return False  # Username already exists
    finally:
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
    powerbi_url = 'https://app.powerbi.com/view?r=eyJrIjoiNzQ1NjFkNzgtMDk4Mi00MjlkLWFlM2QtYmNkM2NlMWU2ODBjIiwidCI6ImQxYWY5MTdkLWI3OGEtNGU1Zi1hOGU3LTE3ZjcwMGU4NDJjZSJ9'
    st.markdown(
        f"""
        <div style="
            background-color: #ffffff; 
            border: 10px solid #006400; 
            border-radius: 20px; 
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2); 
            padding: 20px;
            margin: 40px auto;
            width: 95%;
        ">
            <iframe 
                width="100%" 
                height="650px" 
                src="{powerbi_url}" 
                frameborder="0" 
                allowFullScreen="true" 
                style="border-radius: 15px;">
            </iframe>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Add Custom CSS for vibrant design
def add_custom_styling():
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://images.unsplash.com/photo-1536760384165-d20f5d1faa0b?crop=entropy&cs=tinysrgb&w=1080&fit=max');
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }
        .stApp {
            background-color: white; /* Change gray to white */
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        h1 {
            color: #FFD700;
            font-size: 3rem;
            text-align: center;
            margin-bottom: -10px;
        }
        .subtitle {
            text-align: right;
            color: #ffffff;
            font-size: 1rem;
            margin-top: -20px;
        }
        .center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
        }
        .btn-primary {
            background: linear-gradient(90deg, #6A5ACD, #32CD32);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.2rem;
            margin: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            background: linear-gradient(90deg, #32CD32, #6A5ACD);
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sign-Up Page
def show_signup():
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.subheader("🌟 Create Your Account")
    username = st.text_input("Enter a Username")
    password = st.text_input("Create a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up", key="signup_button"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif save_user(username, password):
            st.success("🎉 Account created! Log in to explore the dashboard.")
        else:
            st.error("Username already exists. Try a different one!")
    st.markdown('</div>', unsafe_allow_html=True)

# Login Page
def show_login():
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.subheader("🔓 Welcome Back! Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log In", key="login_button"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"🎉 Welcome, {username}! Redirecting...")
            st.rerun()
        else:
            st.error("Incorrect username or password. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)

# Logout Option
def show_logout():
    if st.button("Log Out", key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

# Introduction Section
def show_introduction():
    st.markdown("""
    ## 🌍 Introduction
    The AQI Dashboard helps you understand air quality patterns across regions. With this interactive tool, you can analyze air quality trends and uncover actionable insights to make informed decisions for a healthier environment.
    """)

# Conclusion Section
def show_conclusion():
    st.markdown("""
    ---
    ## 🎉 Conclusion
    This dashboard offers an engaging way to understand air quality trends. Stay informed and contribute to a cleaner, healthier planet!

    **Thank you for visiting the AQI Dashboard! 🌿**

    ---
    """)

# Main App
def main():
    st.markdown("<h1>AQI DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Presented by Abinaya</p>', unsafe_allow_html=True)
    add_custom_styling()

    init_db()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.sidebar.title("Welcome")
        menu = st.sidebar.selectbox("Navigation", ["Log In", "Sign Up"])
        if menu == "Log In":
            show_login()
        elif menu == "Sign Up":
            show_signup()
    else:
        show_introduction()
        embed_powerbi()
        show_conclusion()
        show_logout()

if __name__ == "__main__":
    main()
