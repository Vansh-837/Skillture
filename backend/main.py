from backend.db.models import init_db
from backend.ingestion.scraper import run_scraper

if __name__ == "__main__":
    print("Initializing DB...")
    init_db()

    print("Running scraper...")
    run_scraper()

    print("Done. Now run the worker in a separate terminal.")
