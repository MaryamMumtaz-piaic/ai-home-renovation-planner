"""Feedback and contact form submission endpoints (task.md section 56, 54)."""

from __future__ import annotations

from fastapi import APIRouter

from app.models.feedback import ContactSubmission, FeedbackSubmission
from app.services import json_store

router = APIRouter(prefix="/api", tags=["feedback"])


@router.post("/feedback")
async def submit_feedback(body: FeedbackSubmission) -> dict:
    json_store.append_json("feedback.json", body.model_dump(mode="json"))
    return {"message": "Feedback submitted"}


@router.post("/contact")
async def submit_contact(body: ContactSubmission) -> dict:
    json_store.append_json("contacts.json", body.model_dump(mode="json"))
    return {"message": "Message received."}
