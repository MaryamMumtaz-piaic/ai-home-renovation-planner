"""Material planning agent (task.md section 21 / 36)."""

from __future__ import annotations

from typing import Optional

from app.models.renovation import MaterialComparison, MaterialPlan, RenovationBrief
from app.services import openai_service


async def create_material_plan(brief: RenovationBrief) -> MaterialPlan:
    """Generate material recommendations and comparisons for the brief."""
    return await openai_service.generate_material_plan(brief)


async def compare_materials(
    category: str,
    current_material: Optional[str],
    style: Optional[str],
    budget_tier: Optional[str],
    room_type: Optional[str],
) -> MaterialComparison:
    """Generate a standalone material comparison for one category."""
    return await openai_service.generate_material_comparison(
        category=category,
        current_material=current_material,
        style=style,
        budget_tier=budget_tier,
        room_type=room_type,
    )
