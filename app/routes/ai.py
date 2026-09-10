"""Core AI endpoints (task.md section 56, 29).

Route handlers stay thin: build/validate input, delegate to the agent
layer (app.agents.*), and translate agent-layer errors into HTTP errors.
No OpenAI calls happen directly in this file.

Design choice -- POST /api/ai/budget: the budget_agent.create_budget()
contract takes (brief, design_concept, material_plan), and those building
blocks aren't exposed as independently callable functions in the agent
contract given to this layer. Rather than duplicate orchestration logic
here, this endpoint runs the full orchestrator pipeline via
generate_renovation_plan(brief) and returns only the resulting `.budget`
field. This is a bit more expensive than a "budget-only" call would be,
but keeps the AI pipeline logic centralized in the orchestrator instead of
partially re-implemented in the route layer.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.agents import material_agent, orchestrator, space_planning_agent
from app.models.ai_request import (
    AdaptPlanRequest,
    BudgetRequest,
    CreatePlanRequest,
    MaterialAlternativesRequest,
    SpacePlanRequest,
    WhatIfRequest,
)
from app.models.renovation import BudgetPlan, MaterialComparison, RenovationPlan, SpacePlan
from app.services.openai_service import AIGenerationError

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/create-plan", response_model=RenovationPlan)
async def create_plan(body: CreatePlanRequest) -> RenovationPlan:
    try:
        return await orchestrator.generate_renovation_plan(body.brief)
    except AIGenerationError:
        raise HTTPException(status_code=502, detail="AI generation failed, please try again.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/adapt-plan", response_model=RenovationPlan)
async def adapt_plan(body: AdaptPlanRequest) -> RenovationPlan:
    try:
        return await orchestrator.adapt_plan(body.plan, body.option, body.notes)
    except AIGenerationError:
        raise HTTPException(status_code=502, detail="AI generation failed, please try again.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/what-if")
async def what_if(body: WhatIfRequest) -> dict:
    try:
        return await orchestrator.run_what_if(body.plan, body.question)
    except AIGenerationError:
        raise HTTPException(status_code=502, detail="AI generation failed, please try again.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/material-alternatives", response_model=MaterialComparison)
async def material_alternatives(body: MaterialAlternativesRequest) -> MaterialComparison:
    try:
        return await material_agent.compare_materials(
            body.category,
            body.current_material,
            body.style,
            body.budget_tier,
            body.room_type,
        )
    except AIGenerationError:
        raise HTTPException(status_code=502, detail="AI generation failed, please try again.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/space-plan", response_model=SpacePlan)
async def space_plan(body: SpacePlanRequest) -> SpacePlan:
    try:
        return await space_planning_agent.create_space_plan(body.brief)
    except AIGenerationError:
        raise HTTPException(status_code=502, detail="AI generation failed, please try again.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/budget", response_model=BudgetPlan)
async def budget(body: BudgetRequest) -> BudgetPlan:
    try:
        plan = await orchestrator.generate_renovation_plan(body.brief)
        return plan.budget
    except AIGenerationError:
        raise HTTPException(status_code=502, detail="AI generation failed, please try again.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
