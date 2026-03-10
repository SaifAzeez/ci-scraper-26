"""
Donation Tracker Backend
========================
Starts the background scraper then serves the FastAPI app via uvicorn.

Usage:
    pip install -r requirements.txt
    python main.py
"""

import logging

import uvicorn

from scraper import start_background_scraper
from api import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

if __name__ == "__main__":
    print("=" * 55)
    print("  UB ISoc Gaza Appeal — Donation Tracker Backend")
    print("=" * 55)
    print("Starting background scraper...")
    start_background_scraper()

    print("Starting API server at http://localhost:8000")
    print("Endpoint: http://localhost:8000/api/donations")
    print("Health:   http://localhost:8000/health")
    print("Docs:     http://localhost:8000/docs")
    print("=" * 55)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
