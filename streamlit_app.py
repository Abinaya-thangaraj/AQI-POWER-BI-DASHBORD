# Custom CSS for adjusting position of login and sign-up
def add_custom_styling():
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Arial', sans-serif;
            color: white;
        }
        .stApp {
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            padding: 20px;
        }
        h1 {
            color: #FFD700; /* Gold Color */
            font-size: 4rem;
            text-align: center;
            text-shadow: 2px 2px 5px #000000; /* Shadow for visibility */
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 0px;
        }
        .subtitle {
            text-align: center;
            color: #FFFFFF; /* White color for username */
            font-style: italic;
            font-size: 1.5rem;
            font-weight: bold;
            text-shadow: 1px 1px 3px #000000; /* Black shadow for clarity */
            margin-top: -10px;
        }
        .content-box {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        .stButton>button {
            background: linear-gradient(90deg, #32CD32, #6A5ACD);
            border: none;
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #6A5ACD, #32CD32);
            transform: scale(1.05);
        }

        .login-form, .signup-form {
            margin-top: -30px; /* Adjusted margin to make the forms appear higher */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Login Page
def show_login():
    st.subheader("🔓 Welcome Back! Log In", anchor="login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log In"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"🎉 Welcome, {username}!")
            st.rerun()
        else:
            st.error("Incorrect username or password. Please try again.")

# Sign-Up Page
def show_signup():
    st.subheader("🌟 Create Your Account", anchor="signup")
    username = st.text_input("Enter a Username")
    password = st.text_input("Create a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif save_user(username, password):
            st.success("🎉 Account created! Log in to explore the dashboard.")
        else:
            st.error("Username already exists. Try a different one.")
