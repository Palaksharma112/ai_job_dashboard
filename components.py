import streamlit as st


# ============================================
# PAGE HEADER
# ============================================

def page_header(title, subtitle=""):

    html = f"""
    <div class="page-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """

    st.html(html)


# ============================================
# KPI CARD
# ============================================

def kpi_card(icon, title, value):

   st.html(
    f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                {icon}
            </div>

            <div class="kpi-title">
                {title}
            </div>

            <div class="kpi-value">
                {value}
            </div>

        </div>
    """
    )
   
   # ============================================
# COMPANY CARD
# ============================================

def company_card(company, jobs, salary, city, skill):

    st.html(f"""
    <div class="company-card">

        <h3>🏢 {company}</h3>

        <p>💼 Open Jobs : <b>{jobs}</b></p>

        <p>💰 Avg Salary : <b>₹ {salary:,}</b></p>

        <p>📍 Top City : <b>{city}</b></p>

        <p>⭐ Top Skill : <b>{skill}</b></p>

    </div>
    """)


# ============================================
# PROFILE CARD
# ============================================

def profile_card(username):

    st.html(f"""
    <div class="profile-card">

        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
             width="90">

        <h3>{username}</h3>

        <p>MCA Student</p>

    </div>
    """)


# ============================================
# EMPTY STATE
# ============================================

def empty_state(message):
    st.info(message)


# ============================================
# SECTION TITLE
# ============================================

def section(title):
    st.markdown(f"## {title}")


# ============================================
# JOB CARD
# ============================================

def job_card(row):

    salary = row.get("Salary", "N/A")
    title = row.get("Job Title", "N/A")
    company = row.get("Company", "N/A")
    location = row.get("Location", "N/A")
    employment = row.get("Employment Type", "N/A")
    remote = row.get("Remote", "No")
    skills = row.get("Skills", "")
    apply_link = row.get("Apply Link", "")

    st.html(f"""
    <div class="job-card">

        <div class="job-top">

            <div>
                <h3>{title}</h3>
                <h4>{company}</h4>
            </div>

            <div class="salary-badge">
                ₹ {salary}
            </div>

        </div>

        <hr>

        <p>📍 <b>Location:</b> {location}</p>

        <p>💼 <b>Employment:</b> {employment}</p>

        <p>🌍 <b>Remote:</b> {remote}</p>

        <p>🛠 <b>Skills:</b></p>

        <div class="skill-box">
            {skills}
        </div>

    </div>
    """)

    # Apply Button
    if apply_link:
        st.link_button(
            "🚀 Apply Now",
            apply_link,
            use_container_width=True
        )
    else:
        st.button(
            "🚀 Apply Now",
            disabled=True,
            use_container_width=True
        )

    st.markdown("---")