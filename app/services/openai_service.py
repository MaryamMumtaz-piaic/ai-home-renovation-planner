"""Centralized OpenAI communication layer (task.md: "no OpenAI calls anywhere
else"). Every AI-backed capability the agents need is exposed here as one
async function that takes typed context, builds a grounded/minimal prompt,
calls the OpenAI Responses/Chat API with structured output, validates the
result against the relevant Pydantic model, retries once on validation
failure with a corrective follow-up, and either returns validated data or
raises AIGenerationError. Nothing here ever returns raw/unvalidated model
text.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from app.models.renovation import (
    BudgetPlan,
    BudgetScenario,
    CriticReview,
    DesignConcept,
    ExecutionPlan,
    MaterialComparison,
    MaterialPlan,
    RenovationBrief,
    RenovationPlan,
    ShoppingList,
    SpacePlan,
    Timeline,
)

load_dotenv()

_DEFAULT_MODEL = "gpt-4.1-mini"


class AIGenerationError(Exception):
    """Raised when the AI service cannot produce a valid, schema-conforming
    result after retrying once. Callers (agents/orchestrator) should let
    this propagate; the route layer converts it into an HTTP 502/500."""


class WhatIfResult(BaseModel):
    """Structured result of a free-form what-if scenario question against
    an existing renovation plan (kept here since it's AI-service-specific
    rather than part of the core domain models)."""

    budget_impact: str
    timeline_impact: str
    design_impact: str
    functionality_impact: str
    recommendation: str


class BudgetScenarioList(BaseModel):
    """Wrapper so the budget-scenario list can be requested as a single
    structured-output object (the API requires a top-level object, not a
    bare JSON array)."""

    scenarios: list[BudgetScenario]


_client: Optional[Any] = None


def _get_client() -> Any:
    """Lazily construct the AsyncOpenAI client so importing this module
    never requires OPENAI_API_KEY to be set (routes/tests must be able to
    import agent modules without a live key during this build phase)."""
    global _client
    if _client is None:
        from openai import AsyncOpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        _client = AsyncOpenAI(api_key=api_key)
    return _client


def _model_name() -> str:
    return os.environ.get("OPENAI_MODEL", _DEFAULT_MODEL)


# ---------------------------------------------------------------------------
# Shared guardrail instructions injected into every prompt (task.md section
# on safety/estimate framing).
# ---------------------------------------------------------------------------

SAFETY_RULES = (
    "Important rules you must follow:\n"
    "- You are a planning assistant, not a licensed architect, structural engineer, "
    "or contractor. Never claim architectural, engineering, or construction-approval "
    "status for any output.\n"
    "- Never guarantee exact costs or timelines. Frame all numbers as planning "
    "ESTIMATES only, clearly approximate.\n"
    "- Never fabricate specific live market prices from named retailers; give "
    "reasonable planning-level cost estimates instead.\n"
    "- Never give unsafe DIY instructions for electrical, gas, structural, "
    "plumbing, or roofing work. For any such work, explicitly recommend hiring a "
    "licensed professional instead of describing how to do it yourself.\n"
    "- Respond with strict JSON only, matching the requested schema field names "
    "exactly. No prose outside the JSON.\n"
)


async def _structured_call(
    *,
    system_prompt: str,
    user_prompt: str,
    response_model: type[BaseModel],
) -> BaseModel:
    """Call the model once with structured-output parsing, retry once with a
    corrective message on ValidationError, else raise AIGenerationError."""
    try:
        client = _get_client()
    except Exception as exc:  # noqa: BLE001 - e.g. missing OPENAI_API_KEY
        raise AIGenerationError(
            f"OpenAI client is not configured (is OPENAI_API_KEY set?): {exc}"
        ) from exc
    model = _model_name()

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    last_error: Optional[Exception] = None

    for attempt in range(2):
        try:
            completion = await client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_model,
            )
            parsed = completion.choices[0].message.parsed
            if parsed is None:
                raise AIGenerationError(
                    f"Model returned no parsable content for {response_model.__name__}."
                )
            return parsed
        except ValidationError as exc:
            last_error = exc
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Your previous JSON response failed schema validation with "
                        f"this error:\n{exc}\n\n"
                        "Return a corrected JSON object that strictly matches the "
                        "required schema field names and types. JSON only."
                    ),
                }
            )
            continue
        except Exception as exc:  # noqa: BLE001 - convert any SDK/parse failure
            # Some SDK versions raise a plain Exception wrapping a pydantic
            # validation error for refusals/malformed content; treat as
            # retryable on first attempt, fatal on second.
            last_error = exc
            if attempt == 0:
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Your previous response could not be parsed as valid "
                            f"JSON matching the schema ({exc}). Return a corrected "
                            "JSON object only, matching the required schema."
                        ),
                    }
                )
                continue
            break

    raise AIGenerationError(
        f"Failed to generate a valid {response_model.__name__} after retry: {last_error}"
    )


def _brief_context(brief: RenovationBrief) -> dict[str, Any]:
    """Extract only the fields relevant for grounding a prompt, never the
    entire brief dump — keeps prompts small and focused (task.md: don't
    dump entire datasets/objects into prompts)."""
    dims = brief.current_space.dimensions
    dims_str = (
        "unknown/approximate"
        if dims.unknown or not dims.length
        else f"{dims.length}x{dims.width} {dims.unit} (height {dims.height or 'n/a'} {dims.unit})"
    )
    keep_furniture = [
        f"{item.name} ({item.action})" for item in brief.current_space.existing_furniture
    ]
    return {
        "room_type": brief.room_type,
        "dimensions": dims_str,
        "current_condition": brief.current_space.current_condition,
        "existing_flooring": brief.current_space.existing_flooring,
        "existing_walls": brief.current_space.existing_walls,
        "existing_lighting": brief.current_space.existing_lighting,
        "structural_constraints": brief.current_space.structural_constraints,
        "goals": brief.goals,
        "goal_description": brief.goal_description,
        "style": brief.style.style,
        "style_custom_description": brief.style.custom_description,
        "colors_wanted": brief.colors.colors_wanted,
        "colors_avoided": brief.colors.colors_avoided,
        "color_notes": brief.colors.custom_notes,
        "budget_tier": brief.budget.tier,
        "max_budget": brief.budget.max_budget,
        "currency": brief.budget.currency,
        "material_preferences": [
            {"category": m.category, "preference": m.preference, "notes": m.custom_notes}
            for m in brief.materials
        ],
        "existing_furniture_to_keep_or_replace": keep_furniture,
        "target_days": brief.timeline.target_days,
        "timeline_flexible": brief.timeline.flexible,
        "timeline_notes": brief.timeline.notes,
    }


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, default=str)


# ---------------------------------------------------------------------------
# Public generation functions — one per agent need.
# ---------------------------------------------------------------------------


async def generate_design_concept(brief: RenovationBrief) -> DesignConcept:
    system = (
        "You are an interior design concept generator for a home renovation "
        "planning tool. Produce a cohesive design concept grounded strictly in "
        "the user's stated room, goals, style, and colors.\n" + SAFETY_RULES
    )
    user = (
        "Generate a DesignConcept JSON object with fields: concept_name, "
        "design_summary, style, color_palette (list[str]), materials (list[str]), "
        "furniture_direction (list[str]), lighting_direction (list[str]), "
        "decor_direction (list[str]), design_priorities (list[str]).\n\n"
        f"Brief context:\n{_json(_brief_context(brief))}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=DesignConcept
    )  # type: ignore[return-value]


_ROOM_HINTS = {
    "kitchen": "Focus on cabinetry, countertops, storage, lighting, appliances, and workflow.",
    "bedroom": "Focus on bed placement, storage, lighting, comfort, color, and privacy.",
    "bathroom": "Focus on fixtures, storage, lighting, surfaces, and maintenance.",
    "living_room": "Focus on seating, entertainment, lighting, circulation, storage, and decor.",
}


async def generate_space_plan(
    brief: RenovationBrief, room_hint: Optional[str] = None
) -> SpacePlan:
    hint = room_hint or _ROOM_HINTS.get(brief.room_type, "")
    system = (
        "You are a space-planning assistant for a home renovation tool. You are "
        "not a licensed architect and this is not a construction-grade floor "
        "plan — it is a planning concept based on approximate, user-provided "
        f"information. {hint}\n" + SAFETY_RULES
    )
    user = (
        "Generate a SpacePlan JSON object with fields: dimensions_summary, "
        "zones (list of {name, purpose, notes}), furniture_strategy (list[str]), "
        "storage_strategy (list[str]), movement_flow (str), lighting_zones "
        "(list[str]), is_approximate (bool), planning_note (str).\n\n"
        f"Brief context:\n{_json(_brief_context(brief))}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=SpacePlan
    )  # type: ignore[return-value]


async def generate_material_plan(brief: RenovationBrief) -> MaterialPlan:
    system = (
        "You are a materials advisor for a home renovation planning tool. "
        "Recommend materials grounded in the user's room type, style, color "
        "preferences, and stated per-category material preferences.\n" + SAFETY_RULES
    )
    user = (
        "Generate a MaterialPlan JSON object with fields: recommendations "
        "(list of MaterialRecommendation: category, material_name, why, "
        "cost_level [Low/Medium/High], maintenance [Low/Medium/High], style_fit, "
        "alternative, trade_off) and comparisons (list of MaterialComparison: "
        "category, options [list of {name, cost, maintenance, style_fit, notes}], "
        "ai_recommendation). Cover the categories the user gave preferences for, "
        "plus flooring/wall finish/paint if relevant to the room.\n\n"
        f"Brief context:\n{_json(_brief_context(brief))}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=MaterialPlan
    )  # type: ignore[return-value]


async def generate_budget(
    brief: RenovationBrief, design_concept: DesignConcept, material_plan: MaterialPlan
) -> BudgetPlan:
    system = (
        "You are a budgeting assistant for a home renovation planning tool. "
        "Produce a realistic budget breakdown that fits within the user's stated "
        "maximum budget where feasible, and flag risk if it does not.\n" + SAFETY_RULES
    )
    material_cost_levels = [
        {"category": r.category, "material": r.material_name, "cost_level": r.cost_level}
        for r in material_plan.recommendations
    ]
    user = (
        "Generate a BudgetPlan JSON object with fields: currency, total_estimate, "
        "categories (list of {name, amount, percentage} — percentages must sum to "
        "~100), contingency, savings_opportunities (list[str]), budget_risk "
        "[Low/Medium/High], assumptions (list[str]), disclaimer.\n\n"
        f"Room/budget context:\n{_json(_brief_context(brief))}\n\n"
        f"Design concept summary: {design_concept.design_summary}\n"
        f"Design priorities: {design_concept.design_priorities}\n\n"
        f"Material cost levels (not full details): {_json(material_cost_levels)}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=BudgetPlan
    )  # type: ignore[return-value]


async def generate_shopping_list(
    brief: RenovationBrief,
    design_concept: DesignConcept,
    material_plan: MaterialPlan,
    budget: BudgetPlan,
) -> ShoppingList:
    system = (
        "You are a shopping-list assistant for a home renovation planning tool. "
        "Produce a practical, prioritized shopping list consistent with the "
        "design concept, chosen materials, and budget.\n" + SAFETY_RULES
    )
    user = (
        "Generate a ShoppingList JSON object with field items (list of "
        "ShoppingItem: name, category, quantity, estimated_cost, priority "
        "[essential/recommended/optional], alternative, notes, checked=false). "
        "Keep the total of estimated_cost roughly consistent with the budget's "
        "total_estimate.\n\n"
        f"Room: {brief.room_type}, style: {design_concept.style}\n"
        f"Design materials: {design_concept.materials}\n"
        f"Material recommendations: "
        f"{_json([r.material_name for r in material_plan.recommendations])}\n"
        f"Budget total: {budget.total_estimate} {budget.currency}, "
        f"categories: {_json([c.name for c in budget.categories])}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=ShoppingList
    )  # type: ignore[return-value]


async def generate_timeline(
    brief: RenovationBrief, execution_scope_hint: str = ""
) -> Timeline:
    system = (
        "You are a renovation timeline planner. Produce a realistic phased "
        "timeline as a planning estimate, not a guaranteed schedule.\n" + SAFETY_RULES
    )
    user = (
        "Generate a Timeline JSON object with fields: total_estimated_days (str), "
        "phases (list of TimelinePhase: phase_number, name, duration_days, "
        "description, depends_on (list[str] of phase names), "
        "can_run_in_parallel), critical_path (list[str] of phase names), "
        "disclaimer.\n\n"
        f"Room: {brief.room_type}\n"
        f"Goals: {brief.goals} / {brief.goal_description}\n"
        f"User target days: {brief.timeline.target_days} "
        f"(flexible: {brief.timeline.flexible}), notes: {brief.timeline.notes}\n"
        f"Scope hint: {execution_scope_hint}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=Timeline
    )  # type: ignore[return-value]


async def generate_execution_plan(
    brief: RenovationBrief, design_concept: DesignConcept, timeline: Timeline
) -> ExecutionPlan:
    system = (
        "You are an execution-plan assistant for a home renovation tool. Break "
        "the renovation into concrete tasks across stages. For any electrical, "
        "gas, structural, plumbing, or roofing task, set requires_professional "
        "true and add a recommended_skill_note pointing to a licensed "
        "professional — never give DIY instructions for that work.\n" + SAFETY_RULES
    )
    user = (
        "Generate an ExecutionPlan JSON object with fields: tasks (list of "
        "ExecutionTask: task, dependencies (list[str] of task names), materials "
        "(list[str]), requires_professional (bool), recommended_skill_note, "
        "stage [before_renovation/during_renovation/installation/styling/"
        "final_inspection], status='not_started'), preparation_checklist "
        "(list[str]), final_inspection_checklist (list[str]).\n\n"
        f"Room: {brief.room_type}\n"
        f"Design summary: {design_concept.design_summary}\n"
        f"Design priorities: {design_concept.design_priorities}\n"
        f"Timeline phases: {_json([p.name for p in timeline.phases])}\n"
        f"Structural constraints noted by user: {brief.current_space.structural_constraints}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=ExecutionPlan
    )  # type: ignore[return-value]


async def critique_renovation_plan(plan: RenovationPlan) -> CriticReview:
    system = (
        "You are a quality-control critic reviewing a generated renovation "
        "plan for internal consistency, budget sanity, timeline sanity, and "
        "safety. You do not regenerate the plan, only review it.\n" + SAFETY_RULES
    )
    summary = {
        "room_type": plan.style,
        "estimated_budget": plan.estimated_budget,
        "currency": plan.currency,
        "estimated_timeline": plan.estimated_timeline,
        "budget_total_estimate": plan.budget.total_estimate,
        "budget_categories": [
            {"name": c.name, "percentage": c.percentage} for c in plan.budget.categories
        ],
        "timeline_total_days": plan.timeline.total_estimated_days,
        "shopping_items_total_cost": sum(i.estimated_cost for i in plan.shopping_list.items),
        "execution_tasks_requiring_professional": [
            t.task for t in plan.execution_plan.tasks if t.requires_professional
        ],
    }
    user = (
        "Review this renovation plan summary and return a CriticReview JSON "
        "object with fields: issues (list[str] — concrete problems that should "
        "block approval), warnings (list[str] — things worth flagging but not "
        "blocking), improvements (list[str]), approved (bool — false only if "
        "issues is non-empty or something is materially wrong).\n\n"
        f"Plan summary:\n{_json(summary)}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=CriticReview
    )  # type: ignore[return-value]


async def adapt_renovation_plan(
    plan: RenovationPlan, option: str, notes: Optional[str]
) -> RenovationPlan:
    system = (
        "You adapt an existing renovation plan according to a single requested "
        "adaptation option. Change ONLY what that option implies; preserve every "
        "other field, structure, and value from the original plan exactly as "
        "given. Return the FULL RenovationPlan JSON object (all fields), not a "
        "diff.\n" + SAFETY_RULES
    )
    user = (
        f"Adaptation option: {option}\n"
        f"Additional user notes: {notes or 'none'}\n\n"
        "Original plan (full JSON):\n"
        f"{plan.model_dump_json()}\n\n"
        "Return the adapted RenovationPlan as a full JSON object matching the "
        "same schema, with only the fields implied by the adaptation option "
        "changed."
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=RenovationPlan
    )  # type: ignore[return-value]


async def run_what_if_scenario(plan: RenovationPlan, question: str) -> dict:
    system = (
        "You answer a free-form what-if question about an existing renovation "
        "plan, without modifying the plan itself. Give grounded, plan-consistent "
        "impact analysis.\n" + SAFETY_RULES
    )
    summary = {
        "room_type": plan.style,
        "concept_name": plan.concept_name,
        "estimated_budget": plan.estimated_budget,
        "currency": plan.currency,
        "estimated_timeline": plan.estimated_timeline,
        "budget_categories": [
            {"name": c.name, "amount": c.amount} for c in plan.budget.categories
        ],
        "timeline_phases": [p.name for p in plan.timeline.phases],
    }
    user = (
        "Generate a WhatIfResult JSON object with fields: budget_impact, "
        "timeline_impact, design_impact, functionality_impact, recommendation "
        "(all strings).\n\n"
        f"Plan summary:\n{_json(summary)}\n\n"
        f"User question: {question}"
    )
    result = await _structured_call(
        system_prompt=system, user_prompt=user, response_model=WhatIfResult
    )
    return result.model_dump()  # type: ignore[union-attr]


async def generate_budget_scenarios(
    brief: RenovationBrief, base_budget: BudgetPlan
) -> list[BudgetScenario]:
    system = (
        "You produce a three-way budget comparison (budget / balanced / "
        "premium tiers) for a home renovation, grounded in the user's room and "
        "base budget plan.\n" + SAFETY_RULES
    )
    user = (
        "Generate a BudgetScenarioList JSON object with field scenarios: a list "
        "of exactly 3 BudgetScenario objects (tier=budget/balanced/premium, "
        "label, estimated_total, description, changes (list[str])), each "
        "distinct in scope/cost relative to the base plan.\n\n"
        f"Room: {brief.room_type}, budget tier: {brief.budget.tier}, "
        f"max budget: {brief.budget.max_budget} {brief.budget.currency}\n"
        f"Base total estimate: {base_budget.total_estimate} {base_budget.currency}\n"
        f"Base categories: {_json([c.name for c in base_budget.categories])}"
    )
    result = await _structured_call(
        system_prompt=system, user_prompt=user, response_model=BudgetScenarioList
    )
    return result.scenarios  # type: ignore[union-attr]


async def generate_material_comparison(
    category: str,
    current_material: Optional[str],
    style: Optional[str],
    budget_tier: Optional[str],
    room_type: Optional[str],
) -> MaterialComparison:
    system = (
        "You compare material alternatives within one category for a home "
        "renovation planning tool.\n" + SAFETY_RULES
    )
    user = (
        "Generate a MaterialComparison JSON object with fields: category, "
        "options (list of MaterialComparisonOption: name, cost [Low/Medium/High], "
        "maintenance [Low/Medium/High], style_fit, notes), ai_recommendation "
        "(str). Include the current material as one option if given, plus 2-3 "
        "sensible alternatives.\n\n"
        f"Category: {category}\n"
        f"Current material: {current_material or 'none specified'}\n"
        f"Style: {style or 'unspecified'}\n"
        f"Budget tier: {budget_tier or 'unspecified'}\n"
        f"Room type: {room_type or 'unspecified'}"
    )
    return await _structured_call(
        system_prompt=system, user_prompt=user, response_model=MaterialComparison
    )  # type: ignore[return-value]
