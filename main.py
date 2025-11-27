
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import requests
from requests.exceptions import RequestException
from scrapper_bs import extract_job_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Job Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScrapeResponse(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    salary: str | None = None
    posted: str | None = None
    description: str | None = None
    requirements: list[str] = []
    apply_link: str | None = None


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JobScraper/1.0; +https://yourdomain.example/)"
}


@app.get("/")
def home():
    return {"message": "Welcome to Job Scraper API!"}


@app.get("/scrape", response_model=list[ScrapeResponse])
def scrape_local():
    jobs = scrape_jobs()
    return jobs


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
