import streamlit as st
import pandas as pd


def jobs_page(df):

    st.title("💼 AI Jobs")
    st.caption("Find your dream AI, Data Science and Machine Learning job.")

    st.divider()

    # ==============================
    # DATA CLEANING
    # ==============================

    df = df.copy()

    df["Salary"] = pd.to_numeric(
        df["Salary"],
        errors="coerce"
    )

    # ==============================
    # SEARCH
    # ==============================

    search = st.text_input(
        "",
        placeholder="🔍 Search Job Title, Company or Skills...",
        label_visibility="collapsed"
    )

    # ==============================
    # FILTERS
    # ==============================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        company = st.selectbox(
            "Company",
            ["All"] + sorted(df["Company"].dropna().unique())
        )

    with c2:

        location = st.selectbox(
            "Location",
            ["All"] + sorted(df["Location"].dropna().unique())
        )

    with c3:

        employment = st.selectbox(
            "Employment Type",
            ["All"] + sorted(df["Employment Type"].dropna().unique())
        )

    with c4:

        remote = st.selectbox(
            "Remote",
            ["All"] + sorted(df["Remote"].astype(str).unique())
        )

    # ==============================
# SALARY FILTER
# ==============================

    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce").fillna(0)

    min_salary = int(df["Salary"].min())
    max_salary = int(df["Salary"].max())

    # If all salaries are the same (e.g. all 0), don't show a slider
    if min_salary == max_salary:
        st.info("Salary information is not available.")
        salary = (min_salary, max_salary)
    else:
        salary = st.slider(
            "💰 Salary Range",
            min_value=min_salary,
            max_value=max_salary,
            value=(min_salary, max_salary)
        )

    # ==============================
    # FILTER DATA
    # ==============================

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

    filtered = filtered[
        (filtered["Salary"] >= salary[0]) &
        (filtered["Salary"] <= salary[1])
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

    # ==============================
    # KPI
    # ==============================

    total_jobs = len(filtered)

    avg_salary = (
        int(filtered["Salary"].mean())
        if not filtered.empty else 0
    )

    companies = filtered["Company"].nunique()

    remote_jobs = (
        filtered["Remote"]
        .astype(str)
        .str.lower()
        .eq("yes")
        .sum()
    )

    a, b, c, d = st.columns(4)

    a.metric("💼 Jobs", total_jobs)

    b.metric("🏢 Companies", companies)

    c.metric("💰 Avg Salary", f"₹ {avg_salary:,}")

    d.metric("🌍 Remote", remote_jobs)

    st.divider()

    # ==============================
    # DOWNLOAD
    # ==============================

    csv = filtered.to_csv(index=False).encode()

    st.download_button(
        "📥 Download Filtered Jobs",
        csv,
        "jobs.csv",
        "text/csv"
    )

    st.divider()

    # ==============================
    # JOB CARDS
    # ==============================

    st.subheader("🚀 Available Jobs")

    if filtered.empty:

        st.warning("No jobs found.")

        return

    for _, row in filtered.iterrows():

        title = row["Job Title"]

        company = row["Company"]

        location = row["Location"]

        salary = row["Salary"]

        employment = row["Employment Type"]

        remote = row["Remote"]

        skills = row["Skills"]

        st.markdown(
            f"""
<div class="job-card">

<div class="job-top">

<div>

<h3>{title}</h3>

<p><b>{company}</b></p>

</div>

<div class="salary">

₹ {salary:,}

</div>

</div>

<br>

📍 {location}

&nbsp;&nbsp;&nbsp;

💼 {employment}

&nbsp;&nbsp;&nbsp;

🌍 {remote}

<br><br>

<b>Skills</b>

<br>

{skills}

</div>
""",
            unsafe_allow_html=True,
        )

    x, y = st.columns(2)

    with x:
      with st.expander("👁 View Details"):
        st.write("### Job Description")
        st.write(row.get("Description", "No description available."))

    with y:
      apply_link = row.get("Apply Link", "")

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
            use_container_width=True,
            key=f"apply{_}"
        )

        st.markdown("")

    st.divider()

    # ==============================
    # TABLE
    # ==============================

    with st.expander("📋 View Data Table"):

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
            height=500
        )