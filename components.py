import streamlit as st


# =====================================================
# PAGE HEADER
# =====================================================

def page_header(title, subtitle=""):

    st.html(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """
    )


# =====================================================
# KPI CARD
# =====================================================

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


# =====================================================
# PROFILE CARD
# =====================================================

def profile_card(username):

    st.html(
        f"""
        <div class="profile-card">

            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                 width="90">

            <h3>{username}</h3>

            <p>IT Job Portal User</p>

        </div>
        """
    )


# =====================================================
# JOB CARD
# =====================================================

def job_card(row):

    title = row.get("Job Title", "N/A")
    company = row.get("Company", "N/A")
    location = row.get("Location", "N/A")
    employment = row.get("Employment Type", "N/A")
    remote = row.get("Remote", "No")
    experience = row.get("Experience", "N/A")
    skills = row.get("Skills", "")
    salary = row.get("Salary", 0)
    apply_link = row.get("Apply Link", "")

    try:
        salary = f"₹ {float(salary):,.2f} LPA"
    except:
        salary = "Not Disclosed"

    st.html(
        f"""
        <div class="job-card">

            <div class="job-top">

                <div>

                    <h3>{title}</h3>

                    <h4>{company}</h4>

                </div>

                <div class="salary-badge">

                    {salary}

                </div>

            </div>

            <hr>

            <p>📍 <b>Location :</b> {location}</p>

            <p>💼 <b>Employment :</b> {employment}</p>

            <p>🧑‍💻 <b>Experience :</b> {experience}</p>

            <p>🌍 <b>Remote :</b> {remote}</p>

            <p><b>Skills :</b></p>

            <div class="skill-box">

                {skills}

            </div>

        </div>
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        with st.expander("👁 View Details"):

            st.write("### Job Information")

            st.write(f"**Job Title :** {title}")
            st.write(f"**Company :** {company}")
            st.write(f"**Location :** {location}")
            st.write(f"**Employment :** {employment}")
            st.write(f"**Experience :** {experience}")
            st.write(f"**Remote :** {remote}")
            st.write(f"**Salary :** {salary}")
            st.write(f"**Skills :** {skills}")

    with col2:

        if apply_link and str(apply_link).startswith("http"):

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


# =====================================================
# COMPANY CARD
# =====================================================

def company_card(
    company,
    jobs,
    salary,
    city,
    skill
):

    st.html(
        f"""
        <div class="company-card">

            <h3>🏢 {company}</h3>

            <p>💼 Open Jobs : <b>{jobs}</b></p>

            <p>💰 Avg Salary : <b>₹ {salary:,.2f} LPA</b></p>

            <p>📍 Cities : <b>{city}</b></p>

            <p>⭐ Top Skill : <b>{skill}</b></p>

        </div>
        """
    )


# =====================================================
# SECTION TITLE
# =====================================================

def section(title):

    st.tml(f"## {title}")


# =====================================================
# EMPTY STATE
# =====================================================

def empty_state(message):

    st.info(message)