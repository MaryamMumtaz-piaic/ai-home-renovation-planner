"""Main pipeline coordinator (task.md section 29/58).

Runs the full agent pipeline respecting real data dependencies, running
independent agents concurrently, assembles the draft RenovationPlan, runs
the critic, and does one targeted revision pass only for the agents
implicated by the critic's findings (never a blind full re-run)."""

from __future__ import annotations

import asyncio
from typing import Optional

from app.agents import (
    budget_agent,
    critic_agent,
    design_agent,
    execution_agent,
    material_agent,
    shopping_agent,
    space_planning_agent,
    timeline_agent,
)
from app.models.renovation import AdaptationOption, RenovationBrief, RenovationPlan
from app.services import openai_service
from app.utils.scoring import compute_budget_risk, compute_design_match
from app.utils.validation import is_brief_complete, missing_brief_fields

_STRUCTURAL_GOALS_REQUIRING_PRO_WARNING = {
    "kitchen",
    "bathroom",
}

_PROFESSIONAL_CONSULTATION_WARNING = (
    "Any electrical, gas, plumbing, or structural work identified in this plan "
    "should be performed or verified by a licensed professional — this plan is "
    "a planning aid, not an engineering or construction approval."
)


async def generate_renovation_plan(brief: RenovationBrief) -> RenovationPlan:
    """Run the full agent pipeline and return the final, critic-approved plan."""
    if not is_brief_complete(brief):
        missing = ", ".join(missing_brief_fields(brief))
        raise ValueError(f"Renovation brief is incomplete; missing: {missing}")

    # Stage 1: design concept, space plan, and material plan only depend on
    # the brief, so they can run concurrently.
    design_concept, space_plan, material_plan = await asyncio.gather(
        design_agent.create_design_concept(brief),
        space_planning_agent.create_space_plan(brief),
        material_agent.create_material_plan(brief),
    )

    # Stage 2: budget needs design_concept + material_plan; timeline only
    # needs the brief, so it can run in parallel with budget.
    budget, timeline = await asyncio.gather(
        budget_agent.create_budget(brief, design_concept, material_plan),
        timeline_agent.create_timeline(brief),
    )

    # Stage 3: shopping list needs budget; execution plan needs
    # design_concept + timeline. Independent of each other, run concurrently.
    shopping_list, execution_plan = await asyncio.gather(
        shopping_agent.create_shopping_list(brief, design_concept, material_plan, budget),
        execution_agent.create_execution_plan(brief, design_concept, timeline),
    )

    alternatives = await budget_agent.create_budget_scenarios(brief, budget)

    design_match = compute_design_match(brief)
    budget_risk = compute_budget_risk(
        budget.total_estimate, brief.budget.max_budget, budget.categories
    )

    plan = RenovationPlan(
        concept_name=design_concept.concept_name,
        design_summary=design_concept.design_summary,
        style=design_concept.style,
        estimated_budget=budget.total_estimate,
        currency=budget.currency,
        estimated_timeline=timeline.total_estimated_days,
        design_match=design_match,
        budget_risk=budget_risk,
        design_concept=design_concept,
        space_plan=space_plan,
        budget=budget,
        materials=material_plan,
        shopping_list=shopping_list,
        timeline=timeline,
        execution_plan=execution_plan,
        alternatives=alternatives,
        ai_recommendations=[],
        assumptions=list(budget.assumptions),
        warnings=[],
    )

    # Critic pass + one targeted revision.
    review = await critic_agent.review_plan(plan)

    if not review.approved or review.issues:
        plan = await _targeted_revision(brief, plan, review.issues)
        # Note: intentionally do not re-run the critic again — spec calls
        # for a single revision pass, not an iterative loop.

    warnings = list(review.warnings)
    if _implies_professional_work(brief):
        warnings.append(_PROFESSIONAL_CONSULTATION_WARNING)
    plan = plan.model_copy(
        update={
            "warnings": warnings,
            "ai_recommendations": review.improvements,
        }
    )

    return plan


def _implies_professional_work(brief: RenovationBrief) -> bool:
    if brief.room_type in _STRUCTURAL_GOALS_REQUIRING_PRO_WARNING:
        return True
    if brief.current_space.structural_constraints:
        return True
    return False


async def _targeted_revision(
    brief: RenovationBrief, plan: RenovationPlan, issues: list[str]
) -> RenovationPlan:
    """Re-run only the agents implicated by the critic's issues, per
    section 29 ("do not run every agent unnecessarily")."""
    issue_text = " ".join(issues).lower()

    touches_budget = any(
        kw in issue_text for kw in ("budget", "cost", "price", "allocation", "contingency")
    )
    touches_timeline = any(
        kw in issue_text for kw in ("timeline", "schedule", "duration", "phase")
    )
    touches_shopping = "shopping" in issue_text or "item" in issue_text
    touches_execution = any(
        kw in issue_text for kw in ("execution", "task", "professional", "safety")
    )

    budget = plan.budget
    shopping_list = plan.shopping_list
    timeline = plan.timeline
    execution_plan = plan.execution_plan

    if touches_budget:
        budget = await budget_agent.create_budget(brief, plan.design_concept, plan.materials)
        shopping_list = await shopping_agent.create_shopping_list(
            brief, plan.design_concept, plan.materials, budget
        )
    elif touches_shopping:
        shopping_list = await shopping_agent.create_shopping_list(
            brief, plan.design_concept, plan.materials, budget
        )

    if touches_timeline:
        timeline = await timeline_agent.create_timeline(brief)
        execution_plan = await execution_agent.create_execution_plan(
            brief, plan.design_concept, timeline
        )
    elif touches_execution:
        execution_plan = await execution_agent.create_execution_plan(
            brief, plan.design_concept, timeline
        )

    budget_risk = compute_budget_risk(budget.total_estimate, brief.budget.max_budget, budget.categories)

    return plan.model_copy(
        update={
            "budget": budget,
            "shopping_list": shopping_list,
            "timeline": timeline,
            "execution_plan": execution_plan,
            "estimated_budget": budget.total_estimate,
            "estimated_timeline": timeline.total_estimated_days,
            "budget_risk": budget_risk,
        }
    )


async def adapt_plan(
    plan: RenovationPlan, option: AdaptationOption, notes: Optional[str] = None
) -> RenovationPlan:
    """Adapt an existing plan using one predefined adaptation option."""
    return await openai_service.adapt_renovation_plan(plan, option, notes)


async def run_what_if(plan: RenovationPlan, question: str) -> dict:
    """Answer a free-form what-if question against an existing plan."""
    return await openai_service.run_what_if_scenario(plan, question)
