"""Feedback and contact form models (app/routes/feedback.py)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class FeedbackSubmission(BaseModel):
    """POST /api/feedback"""

    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=5000)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


class ContactSubmission(BaseModel):
    """POST /api/contact"""

    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=5000)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
