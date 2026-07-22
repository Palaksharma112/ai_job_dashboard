import streamlit as st
import pandas as pd
import plotly.express as px


def analytics_page(df):

    st.title("📊 Analytics Dashboard")
    st.caption("AI Job Market Insights & Trends")

    st.divider()

    # ==========================
    # Data Cleaning
    # ==========================

    df = df.copy()

    df["Salary"] = pd.to_numeric(
        df["Salary"],
        errors="coerce"
    )

    # ==========================
    # KPI CARDS
    # ==========================

    total_jobs = len(df)

    avg_salary = int(df["Salary"].mean())

    companies = df["Company"].nunique()

    locations = df["Location"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📄 Total Jobs", total_jobs)

    c2.metric("🏢 Companies", companies)

    c3.metric("📍 Cities", locations)

    c4.metric("💰 Avg Salary", f"₹ {avg_salary:,}")

    st.divider()

    # ==================================================
    # ROW 1
    # ==================================================

    left, right = st.columns(2)

    # ---------------- Salary by Company ----------------

    with left:

        st.subheader("💰 Average Salary by Company")

        salary_company = (

            df.groupby("Company")["Salary"]

            .mean()

            .sort_values(ascending=False)

            .head(10)

            .reset_index()

        )

        fig = px.bar(

            salary_company,

            x="Company",

            y="Salary",

            color="Salary",

            color_continuous_scale="Blues",

            text="Salary"

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

    # ---------------- Jobs by Location ----------------

    with right:

        st.subheader("📍 Jobs by Location")

        location = (

            df["Location"]

            .value_counts()

            .head(10)

            .reset_index()

        )

        location.columns = [

            "Location",

            "Jobs"

        ]

        fig = px.bar(

            location,

            x="Location",

            y="Jobs",

            color="Jobs",

            color_continuous_scale="Viridis",

            text="Jobs"

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

    # ==================================================
    # ROW 2
    # ==================================================

    left, right = st.columns(2)

    # ---------------- Remote Jobs ----------------

    with left:

        st.subheader("🌍 Remote vs On-site")

        remote = (

            df["Remote"]

            .astype(str)

            .value_counts()

            .reset_index()

        )

        remote.columns = [

            "Type",

            "Jobs"

        ]

        fig = px.pie(

            remote,

            names="Type",

            values="Jobs",

            hole=.45,

            color_discrete_sequence=px.colors.qualitative.Set2

        )

        fig.update_layout(

            template="plotly_dark",

            height=420

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ---------------- Employment Type ----------------

    with right:

        st.subheader("💼 Employment Type")

        emp = (

            df["Employment Type"]

            .value_counts()

            .reset_index()

        )

        emp.columns = [

            "Employment",

            "Jobs"

        ]

        fig = px.bar(

            emp,

            x="Employment",

            y="Jobs",

            color="Jobs",

            text="Jobs",

            color_continuous_scale="Teal"

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

    # ==================================================
    # TOP SKILLS
    # ==================================================

    st.subheader("💻 Most Demanded Skills")

    skills = (

        df["Skills"]

        .dropna()

        .str.split(",")

        .explode()

        .str.strip()

        .value_counts()

        .head(15)

        .reset_index()

    )

    skills.columns = [

        "Skill",

        "Demand"

    ]

    fig = px.bar(

        skills,

        x="Demand",

        y="Skill",

        orientation="h",

        color="Demand",

        text="Demand",

        color_continuous_scale="Turbo"

    )

    fig.update_layout(

        template="plotly_dark",

        height=550,

        yaxis=dict(

            categoryorder="total ascending"

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ==================================================
    # SALARY DISTRIBUTION
    # ==================================================

    st.subheader("📈 Salary Distribution")

    fig = px.histogram(

        df,

        x="Salary",

        nbins=20,

        color_discrete_sequence=["#3B82F6"]

    )

    fig.update_layout(

        template="plotly_dark",

        height=450

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ==================================================
    # TOP COMPANIES
    # ==================================================

    st.subheader("🏆 Top Hiring Companies")

    top = (

        df["Company"]

        .value_counts()

        .head(10)

        .reset_index()

    )

    top.columns = [

        "Company",

        "Jobs"

    ]

    fig = px.bar(

        top,

        x="Jobs",

        y="Company",

        orientation="h",

        text="Jobs",

        color="Jobs",

        color_continuous_scale="Plasma"

    )

    fig.update_layout(

        template="plotly_dark",

        height=500,

        yaxis=dict(

            categoryorder="total ascending"

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ==================================================
    # DATA TABLE
    # ==================================================

    with st.expander("📄 View Dataset"):

        st.dataframe(

            df,

            use_container_width=True,

            hide_index=True,

            height=500

        )

    st.success("Analytics Generated Successfully.")