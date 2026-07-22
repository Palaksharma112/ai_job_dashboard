import streamlit as st
import pandas as pd
import plotly.express as px


def companies_page(df):

    st.title("🏢 Companies")
    st.caption("Explore hiring companies and their recruitment statistics.")

    st.divider()

    # ----------------------------
    # Data Cleaning
    # ----------------------------

    df = df.copy()

    df["Salary"] = pd.to_numeric(
        df["Salary"],
        errors="coerce"
    )

    # ----------------------------
    # Search Company
    # ----------------------------

    search = st.text_input(
        "",
        placeholder="🔍 Search Company...",
        label_visibility="collapsed"
    )

    if search:
        df = df[
            df["Company"]
            .astype(str)
            .str.contains(search, case=False)
        ]

    companies = sorted(df["Company"].dropna().unique())

    if len(companies) == 0:
        st.warning("No companies found.")
        return

    # ----------------------------
    # KPI Cards
    # ----------------------------

    total_companies = len(companies)

    total_jobs = len(df)

    avg_salary = int(df["Salary"].mean()) if not df.empty else 0

    locations = df["Location"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🏢 Companies", total_companies)
    c2.metric("💼 Jobs", total_jobs)
    c3.metric("📍 Cities", locations)
    c4.metric("💰 Avg Salary", f"₹ {avg_salary:,}")

    st.divider()

    # ----------------------------
    # Top Hiring Companies Chart
    # ----------------------------

    st.subheader("📋 Company Summary")

    summary = (
        df.groupby("Company", dropna=False)
        .agg(
            Jobs=("Company", "count"),
            Avg_Salary=("Salary", "mean"),
            Cities=("Location", "nunique")
        )
        .reset_index()
    )

    summary["Avg_Salary"] = summary["Avg_Salary"].fillna(0).astype(int)

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )