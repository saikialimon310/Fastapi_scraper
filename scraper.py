# scraper.py
from bs4 import BeautifulSoup

def parse_job_page(html: str, base_url: str = "") -> dict:
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
    ][:10]  # Limit to 10 for brevity

    apply_link = soup.select_one("a[href*='apply'], a.apply-btn")
    apply_url = (
        apply_link["href"] if apply_link and "href" in apply_link.attrs else base_url
    )

    return {
        "title": title.get_text(strip=True) if title else None,
        "company": company.get_text(strip=True) if company else None,
        "location": location.get_text(strip=True) if location else None,
        "salary": salary.get_text(strip=True) if salary else None,
        "posted": posted.get_text(strip=True) if posted else None,
        "description": description.get_text(strip=True) if description else None,
        "requirements": requirements,
        "apply_link": apply_url,
    }


def scrape_jobs() -> list[dict]:
    """Mock job list scraper (you can replace this with real scraping)."""
    return [
        {
            "title": "Software Developer",
            "company": "TechCorp Ltd",
            "location": "Guwahati, Assam",
            "salary": "₹6 LPA",
            "posted": "2 days ago",
            "description": "Develop and maintain web applications using Python and React.",
            "requirements": ["Python", "FastAPI", "React", "REST APIs"],
            "apply_link": "https://example.com/apply",
        },
        {
            "title": "Data Analyst",
            "company": "DataWorks Pvt. Ltd",
            "location": "Remote",
            "salary": "₹5 LPA",
            "posted": "1 week ago",
            "description": "Analyze data and build dashboards.",
            "requirements": ["SQL", "Pandas", "PowerBI"],
            "apply_link": "https://example.com/apply-data",
        },
    ]
