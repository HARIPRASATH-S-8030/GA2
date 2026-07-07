from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# -----------------------------
# CHANGE THIS TO YOUR EMAIL
# -----------------------------
EMAIL = "24f1001287@ds.study.iitm.ac.in"

API_KEY = "ak_qx2ur0bd0iry2lqfg9fup303"

app = FastAPI(title="Analytics API")

# Allow browser-based grading
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or the exam domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
async def analytics(
    request: AnalyticsRequest,
    x_api_key: str = Header(None)
):
    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    events = request.events

    total_events = len(events)

    unique_users = len(set(event.user for event in events))

    revenue = 0.0

    user_totals = {}

    for event in events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] = (
                user_totals.get(event.user, 0) + event.amount
            )

    if user_totals:
        top_user = max(user_totals, key=user_totals.get)
    else:
        top_user = ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }