import requests
import pandas as pd

API_KEY = "a328c18496msh66feda03a85de26p18cc9djsn86c106ae92e2"

URL = "https://jsearch.p.rapidapi.com/search-v2"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}


def get_jobs(query="Data Scientist", page=1):

    params = {
        "query": query,
        "page": page,
        "num_pages": 1,
        "country": "in",
        "date_posted": "all"
    }

    try:

        response = requests.get(
            URL,
            headers=HEADERS,
            params=params,
            timeout=30
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return pd.DataFrame()

        data = response.json()

        print(data)

    except Exception as e:
        print("Request Error:", e)
        return pd.DataFrame()

    jobs = []

    # ---------- Find job list safely ----------

    if isinstance(data, dict):

        if isinstance(data.get("data"), list):
            jobs = data["data"]

        elif isinstance(data.get("data"), dict):

            if isinstance(data["data"].get("jobs"), list):
                jobs = data["data"]["jobs"]

            elif isinstance(data["data"].get("results"), list):
                jobs = data["data"]["results"]

    if not jobs:
        print("No jobs found.")
        return pd.DataFrame()

    records = []

    for job in jobs:

        if not isinstance(job, dict):
            continue

        records.append({
    "Job Title": job.get("job_title", ""),
    "Company": job.get("employer_name", ""),
    "Location": job.get("job_city") or job.get("job_country", ""),
    "Employment Type": job.get("job_employment_type", ""),
    "Remote": "Yes" if job.get("job_is_remote") else "No",
    "Salary": job.get("job_min_salary") or 0,
    "Skills": "",
    "Apply Link": job.get("job_apply_link", "")
})

    return pd.DataFrame(records)