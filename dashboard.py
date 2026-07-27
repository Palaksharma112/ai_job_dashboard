import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

from utils import (
    load_data,
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


# =====================================================
# SIDEBAR
# =====================================================

def sidebar(df):

    with st.sidebar:

        profile_card(
            st.session_state.get("username", "User")
        )

        st.html("---")

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
            default_index=0
        )

        st.html("---")

        st.subheader("🔍 Filters")

        company = st.selectbox(
            "Company",
            ["All"] + sorted(df["Company"].dropna().unique().tolist())
        )

        location = st.selectbox(
            "Location",
            ["All"] + sorted(df["Location"].dropna().unique().tolist())
        )

        employment = st.selectbox(
            "Employment Type",
            ["All"] + sorted(df["Employment Type"].dropna().unique().tolist())
        )

        remote = st.selectbox(
            "Remote",
            ["All"] + sorted(
                df["Remote"]
                .astype(str)
                .unique()
                .tolist()
            )
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


# =====================================================
# HEADER
# =====================================================

def dashboard_header():

    col1, col2 = st.columns([6, 1])

    with col1:
        page_header(
            "💼 IT Job Market Dashboard",
            "Explore IT Jobs using your own dataset"
        )

    with col2:
        st.write("")
        st.write("")

        if st.button(
            "Logout",
            key="header_logout",
            use_container_width=True
        ):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

    st.write("")

    st.markdown("### 🔍 Search Jobs")

    c1, c2 = st.columns([1, 4], gap="small")

    with c1:
        search_by = st.selectbox(
            "Search By",
            [
                "All",
                "Job Title",
                "Company",
                "Skills",
                "Location"
            ],
            index=0
        )

    with c2:
        search = st.text_input(
            "Search",
            placeholder="🔍 Enter keyword...",
            label_visibility="collapsed"
        )

    return search, search_by

# =====================================================
# DASHBOARD PAGE
# =====================================================

def dashboard_page():

    with st.spinner("Loading IT Job Dataset..."):

        df = load_data()

        search, search_by = dashboard_header()

        filtered_df = df.copy()

    if search.strip():

     if search_by == "All":

        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    elif search_by == "Job Title":

        filtered_df = filtered_df[
            filtered_df["Job Title"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    elif search_by == "Company":

        filtered_df = filtered_df[
            filtered_df["Company"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    elif search_by == "Location":

        filtered_df = filtered_df[
            filtered_df["Location"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    elif search_by == "Skills":

        filtered_df = filtered_df[
            filtered_df["Skills"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if df.empty:

        st.error("Dataset not found.")

        return

    (
        selected,
        company,
        location,
        employment,
        remote
    ) = sidebar(df)

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

    

    filtered_df = filter_jobs(
        df=df,
        company=company,
        location=location,
        employment=employment,
        remote=remote,
        search=search
    )

    if filtered_df.empty:

        st.warning("No jobs found.")

        return

    (
        total_jobs,
        total_companies,
        avg_salary,
        remote_jobs
    ) = get_kpis(filtered_df)

    st.html("## 📊 Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card("💼", "Jobs", total_jobs)

    with c2:
        kpi_card("🏢", "Companies", total_companies)

    with c3:
        kpi_card("💰", "Average Salary", f"₹ {avg_salary:,.2f} LPA")

    with c4:
        kpi_card("🌍", "Remote Jobs", remote_jobs)

    st.divider()


        # =====================================================
    # FIRST ROW CHARTS
    # =====================================================

    left, right = st.columns(2)

    # ---------------------------------
    # Average Salary by Company
    # ---------------------------------

    with left:

        st.subheader("💰 Average Salary by Company")

        salary_df = (
            filtered_df
            .groupby("Company", as_index=False)["Salary"]
            .mean()
            .sort_values(
                by="Salary",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            salary_df,
            x="Company",
            y="Salary",
            color="Salary",
            text_auto=".2f",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            showlegend=False,
            xaxis_title="Company",
            yaxis_title="Salary (LPA)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------------------------
    # Jobs by Location
    # ---------------------------------

    with right:

        st.subheader("📍 Jobs by Location")

        location_df = (
            filtered_df["Location"]
            .dropna()
            .value_counts()
            .head(10)          # Show only top 10 locations
            .reset_index()
        )

        location_df.columns = ["Location", "Jobs"]

        fig = px.bar(
            location_df,
            x="Jobs",
            y="Location",
            orientation="h",
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

    # ---------------------------------
    # Remote Jobs
    # ---------------------------------

    with left:

        st.subheader("🌍 Remote vs On-site")

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
            hole=0.45
        )

        fig.update_layout(
            template="plotly_dark",
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ---------------------------------
    # Top Skills
    # ---------------------------------

    with right:

        st.subheader("💻 Most Demanded Skills")

        skills_df = top_skills(filtered_df)

        if skills_df.empty:

            st.info("No Skills Available")

        else:

            fig = px.bar(
                skills_df,
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
    # LATEST JOBS
    # =====================================================

    st.html("## 🚀 Latest IT Jobs")

    recent_jobs = filtered_df.head(10)

    if recent_jobs.empty:

        st.warning("No jobs available.")

    else:

        for _, row in recent_jobs.iterrows():

            job_card(row)

    st.divider()


    # =====================================================
    # FEATURED JOBS
    # =====================================================

    st.html("## ⭐ Featured Jobs")

    featured = (
        filtered_df
        .sort_values(
            by="Salary",
            ascending=False
        )
        .head(3)
    )

    cols = st.columns(3)

    for col, (_, row) in zip(cols, featured.iterrows()):

        with col:

            st.html(
                f"""
<div class="featured-job">

<h3>{row['Job Title']}</h3>

<p><b>{row['Company']}</b></p>

<hr>

<p>📍 {row['Location']}</p>

<p>💰 ₹ {row['Salary']} LPA</p>

<p>💼 {row['Employment Type']}</p>

<p>🌍 {row['Remote']}</p>

</div>
                """

               
            )

    st.divider()


    # =====================================================
    # TOP HIRING COMPANIES
    # =====================================================

    st.html("## 🏢 Top Hiring Companies")

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

                    salary=float(row["Avg_Salary"]),

                    city=f"{row['Cities']} Cities",

                    skill="-"

                )

    st.divider()


    # =====================================================
    # QUICK INSIGHTS
    # =====================================================

    st.html("## 📈 Quick Insights")

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"""
### 💼 Total Jobs

**{len(filtered_df)}**

Jobs currently available.
"""
        )

        st.info(
            f"""
### 🏢 Companies

**{filtered_df['Company'].nunique()}**

Companies hiring now.
"""
        )

    with c2:

        highest_salary = filtered_df["Salary"].max()

        highest_job = filtered_df.loc[
            filtered_df["Salary"].idxmax()
        ]

        st.warning(
            f"""
### 💰 Highest Salary

₹ {highest_salary} LPA

**{highest_job['Company']}**
"""
        )

        st.info(
            f"""
### 📍 Cities

**{filtered_df['Location'].nunique()}**

Cities with job openings.
"""
        )

    st.divider()

        # =====================================================
    # DOWNLOAD DATA
    # =====================================================

    st.html("## 📥 Export Dataset")

    csv = convert_csv(filtered_df)

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="IT_Job_Market_Dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()


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
    # DATASET SUMMARY
    # =====================================================

    st.html("## 📊 Dataset Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Total Records",
            len(filtered_df)
        )

    with c2:

        st.metric(
            "Companies",
            filtered_df["Company"].nunique()
        )

    with c3:

        st.metric(
            "Locations",
            filtered_df["Location"].nunique()
        )

    st.divider()


    # =====================================================
    # FOOTER
    # =====================================================

    st.html(
        """
---
<div style="text-align:center;padding:20px">

<h3>💼 IT Job Market Dashboard</h3>

<p>Developed using <b>Python • Streamlit • Pandas • Plotly • SQLite</b></p>

<p>📊 Analyze IT jobs by Company, Salary, Skills, Location and Employment Type.</p>

<p>© 2026 | Created by <b>Palak Sharma</b></p>

</div>
"""
    )