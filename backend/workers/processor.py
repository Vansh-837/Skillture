import json
import redis
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from backend.db.models import Job
from backend.config import REDIS_URL, POSTGRES_URL
from datetime import datetime

r = redis.from_url(REDIS_URL)
engine = create_engine(POSTGRES_URL)
STREAM_NAME = "jobs:raw"
CONSUMER_GROUP = "job-processors"

def ensure_consumer_group():
    """
    Consumer groups let multiple workers read from the same stream
    without processing the same message twice.
    """
    try:
        r.xgroup_create(STREAM_NAME, CONSUMER_GROUP, id="0", mkstream=True)
    except Exception:
        pass  # group already exists, that's fine

def process_jobs():
    ensure_consumer_group()

    while True:
        # Read up to 10 messages at a time, block for 2s if stream is empty
        messages = r.xreadgroup(
            CONSUMER_GROUP, "worker-1",
            {STREAM_NAME: ">"}, count=10, block=2000
        )

        if not messages:
            continue

        with Session(engine) as session:
            for stream, entries in messages:
                for entry_id, data in entries:
                    job_data = json.loads(data[b"data"])

                    # Skip if we already have this job
                    exists = session.query(Job).filter_by(
                        external_id=job_data["external_id"]
                    ).first()

                    if not exists:
                        job = Job(
                            external_id=job_data["external_id"],
                            title=job_data["title"],
                            company=job_data["company"],
                            location=job_data["location"],
                            description=job_data["description"],
                            salary_min=job_data.get("salary_min"),
                            salary_max=job_data.get("salary_max"),
                            url=job_data["url"],
                            source=job_data["source"],
                            posted_at=datetime.fromisoformat(job_data["posted_at"])
                            if job_data.get("posted_at") else None
                        )
                        session.add(job)

                    # Acknowledge message — tells Redis "we handled this"
                    r.xack(STREAM_NAME, CONSUMER_GROUP, entry_id)

            session.commit()
            print("Batch committed to Postgres")

if __name__ == "__main__":
    process_jobs()
