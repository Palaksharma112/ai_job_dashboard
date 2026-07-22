import streamlit as st
from database import (
    get_user,
    update_profile,
    change_password
)


# ==========================================================
# PROFILE PAGE
# ==========================================================

def profile_page():

    st.title("👤 My Profile")
    st.caption("Manage your account settings")

    # ---------------- Get User ---------------- #

    user = get_user(st.session_state.username)

    if user is None:
        st.error("User not found.")
        return

    fullname, email, username = user

    # ======================================================
    # PROFILE HEADER
    # ======================================================

    left, right = st.columns([1, 3])

    with left:

        st.html(
            f"""
            <div style="
                background:#1E293B;
                padding:25px;
                border-radius:18px;
                text-align:center;
                border:1px solid #334155;
            ">
                <img
                    src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                    width="120">

                <h3 style="color:white;">
                    User
                </h3>
            </div>
            """
        )

    with right:

        st.html(
            f"""
            <div style="
                background:#1E293B;
                padding:25px;
                border-radius:18px;
                border:1px solid #334155;
            ">

            <h2 style="color:white;">
            {fullname}
            </h2>

            <p style="color:#CBD5E1;">
            📧 {email}
            </p>

            <p style="color:#CBD5E1;">
            👤 @{username}
            </p>

            <p style="color:#10B981;">
            ● Active Account
            </p>

            </div>
            """
        )

    st.markdown("")

    # ======================================================
    # ACCOUNT STATISTICS
    # ======================================================

    st.subheader("📊 Account Statistics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Profile Status",
            "Active"
        )

    with c2:
        st.metric(
            "Role",
            "Student"
        )

    with c3:
        st.metric(
            "Database",
            "SQLite"
        )

    st.divider()

    # ======================================================
    # PROFILE TABS
    # ======================================================

    tab1, tab2 = st.tabs(
        [
            "✏ Update Profile",
            "🔒 Change Password"
        ]
    )

    

        # ======================================================
    # UPDATE PROFILE
    # ======================================================

    with tab1:

        st.subheader("✏ Update Profile")

        new_name = st.text_input(
            "Full Name",
            value=fullname
        )

        new_email = st.text_input(
            "Email",
            value=email
        )

        st.text_input(
            "Username",
            value=username,
            disabled=True
        )

        if st.button(
            "💾 Update Profile",
            use_container_width=True
        ):

            if new_name.strip() == "":
                st.error("Full Name cannot be empty.")

            elif new_email.strip() == "":
                st.error("Email cannot be empty.")

            elif "@" not in new_email:
                st.error("Enter a valid email.")

            else:

                update_profile(
                    new_name,
                    new_email,
                    username
                )

                st.success("Profile Updated Successfully.")

                st.rerun()

    # ======================================================
    # CHANGE PASSWORD
    # ======================================================

    with tab2:

        st.subheader("🔒 Change Password")

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
            "🔑 Change Password",
            use_container_width=True
        ):

            if len(new_password) < 6:

                st.error("Password must be at least 6 characters.")

            elif new_password != confirm_password:

                st.error("Passwords do not match.")

            else:

                change_password(
                    username,
                    new_password
                )

                st.success("Password Changed Successfully.")

                st.rerun()

        st.info(
            """
✔ Use uppercase letters

✔ Use lowercase letters

✔ Include numbers

✔ Include special characters
"""
        )

    st.divider()

    st.subheader("📊 Account Information")

    c1, c2, c3 = st.columns(3)

    c1.metric("Username", username)
    c2.metric("Email", email)
    c3.metric("Status", "Active")

    st.markdown(
        """
<div class="footer">
AI Job Market Dashboard<br>
Profile Management<br>
Python • Streamlit • SQLite
</div>
""",
        unsafe_allow_html=True
    )