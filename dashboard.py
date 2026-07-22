import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

from api import get_jobs
from utils import (
    filter_jobs,
    get_kpis,
    company_summary,
    top_skills,
    convert_csv
)

from components import (
    page_header,
    profile_card,
    kpi_card,
    job_card,
    company_card
)

from jobs import jobs_page
from companies import companies_page
from analytics import analytics_page
from profile import profile_page


# ======================================================
# SIDEBAR
# ======================================================

def sidebar(df):

    with st.sidebar:

        profile_card(
            st.session_state.get("username", "User")
        )

        st.markdown("---")

        selected = option_menu(
            menu_title="Navigation",

            options=[
                "Dashboard",
                "Jobs",
                "Companies",
                "Analytics",
                "Profile"
            ],

            icons=[
                "speedometer2",
                "briefcase-fill",
                "building",
                "bar-chart-fill",
                "person-circle"
            ],

            default_index=0,

            styles={
                "container": {
                    "background-color": "#111827",
                    "padding": "5px"
                },

                "icon": {
                    "color": "#3B82F6",
                    "font-size": "18px"
                },

                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "4px",
                    "border-radius": "10px",
                    "--hover-color": "#1E293B"
                },

                "nav-link-selected": {
                    "background-color": "#2563EB",
                    "font-weight": "bold"
                }
            }
        )

        st.markdown("---")
        st.subheader("🔍 Filters")

        company = st.selectbox(
            "Company",
            ["All"] + sorted(df["Company"].dropna().unique().tolist())
            if "Company" in df.columns else ["All"]
        )

        location = st.selectbox(
            "Location",
            ["All"] + sorted(df["Location"].dropna().unique().tolist())
            if "Location" in df.columns else ["All"]
        )

        employment = st.selectbox(
            "Employment Type",
            ["All"] + sorted(df["Employment Type"].dropna().unique().tolist())
            if "Employment Type" in df.columns else ["All"]
        )

        remote = st.selectbox(
            "Remote",
            ["All", "Yes", "No"]
        )

        st.markdown("---")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    return (
        selected,
        company,
        location,
        employment,
        remote
    )


# ======================================================
# HEADER
# ======================================================

def dashboard_header():

    col1, col2 = st.columns([6,1])

    with col1:

        page_header(
            "🤖 AI Job Market Dashboard",
            "Live AI Jobs using JSearch API"
        )

    with col2:

        st.write("")
        st.write("")

        if st.button(
            "🚪 Logout",
            use_container_width=True,
            key="header_logout"
        ):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    search = st.text_input(
        "",
        placeholder="Search AI, Data Scientist, Python Developer...",
        label_visibility="collapsed"
    )

    return search

# ======================================================
# MAIN DASHBOARD
# ======================================================

def dashboard_page():

    # -------------------------------
    # LOAD LIVE DATA
    # -------------------------------

    with st.spinner("Loading latest AI jobs..."):

        df = get_jobs("Data Scientist")

    if df.empty:
        st.warning("No jobs found.")
        return

    # -------------------------------
    # SIDEBAR
    # -------------------------------

    (
        selected,
        company,
        location,
        employment,
        remote
    ) = sidebar(df)

    # -------------------------------
    # PAGE NAVIGATION
    # -------------------------------

    if selected == "Jobs":
        jobs_page(df)
        return

    if selected == "Companies":
        companies_page(df)
        return

    if selected == "Analytics":
        analytics_page(df)
        return

    if selected == "Profile":
        profile_page()
        return

    # -------------------------------
    # HEADER
    # -------------------------------

    search = dashboard_header()

    # -------------------------------
    # FILTER DATA
    # -------------------------------

    filtered_df = filter_jobs(
        df=df,
        company=company,
        location=location,
        employment=employment,
        remote=remote,
        search=search
    )

    if filtered_df.empty:
        st.warning("No jobs found for selected filters.")
        return

    # -------------------------------
    # KPI
    # -------------------------------

    (
        total_jobs,
        total_companies,
        avg_salary,
        remote_jobs
    ) = get_kpis(filtered_df)

    st.markdown("## 📊 Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "💼",
            "Jobs",
            total_jobs
        )

    with c2:
        kpi_card(
            "🏢",
            "Companies",
            total_companies
        )

    with c3:
        kpi_card(
            "💰",
            "Average Salary",
            f"₹ {avg_salary:,}"
        )

    with c4:
        kpi_card(
            "🌍",
            "Remote Jobs",
            remote_jobs
        )

    st.divider()

    # =====================================================
    # CHARTS
    # =====================================================

    left, right = st.columns(2)

    # -----------------------------
    # Salary by Company
    # -----------------------------

    with left:

        st.subheader("💰 Average Salary by Company")

        salary_df = (

            filtered_df

            .groupby("Company")["Salary"]

            .mean()

            .reset_index()

            .sort_values(
                "Salary",
                ascending=False
            )

            .head(10)

        )

        fig = px.bar(

            salary_df,

            x="Company",

            y="Salary",

            color="Salary",

            text_auto=".2s",

            color_continuous_scale="Blues"

        )

        fig.update_layout(

            template="plotly_dark",

            height=420,

            showlegend=False

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Jobs by Location
    # -----------------------------

    with right:

        st.subheader("📍 Jobs by Location")

        location_df = (

            filtered_df["Location"]

            .value_counts()

            .reset_index()

        )

        location_df.columns = [

            "Location",

            "Jobs"

        ]

        fig = px.bar(

            location_df,

            x="Location",

            y="Jobs",

            color="Jobs",

            text_auto=True,

            color_continuous_scale="Viridis"

        )

        fig.update_layout(

            template="plotly_dark",

            height=420,

            showlegend=False

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # SECOND ROW
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("🌍 Remote Jobs")

        remote_df = (

            filtered_df["Remote"]

            .astype(str)

            .value_counts()

            .reset_index()

        )

        remote_df.columns = [

            "Type",

            "Jobs"

        ]

        fig = px.pie(

            remote_df,

            names="Type",

            values="Jobs",

            hole=.45

        )

        fig.update_layout(

            template="plotly_dark",

            height=420

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("💻 Most Demanded Skills")

        skills = top_skills(filtered_df)

        if skills.empty:

            st.info("No skills available.")

        else:

            fig = px.bar(

                skills,

                x="Demand",

                y="Skill",

                orientation="h",

                color="Demand",

                text_auto=True,

                color_continuous_scale="Turbo"

            )

            fig.update_layout(

                template="plotly_dark",

                height=420,

                yaxis=dict(
                    categoryorder="total ascending"
                )

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

        # =====================================================
    # RECENT JOBS
    # =====================================================

    st.markdown("## 🚀 Latest AI Jobs")

    recent_jobs = filtered_df.head(10)

    if recent_jobs.empty:

        st.warning("No jobs available.")

    else:

        for index, row in recent_jobs.iterrows():

            job_card(row)

            st.write(row.get("Apply Link"))
        

           
            st.markdown("---")


    # =====================================================
    # FEATURED JOBS
    # =====================================================

    st.markdown("## ⭐ Featured Jobs")

    if "Salary" in filtered_df.columns:

        featured = filtered_df.sort_values(
            by="Salary",
            ascending=False
        ).head(3)

    else:

        featured = filtered_df.head(3)

    cols = st.columns(3)

    for col, (_, row) in zip(cols, featured.iterrows()):

        with col:

            st.markdown(
                f"""
<div class="featured-job">

<h3>{row.get('Job Title','')}</h3>

<p><b>{row.get('Company','')}</b></p>

<hr>

<p>📍 {row.get('Location','')}</p>

<p>💰 ₹ {int(row.get('Salary',0)):,}</p>

<p>💼 {row.get('Employment Type','')}</p>

<p>🌍 {row.get('Remote','')}</p>

</div>
""",
                unsafe_allow_html=True
            )


    st.divider()


    # =====================================================
    # TOP HIRING COMPANIES
    # =====================================================

    st.markdown("## 🏢 Top Hiring Companies")

    summary = company_summary(filtered_df)

    if summary.empty:

        st.info("No company information available.")

    else:

        left, right = st.columns(2)

        for i, row in summary.head(6).iterrows():

            target = left if i % 2 == 0 else right

            with target:

                company_card(

                    company=row["Company"],

                    jobs=int(row["Jobs"]),

                    salary=int(row["Avg_Salary"]),

                    city=f"{row['Cities']} Cities",

                    skill="-"

                )


    st.divider()


    # =====================================================
    # QUICK INSIGHTS
    # =====================================================

    st.markdown("## 📈 Quick Insights")

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"""
### 🏢 Companies

**{filtered_df['Company'].nunique()}**

Active companies hiring today.
"""
        )

        st.info(
            f"""
### 📍 Locations

**{filtered_df['Location'].nunique()}**

Cities with job openings.
"""
        )

    with c2:

        highest = filtered_df.iloc[0]

        st.warning(
            f"""
### 💰 Highest Salary

₹ {int(highest.get('Salary',0)):,}

{highest.get('Company','')}
"""
        )

        st.info(
            f"""
### 🌍 Remote Jobs

**{remote_jobs}**

Remote opportunities available.
"""
        )


    st.divider()


    # =====================================================
    # DOWNLOAD DATA
    # =====================================================

    st.markdown("## 📥 Export")

    csv = convert_csv(filtered_df)

    st.download_button(

        "⬇ Download CSV",

        csv,

        "AI_Jobs.csv",

        "text/csv",

        use_container_width=True

    )


    # =====================================================
    # COMPLETE DATASET
    # =====================================================

    with st.expander("📋 View Complete Dataset"):

        st.dataframe(

            filtered_df,

            use_container_width=True,

            hide_index=True,

            height=500

        )


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("---")

    st.markdown(
        """
<div style="text-align:center;color:#94A3B8;padding:15px">

🤖 AI Job Market Dashboard

Live Data using JSearch API • Streamlit • Plotly • SQLite

</div>
""",
        unsafe_allow_html=True
    )