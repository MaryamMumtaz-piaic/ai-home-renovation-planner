"""SavedProject model shape used for API validation of save/export endpoints.

Actual persistence is client-side via localStorage (task.md section 46).
This model defines the shape the frontend stores and may POST for validation
or PDF export purposes.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.renovation import RenovationBrief, RenovationPlan


class SavedProject(BaseModel):
    id: str
    name: str
    room_type: str
    style: str
    budget: float
    currency: str = "PKR"
    timeline: str
    progress: int = Field(default=0, ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    brief: Optional[RenovationBrief] = None
    plan: Optional[RenovationPlan] = None
