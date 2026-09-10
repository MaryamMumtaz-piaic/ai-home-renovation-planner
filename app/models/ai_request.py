"""Request models for the AI endpoints (app/routes/ai.py, section 56)."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from app.models.renovation import (
    AdaptationOption,
    RenovationBrief,
    RenovationPlan,
)


class CreatePlanRequest(BaseModel):
    """POST /api/ai/create-plan"""

    brief: RenovationBrief


class AdaptPlanRequest(BaseModel):
    """POST /api/ai/adapt-plan — adapt an existing plan using one of the
    predefined adaptation options from section 41."""

    plan: RenovationPlan
    option: AdaptationOption
    notes: Optional[str] = None


class WhatIfRequest(BaseModel):
    """POST /api/ai/what-if — free-form scenario question against a plan."""

    plan: RenovationPlan
    question: str = Field(min_length=1)


class MaterialAlternativesRequest(BaseModel):
    """POST /api/ai/material-alternatives"""

    category: str
    current_material: Optional[str] = None
    style: Optional[str] = None
    budget_tier: Optional[str] = None
    room_type: Optional[str] = None


class SpacePlanRequest(BaseModel):
    """POST /api/ai/space-plan"""

    brief: RenovationBrief


class BudgetRequest(BaseModel):
    """POST /api/ai/budget"""

    brief: RenovationBrief
