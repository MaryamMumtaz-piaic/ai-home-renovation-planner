"""Design concept agent (task.md section 23)."""

from __future__ import annotations

from app.models.renovation import DesignConcept, RenovationBrief
from app.services import openai_service


async def create_design_concept(brief: RenovationBrief) -> DesignConcept:
    """Generate the overall design concept for the brief's room."""
    return await openai_service.generate_design_concept(brief)
