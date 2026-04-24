import requests
import redis
import json
from datetime import datetime
from backend.config import REDIS_URL, ADZUNA_APP_ID, ADZUNA_APP_KEY

r = redis.from_url(REDIS_URL)
STREAM_NAME = "jobs:raw"  # the Redis Stream we'll push to

def fetch_adzuna_jobs(what="software engineer", where="us", page=1):
    """
    Fetches jobs from Adzuna API.
    'what' = job title keyword
    'where' = country code
    """
    url = f"https://api.adzuna.com/v1/api/jobs/{where}/search/{page}"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": what,
        "results_per_page": 50,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # throws error if request failed
    return response.json().get("results", [])

def push_to_stream(jobs: list):
    """
    Pushes raw job dicts into a Redis Stream.
    Redis Streams are like an append-only log — great for pipelines.
    """
    for job in jobs:
        payload = {
            "external_id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "description": job.get("description"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "url": job.get("redirect_url"),
            "posted_at": job.get("created"),
            "source": "adzuna"
        }
        # xadd = "stream add" — appends one entry to the stream
        r.xadd(STREAM_NAME, {"data": json.dumps(payload)})

    print(f"Pushed {len(jobs)} jobs to Redis Stream")

def run_scraper():
    roles = ["software engineer", "python developer", "backend engineer", "ML engineer"]
    for role in roles:
        jobs = fetch_adzuna_jobs(what=role)
        push_to_stream(jobs)
