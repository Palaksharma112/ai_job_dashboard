import streamlit as st
from auth import login_page, register_page
from dashboard import dashboard_page
from database import create_table

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IT Job Market Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# DATABASE
# =====================================================

create_table()

# =====================================================
# LOAD CSS
# =====================================================

try:
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "home"

if "username" not in st.session_state:
    st.session_state.username = ""

# =====================================================
# HOME PAGE
# =====================================================

if st.session_state.page == "home":

    # ---------------- NAVBAR ----------------

    nav1, nav2 = st.columns([6, 2])

    with nav1:

        st.markdown(
            f"""
            <h2 style='color:white;font-weight:700;'>
                IT Job Market Dashboard
            </h2>
            """,
            unsafe_allow_html=True
        )

    with nav2:

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "Login",
                use_container_width=True
            ):
                st.session_state.page = "login"
                st.rerun()

        with c2:

            if st.button(
                "Register",
                use_container_width=True
            ):
                st.session_state.page = "register"
                st.rerun()

    st.divider()

    # ---------------- HERO SECTION ----------------

    left, right = st.columns([1.3, 1])

    with left:

        st.markdown(
            """
            <h1 style='font-size:48px;color:white;'>
            Find Your Dream AI Career
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown("")

        st.markdown(
            """
Explore thousands of **AI**, **Machine Learning**, **Data Science**, and
**Data Analytics** jobs using an interactive dashboard.

### Why use this dashboard?

✅ AI Job Analytics

✅ Salary Insights

✅ Top Hiring Companies

✅ Skill Demand Analysis

✅ Remote Job Analysis

✅ Employment Type Analytics

✅ Interactive Charts

✅ Excel-based Dashboard
            """
        )

        st.markdown("")

        btn1, btn2 = st.columns(2)

        with btn1:

            if st.button(
                "🚀 Get Started",
                use_container_width=True
            ):
                st.session_state.page = "login"
                st.rerun()

        with btn2:

           if st.button(
    "📖 Learn More",
    use_container_width=True
):
              st.markdown("""
## IT Job Market Dashboard

### Project Description

This dashboard provides real-time AI, Machine Learning, Data Science, and Python job listings using the JSearch API.

### Features

- Live AI Jobs
- Search Jobs
- Company Filters
- Location Filters
- Remote Jobs
- Salary Analysis
- Top Hiring Companies
- Skills Analysis
- Interactive Charts
- Download Jobs as CSV
- Secure Login System

### Technologies

- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- RapidAPI (JSearch)

### Data Source

Live job data is fetched directly from the JSearch API through RapidAPI.

""")

    with right:

        st.image(
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200",
            use_container_width=True
        )

    st.markdown("")
    st.divider()

        # =====================================================
    # FEATURE SECTION
    # =====================================================

    st.markdown("## 🚀 Dashboard Features")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.info(
            """
### IT Job Analytics

✔ Interactive Dashboard

✔ KPI Cards

✔ Search Jobs

✔ Smart Filters
"""
        )

    with f2:
        st.success(
            """
### 💰 Salary Insights

✔ Average Salary

✔ Highest Paying Companies

✔ Salary Distribution

✔ Salary Trends
"""
        )

    with f3:
        st.warning(
            """
### 💻 Skills Analysis

✔ Most Demanded Skills

✔ Top Technologies

✔ Remote Jobs

✔ Employment Types
"""
        )

    st.divider()

    # =====================================================
    # PROJECT HIGHLIGHTS
    # =====================================================

    st.markdown("## 🌟 Why Choose This Dashboard?")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
### 🎯 Key Features

- AI Job Market Analysis
- Excel Dataset Integration
- SQLite User Authentication
- Interactive Visualizations
- Search & Filters
- Responsive UI
- User Profile
- Company Insights
""")

    with c2:

        st.markdown("""
### 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- SQLite
- OpenPyXL
- Plotly
- CSS
- Excel Dataset
""")

    st.divider()

    # =====================================================
    # QUICK STATS
    # =====================================================

    st.markdown("## 📈 Dashboard Overview")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "AI Jobs",
            "15,000+"
        )

    with s2:
        st.metric(
            "Companies",
            "500+"
        )

    with s3:
        st.metric(
            "Skills",
            "150+"
        )

    with s4:
        st.metric(
            "Locations",
            "75+"
        )

    st.divider()

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        """
<div style="text-align:center;padding:20px;color:gray;">

Made with ❤️ using

<b>Python • Streamlit • SQLite • Excel</b>

<br><br>

AI Job Market Dashboard

MCA Major Project

</div>
""",
        unsafe_allow_html=True
    )

    # =====================================================
# LOGIN PAGE
# =====================================================

elif st.session_state.page == "login":

    login_page()


# =====================================================
# REGISTER PAGE
# =====================================================

elif st.session_state.page == "register":

    register_page()


# =====================================================
# DASHBOARD
# =====================================================

elif st.session_state.page == "dashboard":

    if st.session_state.logged_in:

        dashboard_page()

    else:

        st.session_state.page = "login"
        st.rerun()


# =====================================================
# INVALID PAGE
# =====================================================

else:

    st.session_state.page = "home"
    st.rerun()