"""Shopping list agent (task.md section 25)."""

from __future__ import annotations

from app.models.renovation import (
    BudgetPlan,
    DesignConcept,
    MaterialPlan,
    RenovationBrief,
    ShoppingList,
)
from app.services import openai_service


async def create_shopping_list(
    brief: RenovationBrief,
    design_concept: DesignConcept,
    material_plan: MaterialPlan,
    budget: BudgetPlan,
) -> ShoppingList:
    """Generate the itemized shopping list grounded in design, materials, and budget."""
    return await openai_service.generate_shopping_list(
        brief, design_concept, material_plan, budget
    )
