import streamlit as st
import pandas as pd
from api import get_jobs


# =====================================
# LOAD DATA
# =====================================

@st.cache_data(ttl=1800)
def load_data():

    try:
        df = get_jobs("Data Scientist")

        if df is None or df.empty:
            return pd.DataFrame()

        df.columns = df.columns.str.strip()

        # Required columns
        required_columns = [
            "Job Title",
            "Company",
            "Location",
            "Employment Type",
            "Salary",
            "Remote",
            "Skills",
            "Apply Link"
        ]

        for col in required_columns:
            if col not in df.columns:
                df[col] = ""

        df["Salary"] = pd.to_numeric(
            df["Salary"],
            errors="coerce"
        ).fillna(0)

        return df

    except Exception as e:
        st.error(f"Error loading jobs: {e}")
        return pd.DataFrame()


# =====================================
# FILTER DATA
# =====================================

def filter_jobs(
    df,
    company="All",
    location="All",
    employment="All",
    remote="All",
    search=""
):

    filtered = df.copy()

    if company != "All":
        filtered = filtered[
            filtered["Company"] == company
        ]

    if location != "All":
        filtered = filtered[
            filtered["Location"] == location
        ]

    if employment != "All":
        filtered = filtered[
            filtered["Employment Type"] == employment
        ]

    if remote != "All":
        filtered = filtered[
            filtered["Remote"].astype(str) == remote
        ]

    if search:
        filtered = filtered[
            filtered.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    return filtered


# =====================================
# KPI
# =====================================

def get_kpis(df):

    total_jobs = len(df)

    total_companies = (
        df["Company"].nunique()
        if "Company" in df.columns else 0
    )

    avg_salary = (
        int(df["Salary"].mean())
        if not df.empty else 0
    )

    remote_jobs = (
        df["Remote"]
        .astype(str)
        .str.lower()
        .eq("yes")
        .sum()
        if "Remote" in df.columns else 0
    )

    return (
        total_jobs,
        total_companies,
        avg_salary,
        remote_jobs
    )


# =====================================
# TOP SKILLS
# =====================================

def top_skills(df):

    if df.empty or "Skills" not in df.columns:
        return pd.DataFrame()

    skills = (
        df["Skills"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )

    skills.columns = [
        "Skill",
        "Demand"
    ]

    return skills


# =====================================
# COMPANY SUMMARY
# =====================================

def company_summary(df):

    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("Company")
        .agg(
            Jobs=("Company", "count"),
            Avg_Salary=("Salary", "mean"),
            Cities=("Location", "nunique")
        )
        .reset_index()
    )

    summary["Avg_Salary"] = (
        summary["Avg_Salary"]
        .fillna(0)
        .astype(int)
    )

    return summary


# =====================================
# DOWNLOAD CSV
# =====================================

def convert_csv(df):
    return df.to_csv(index=False).encode("utf-8")