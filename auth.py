import streamlit as st
from database import register_user, login_user


# ==========================================
# LOGIN PAGE
# ==========================================

def login_page():

    st.markdown("<h1 style='text-align:center;'>🔐 Login</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Welcome back! Sign in to continue.</p>", unsafe_allow_html=True)

    with st.container(border=True):

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        remember = st.checkbox("Remember Me")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Login",
                use_container_width=True,
                type="primary"
            ):

                if username == "" or password == "":
                    st.warning("Please fill all fields.")

                else:

                    success = login_user(
                        username,
                        password
                    )

                    if success:

                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.page = "dashboard"

                        st.success("Login Successful")

                        st.rerun()

                    else:

                        st.error("Invalid Username or Password")

        with col2:

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                st.session_state.page = "register"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back to Home"):

        st.session_state.page = "home"
        st.rerun()


# ==========================================
# REGISTER PAGE
# ==========================================

def register_page():

    st.markdown("<h1 style='text-align:center;'>📝 Create Account</h1>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center;'>Register to access the AI Job Dashboard</p>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        fullname = st.text_input(
            "Full Name"
        )

        email = st.text_input(
            "Email"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        agree = st.checkbox(
            "I agree to the Terms & Conditions"
        )

        if st.button(
            "Create Account",
            use_container_width=True,
            type="primary"
        ):

            if fullname == "" or email == "" or username == "" or password == "":
                st.warning("Please fill all fields.")

            elif password != confirm:
                st.error("Passwords do not match.")

            elif not agree:
                st.warning("Accept Terms & Conditions.")

            else:

                success = register_user(
                    fullname,
                    email,
                    username,
                    password
                )

                if success:

                    st.success("Registration Successful!")

                    st.balloons()

                    st.session_state.page = "login"

                    st.rerun()

                else:

                    st.error("Username already exists.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Already have an account? Login"
    ):

        st.session_state.page = "login"

        st.rerun()