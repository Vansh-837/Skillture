from sqlalchemy import create_engine, Column, String, DateTime, Text, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from backend.config import POSTGRES_URL

Base = declarative_base()
engine = create_engine(POSTGRES_URL)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String, unique=True)   # ID from the source API
    title = Column(String, nullable=False)
    company = Column(String)
    location = Column(String)
    description = Column(Text)
    salary_min = Column(Float)
    salary_max = Column(Float)
    source = Column(String)                     # "adzuna", "remotive", etc.
    url = Column(String)
    posted_at = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)  # creates the table if it doesn't exist
