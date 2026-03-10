from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scraper import get_state
from milestones import get_milestone_data

app = FastAPI(title="Donation Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Donor(BaseModel):
    name: str
    amount: Optional[float]
    time_ago: str
    message: Optional[str]


class DonationResponse(BaseModel):
    current_total: float
    next_target: int
    progress_percent: float
    remaining: float
    last_updated: Optional[str]
    donors: List[Donor]


@app.get("/api/donations", response_model=DonationResponse)
def get_donations():
    state = get_state()

    if state["current_total"] is None:
        raise HTTPException(
            status_code=503,
            detail="Data not yet available — scraper is initialising, try again shortly.",
        )

    milestone_data = get_milestone_data(state["current_total"])
    last_updated = state["last_updated"].strftime("%Y-%m-%dT%H:%M:%S") if state["last_updated"] else None

    return DonationResponse(
        current_total=milestone_data["current_total"],
        next_target=milestone_data["next_target"],
        progress_percent=milestone_data["progress_percent"],
        remaining=milestone_data["remaining"],
        last_updated=last_updated,
        donors=state.get("donors", []),
    )


@app.get("/health")
def health_check():
    state = get_state()
    return {
        "status": "ok",
        "has_data": state["current_total"] is not None,
        "last_error": state["last_error"],
    }