# Skillture - Skills of Future
A real-time job market analytics system that scrapes and processes job postings at scale, models demand trends, and uses AI to extract skill signals and generate structured insights




Job Market Intelligence Platform. Scrapes job postings in real-time, tracks demand trends, and uses AI to surface insights. Highly relevant to your life right now, great story to tell in interviews.

Architecture
Data Sources (Job APIs / scrapers)
        ↓
  Ingestion Layer (Kafka / Redis Streams)
        ↓
  Processing Worker (Python, Celery)
        ↓
  Storage (Postgres + pgvector)
        ↓
  FastAPI Backend
        ↓
  React Dashboard (WebSockets for live updates)
        +
  AI Layer (sits between storage & API)

The AI Features (non-trivial ones)

Trend summarization — every 24hrs, LLM summarizes what skills are rising/falling in demand across new postings
Semantic job search — pgvector embeddings so you can search "jobs like Stripe but smaller" and get real results
Salary anomaly detection — flag outlier postings (unusually high/low for the role)
Weekly insight digest — auto-generated report: "This week, demand for Rust engineers grew 12% in fintech"


Tech Stack
LayerTechScraping/IngestionPython, apify or scrapy, Redis StreamsTask QueueCelery + RedisDatabasePostgres + pgvectorBackendFastAPIAIOpenAI API + embeddingsFrontendReact + Recharts + WebSocketsDeployRailway or Render (backend), Vercel (frontend)SchedulerAPScheduler or cron via Celery Beat

Week-by-Week Build Plan (4 weeks)
Week 1 — Data Pipeline

Set up scraper hitting 2-3 job sources (Adzuna API is free, Remotive, HN Who's Hiring)
Redis Streams ingestion
Celery workers processing and storing in Postgres
Goal: 500+ jobs flowing in cleanly

Week 2 — Backend + AI

FastAPI endpoints (jobs, trends, search)
pgvector embeddings for semantic search
LLM summarization pipeline (daily cron)
Anomaly detection (simple z-score first, dress it up with AI explanation)

Week 3 — Frontend

React dashboard: live feed, trend charts (Recharts), semantic search bar
WebSockets for real-time new posting notifications
Filters by role, location, stack, salary

Week 4 — Polish + Ship

Deploy everything
Write a killer README with demo GIF
Add a "How it works" architecture diagram
Seed it with real data so the demo looks alive


What This Proves to Recruiters

You can design and build a multi-component system from scratch
You understand async processing, queues, and real-time data
Your AI usage is purposeful, not just slapping GPT on everything
You can deploy and maintain something real

This is a fundamentally different class of project than anything on your GitHub right now. Want me to help you scaffold the project structure or start with any specific component?You said: ok lets start with a good name for the project, github repo and week 1 stuff.ok lets start with a good name for the project, github repo and week 1 stuff. I wanna learn too alongwith so keep teaching me wht code we are doing and why.2:23 PMClaude responded: Love that mindset.Love that mindset. Let's do this properly.

Name & Branding
TalentPulse — tracks the pulse of the job market in real-time. Clean, professional, memorable. Works as a repo name, a demo URL, everything.

github.com/Vansh-837/TalentPulse


Week 1 Goal
By end of week 1 you should have real job data flowing automatically from sources → Redis → Postgres. No frontend yet, no AI yet. Just clean, reliable data infrastructure.

First — understand the architecture we're building this week
Job APIs
   ↓
Scraper (Python) — fetches jobs every X minutes
   ↓
Redis Streams — a queue that holds raw jobs temporarily
   ↓
Celery Worker — picks jobs off the queue, cleans them, saves to DB
   ↓
Postgres — permanent storage
Why this pattern and not just "fetch → save directly"?
Because direct fetch→save breaks under load and is fragile. Redis Streams acts as a buffer — if your DB goes down, jobs pile up in Redis and nothing is lost. Celery workers can scale horizontally. This is how real production systems are built, and it's what makes this project impressive.

Step 1 — Project Setup
Create this folder structure:
TalentPulse/
├── backend/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── scraper.py        # fetches jobs from APIs
│   ├── workers/
│   │   ├── __init__.py
│   │   └── processor.py      # celery worker
│   ├── db/
│   │   ├── __init__.py
│   │   └── models.py         # postgres table definitions
│   ├── config.py
│   └── main.py
├── docker-compose.yml         # runs Redis + Postgres locally
├── requirements.txt
└── .env

