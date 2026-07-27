import streamlit as st
import pandas as pd

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(show_spinner=False)
def load_data():
    try:
        st.write("📂 Loading dataset...")

        df = pd.read_excel(
            "data/jobs.xlsx",
            engine="openpyxl"
        )

        st.write(f"✅ Dataset Loaded: {len(df):,} Records")

        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()

        # Rename Salary column if required
        if "Salary (LPA)" in df.columns:
            df.rename(
                columns={"Salary (LPA)": "Salary"},
                inplace=True
            )

        # Salary
        if "Salary" in df.columns:
            df["Salary"] = (
                pd.to_numeric(
                    df["Salary"],
                    errors="coerce"
                )
                .fillna(0)
            )

        # Posted Date
        if "Posted Date" in df.columns:
            df["Posted Date"] = pd.to_datetime(
                df["Posted Date"],
                errors="coerce"
            )

        # Remove duplicate rows
        df.drop_duplicates(inplace=True)

        # Replace NaN values
        df.fillna("", inplace=True)

        st.success("✅ Data Ready")

        return df

    except FileNotFoundError:
        st.error("❌ data/jobs.xlsx not found.")
        return pd.DataFrame()

    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")
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

    if search and search != "All":

        filtered = filtered[
            filtered["Job Title"]
            .astype(str)
            .str.contains(
                str(search),
                case=False,
                na=False
            )
        ]

    return filtered


# =====================================================
# KPI
# =====================================================

def get_kpis(df):

    total_jobs = len(df)

    total_companies = (
        df["Company"].nunique()
        if "Company" in df.columns
        else 0
    )

    avg_salary = (
        int(df["Salary"].mean())
        if "Salary" in df.columns and not df.empty
        else 0
    )

    remote_jobs = df[
    df["Remote"]
    .astype(str)
    .str.lower()
    .str.contains("remote")
].shape[0]

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

    if df.empty:
        return pd.DataFrame()

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

    if "Skills" not in df.columns:
        return pd.DataFrame(
            columns=["Skill", "Demand"]
        )

    skills = []

    for value in df["Skills"].dropna():

        for skill in str(value).split(","):

            skill = skill.strip()

            if skill:
                skills.append(skill)

    if len(skills) == 0:
        return pd.DataFrame(
            columns=["Skill", "Demand"]
        )

    skill_df = (
        pd.Series(skills)
        .value_counts()
        .reset_index()
    )

    skill_df.columns = [
        "Skill",
        "Demand"
    ]

    return skill_df.head(10)


# =====================================================
# HIGHEST PAYING COMPANIES
# =====================================================

def highest_paying_companies(df):

    if df.empty:
        return pd.DataFrame()

    return (
        df.groupby("Company")["Salary"]
        .mean()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )


# =====================================================
# JOBS BY CITY
# =====================================================

def jobs_by_city(df):

    return (
        df["Location"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index": "Location",
                "Location": "Jobs"
            }
        )
    )


# =====================================================
# JOBS BY EMPLOYMENT TYPE
# =====================================================

def jobs_by_type(df):

    return (
        df["Employment Type"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index": "Employment Type",
                "Employment Type": "Jobs"
            }
        )
    )


# =====================================================
# SEARCH JOBS
# =====================================================

def search_jobs(df, keyword):

    if keyword == "":
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

    avg_salary = 0

    if "Salary" in df.columns and not df.empty:
        avg_salary = round(
            df["Salary"].mean(),
            2
        )

    return {

        "Total Jobs": len(df),

        "Total Companies":
        df["Company"].nunique(),

        "Total Cities":
        df["Location"].nunique(),

        "Average Salary":
        avg_salary
    }


# =====================================================
# DOWNLOAD CSV
# =====================================================

def convert_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")