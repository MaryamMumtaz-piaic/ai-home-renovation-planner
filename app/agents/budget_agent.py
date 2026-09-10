"""Budget planning agent (task.md section 24 / 35).

Applies a local safety net: if the AI's category percentages don't sum to
~100%, rescale them proportionally locally rather than re-calling the AI
(keeps AI calls minimal per section 62)."""

from __future__ import annotations

from app.models.renovation import (
    BudgetPlan,
    BudgetScenario,
    DesignConcept,
    MaterialPlan,
    RenovationBrief,
)
from app.services import openai_service
from app.utils.validation import is_allocation_valid


def _rescale_categories(budget: BudgetPlan) -> BudgetPlan:
    """Proportionally rescale category percentages (and amounts, to stay
    consistent) to sum to 100% if the model's output drifted."""
    if not budget.categories or is_allocation_valid(budget.categories):
        return budget

    total_pct = sum(c.percentage for c in budget.categories)
    if total_pct <= 0:
        return budget

    scale = 100.0 / total_pct
    rescaled = []
    for cat in budget.categories:
        new_pct = round(cat.percentage * scale, 2)
        new_amount = round(budget.total_estimate * (new_pct / 100.0), 2)
        rescaled.append(cat.model_copy(update={"percentage": new_pct, "amount": new_amount}))

    return budget.model_copy(update={"categories": rescaled})


async def create_budget(
    brief: RenovationBrief, design_concept: DesignConcept, material_plan: MaterialPlan
) -> BudgetPlan:
    """Generate the budget plan, then locally validate/rescale allocations."""
    budget = await openai_service.generate_budget(brief, design_concept, material_plan)
    return _rescale_categories(budget)


async def create_budget_scenarios(
    brief: RenovationBrief, base_budget: BudgetPlan
) -> list[BudgetScenario]:
    """Generate the Budget/Balanced/Premium comparison scenarios."""
    return await openai_service.generate_budget_scenarios(brief, base_budget)
