"""Critic agent (task.md section 28)."""

from __future__ import annotations

from app.models.renovation import CriticReview, RenovationPlan
from app.services import openai_service


async def review_plan(plan: RenovationPlan) -> CriticReview:
    """Run the critic pass over an assembled draft renovation plan."""
    return await openai_service.critique_renovation_plan(plan)
