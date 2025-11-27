import os
from bs4 import BeautifulSoup
from pymongo import MongoClient




local_files = [
    "C:\wamp64\www\job.html",
    "C:\wamp64\www\job2.html",
    "C:\wamp64\www\job3.html",
    "C:\wamp64\www\job4.html",
    "C:\wamp64\www\job5.html",
    "C:\wamp64\www\job6.html",
    "C:\wamp64\www\job7.html",
    "C:\wamp64\www\job8.html",
    "C:\wamp64\www\job9.html",
    "C:\wamp64\www\job10.html",
    "C:\wamp64\www\job11.html",
    "C:\wamp64\www\job12.html",
    "C:\wamp64\www\job13.html",
    "C:\wamp64\www\job14.html",
    "C:\wamp64\www\job15.html",
    "C:\wamp64\www\job16.html",
    "C:\wamp64\www\job17.html",
    "C:\wamp64\www\job18.html",
    "C:\wamp64\www\job19.html",
    "C:\wamp64\www\job20.html",
    "C:\wamp64\www\job21.html",
    "C:\wamp64\www\job22.html",
    
]

client = MongoClient("mongodb://localhost:27017/")
db = client["job_database"]
collection = db["jobs"]


def extract_job_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()
    """Parse a single job posting HTML and return job details."""
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one("h1, .job-title, .title")
    company = soup.select_one(".company, .job-company, [itemprop='hiringOrganization']")
    location = soup.select_one(".location, [itemprop='jobLocation']")
    salary = soup.select_one(".salary, [itemprop='baseSalary']")
    posted = soup.select_one(".posted-date, .date, time")
    description = soup.select_one(".job-description, #job-desc, article, .desc")

    requirements = [
        li.get_text(strip=True)
        for li in soup.select(".requirements li, .qualifications li, ul li")
    ][:10] 

    apply_link = soup.select_one("a[href*='apply'], a.apply-btn")
    apply_url = (
        apply_link["href"] if apply_link and "href" in apply_link.attrs else None
    )

    job = {
        "title": title.get_text(strip=True) if title else None,
        "company": company.get_text(strip=True) if company else None,
        "location": location.get_text(strip=True) if location else None,
        "salary": salary.get_text(strip=True) if salary else None,
        "posted": posted.get_text(strip=True) if posted else None,
        "description": description.get_text(strip=True) if description else None,
        "requirements": requirements,
        "apply_link": apply_url,
    }

    return job




for file_path in local_files:
    if os.path.exists(file_path):
        job = extract_job_data(file_path)
        collection.insert_one(job)
        

        print(f"✓ Inserted into MongoDB: {file_path}")
    else:
        print(f"✗ File not found: {file_path}")

print("\n All job data inserted into MongoDB successfully!")

