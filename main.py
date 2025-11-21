# main.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import requests
from requests.exceptions import RequestException
from scraper import parse_job_page, scrape_jobs
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI(title="Job Scraper API")

# Allow CORS (for frontend testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model for job data
class ScrapeResponse(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    salary: str | None = None
    posted: str | None = None
    description: str | None = None
    requirements: list[str] = []
    apply_link: str | None = None

# Request headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JobScraper/1.0; +https://yourdomain.example/)"
}

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Job Scraper API!"}

# Endpoint to scrape jobs (local or pre-defined)
@app.get("/scrape", response_model=list[ScrapeResponse])
def scrape_local():
    jobs = scrape_jobs()
    return jobs

# Endpoint to scrape a single live job page
@app.get("/scrape-job", response_model=ScrapeResponse)
def scrape_job(url: str = Query(..., description="URL of the job posting to scrape")):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")

    parsed = parse_job_page(resp.text, base_url=url)
    parsed.setdefault("requirements", [])
    return parsed
