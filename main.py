# main.py
import os
import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_state, start_background_scraper

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: kick off the background scraper
    print("Starting background scraper...")
    start_background_scraper()
    yield
    # Shutdown: nothing to clean up

app = FastAPI(lifespan=lifespan)

# Allow Lovable (and any frontend) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your Lovable domain in production
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/state")
def get_current_state():
    """Returns the latest scraped donation data."""
    return get_state()

@app.get("/total")
def get_total():
    """Returns just the current donation total."""
    state = get_state()
    return {"total": state.get("current_total")}

@app.get("/donors")
def get_donors():
    """Returns the donor list."""
    state = get_state()
    return {"donors": state.get("Donors", [])}

@app.get("/health")
def health():
    return {"status": "ok"}