"""Execution plan agent (task.md section 27)."""

from __future__ import annotations

from app.models.renovation import DesignConcept, ExecutionPlan, RenovationBrief, Timeline
from app.services import openai_service


async def create_execution_plan(
    brief: RenovationBrief, design_concept: DesignConcept, timeline: Timeline
) -> ExecutionPlan:
    """Generate the task-by-task execution plan grounded in the design concept and timeline."""
    return await openai_service.generate_execution_plan(brief, design_concept, timeline)
