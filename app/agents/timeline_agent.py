"""Timeline agent (task.md section 26)."""

from __future__ import annotations

from app.models.renovation import RenovationBrief, Timeline
from app.services import openai_service


async def create_timeline(brief: RenovationBrief, execution_scope_hint: str = "") -> Timeline:
    """Generate a phased renovation timeline."""
    return await openai_service.generate_timeline(brief, execution_scope_hint)
