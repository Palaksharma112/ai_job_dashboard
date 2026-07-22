import pandas as pd
import os

os.makedirs("data", exist_ok=True)

df = pd.DataFrame({
    "Job Title": [
        "Data Analyst",
        "Python Developer",
        "Data Scientist",
        "ML Engineer"
    ],
    "Company": [
        "TCS",
        "Infosys",
        "Accenture",
        "Microsoft"
    ],
    "Location": [
        "Jaipur",
        "Bangalore",
        "Pune",
        "Hyderabad"
    ],
    "Salary": [
        600000,
        800000,
        1200000,
        1500000
    ],
    "Experience": [
        "1-2 Years",
        "2-3 Years",
        "3-5 Years",
        "3-5 Years"
    ],
    "Employment Type": [
        "Full Time",
        "Full Time",
        "Full Time",
        "Full Time"
    ],
    "Remote": [
        "No",
        "Yes",
        "No",
        "Yes"
    ],
    "Skills": [
        "Python, SQL",
        "Python, Django",
        "Python, ML, SQL",
        "Python, AI, Deep Learning"
    ]
})


df.to_excel(
    "data/jobs.xlsx",
    index=False,
    engine="openpyxl"
)

print("jobs.xlsx created")