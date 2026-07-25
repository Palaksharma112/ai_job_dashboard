import streamlit as st
import pandas as pd


# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():

    try:
        df = pd.read_excel(
            "data/jobs.xlsx",
            engine="openpyxl"
        )

        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()

        # Rename Salary column
        df.rename(
            columns={
                "Salary (LPA)": "Salary",
                "Salary(LPA)": "Salary",
                "salary (lpa)": "Salary",
                "salary(lpa)": "Salary"
            },
            inplace=True
        )

        # Convert Salary from LPA to Rupees
        if "Salary" in df.columns:

            df["Salary"] = (
                df["Salary"]
                .astype(str)
                .str.replace("LPA", "", regex=False)
                .str.replace("lpa", "", regex=False)
                .str.replace(",", "")
                .str.strip()
            )

            df["Salary"] = (
                pd.to_numeric(
                    df["Salary"],
                    errors="coerce"
                )
                .fillna(0)
                * 100000
            )

        # Convert Posted Date
        if "Posted Date" in df.columns:

            df["Posted Date"] = pd.to_datetime(
                df["Posted Date"],
                errors="coerce"
            )

        return df

    except Exception as e:

        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()


# =====================================================
# FILTER JOBS
# =====================================================

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
            filtered["Remote"].astype(str) == str(remote)
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


# =====================================================
# KPI
# =====================================================

def get_kpis(df):

    total_jobs = len(df)

    total_companies = (
        df["Company"].nunique()
        if "Company" in df.columns else 0
    )

    avg_salary = (
        int(df["Salary"].mean())
        if "Salary" in df.columns and not df.empty
        else 0
    )

    remote_jobs = (
        df["Remote"]
        .astype(str)
        .str.lower()
        .str.contains("remote|yes|true|work from home")
        .sum()
        if "Remote" in df.columns
        else 0
    )

    return (
        total_jobs,
        total_companies,
        avg_salary,
        remote_jobs
    )


# =====================================================
# COMPANY SUMMARY
# =====================================================

def company_summary(df):

    summary = (

        df.groupby("Company", dropna=False)

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


# =====================================================
# TOP SKILLS
# =====================================================

def top_skills(df):

    skills = []

    if "Skills" not in df.columns:
        return pd.DataFrame(
            columns=["Skill", "Demand"]
        )

    for value in df["Skills"].dropna():

        for skill in str(value).split(","):

            skill = skill.strip()

            if skill:
                skills.append(skill)

    if not skills:

        return pd.DataFrame(
            columns=["Skill", "Demand"]
        )

    return (

        pd.Series(skills)

        .value_counts()

        .head(10)

        .reset_index()

        .rename(
            columns={
                "index": "Skill",
                "count": "Demand",
                0: "Demand"
            }
        )

    )


# =====================================================
# HIGHEST PAYING COMPANIES
# =====================================================

def highest_paying_companies(df):

    return (

        df.groupby("Company")["Salary"]

        .mean()

        .sort_values(ascending=False)

        .head(10)

    )


# =====================================================
# JOBS BY CITY
# =====================================================

def jobs_by_city(df):

    return df["Location"].value_counts()


# =====================================================
# JOBS BY TYPE
# =====================================================

def jobs_by_type(df):

    return df["Employment Type"].value_counts()


# =====================================================
# SEARCH
# =====================================================

def search_jobs(df, keyword):

    if not keyword:
        return df

    return df[
        df.astype(str)
        .apply(
            lambda x: x.str.contains(
                keyword,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]


# =====================================================
# DATASET INFO
# =====================================================

def dataset_info(df):

    return {

        "Total Jobs": len(df),

        "Total Companies": df["Company"].nunique(),

        "Total Cities": df["Location"].nunique(),

        "Average Salary": round(
            df["Salary"].mean(),
            2
        )

    }


# =====================================================
# CSV DOWNLOAD
# =====================================================

def convert_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")