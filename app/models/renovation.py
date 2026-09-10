"""
Core domain models for the renovation planning flow.

Contains:
- Input models built from the multi-step planner (RenovationBrief and its parts)
- Structured output models returned by each AI agent (DesignConcept, SpacePlan, etc.)
- The aggregate RenovationPlan model returned to the frontend as the final result.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Enums / Literal types
# ---------------------------------------------------------------------------

RoomType = Literal[
    "living_room",
    "bedroom",
    "kitchen",
    "bathroom",
    "dining_room",
    "home_office",
    "entryway",
    "balcony",
    "outdoor_area",
    "nursery",
    "guest_room",
    "basement",
    "other",
]

RenovationGoal = Literal[
    "modernize",
    "brighten",
    "increase_storage",
    "improve_functionality",
    "feel_larger",
    "luxury_look",
    "reduce_maintenance",
    "improve_lighting",
    "improve_organization",
    "increase_comfort",
    "prepare_for_resale",
    "complete_makeover",
    "partial_renovation",
]

DesignStyle = Literal[
    "modern",
    "minimalist",
    "scandinavian",
    "industrial",
    "japandi",
    "traditional",
    "contemporary",
    "luxury",
    "bohemian",
    "mid_century_modern",
    "rustic",
    "coastal",
    "classic",
    "eclectic",
    "custom",
]

ColorPreferenceOption = Literal[
    "warm_neutrals",
    "cool_neutrals",
    "earth_tones",
    "white_and_beige",
    "black_and_white",
    "green",
    "blue",
    "terracotta",
    "natural_wood",
    "custom",
]

BudgetTier = Literal["low", "moderate", "premium", "luxury", "custom"]

DimensionUnit = Literal["ft", "m"]

MaterialCategoryPreference = Literal[
    "flooring",
    "wall_finish",
    "paint",
    "countertops",
    "cabinet_materials",
    "hardware",
    "lighting",
    "furniture_materials",
]

MaterialPreferenceOption = Literal[
    "natural",
    "budget_friendly",
    "premium",
    "low_maintenance",
    "durable",
    "eco_conscious",
    "easy_to_clean",
    "custom",
]

FurnitureAction = Literal["keep", "replace", "unsure"]

CostLevel = Literal["Low", "Medium", "High"]
RiskLevel = Literal["Low", "Medium", "High"]
ConfidenceLevel = Literal["Low", "Medium", "High"]
Priority = Literal["essential", "recommended", "optional"]
TaskStatus = Literal["not_started", "in_progress", "completed"]

AdaptationOption = Literal[
    "make_cheaper",
    "make_luxurious",
    "finish_faster",
    "more_sustainable",
    "make_minimalist",
    "add_storage",
    "keep_existing_furniture",
    "reduce_construction",
    "change_color_palette",
]

BudgetScenarioTier = Literal["budget", "balanced", "premium"]


# ---------------------------------------------------------------------------
# Step input models (brief construction)
# ---------------------------------------------------------------------------


class RoomDimensions(BaseModel):
    """Room dimensions as entered in Step 2. If unknown is True, numeric
    fields may be omitted and downstream planning treats them as approximate."""

    length: Optional[float] = Field(default=None, ge=0)
    width: Optional[float] = Field(default=None, ge=0)
    height: Optional[float] = Field(default=None, ge=0)
    unit: DimensionUnit = "ft"
    unknown: bool = False


class ExistingFurnitureItem(BaseModel):
    name: str
    action: FurnitureAction = "unsure"
    notes: Optional[str] = None


class CurrentSpace(BaseModel):
    """Step 2: description of the room as it currently exists."""

    dimensions: RoomDimensions = Field(default_factory=RoomDimensions)
    current_condition: Optional[str] = None
    existing_furniture: list[ExistingFurnitureItem] = Field(default_factory=list)
    existing_flooring: Optional[str] = None
    existing_walls: Optional[str] = None
    existing_lighting: Optional[str] = None
    windows_doors: Optional[str] = None
    structural_constraints: Optional[str] = None


class DesignStylePreference(BaseModel):
    """Step 4: design style, optionally with free-form custom description."""

    style: DesignStyle = "modern"
    custom_description: Optional[str] = None


class ColorPreference(BaseModel):
    """Step 5: colors wanted vs. avoided."""

    colors_wanted: list[ColorPreferenceOption] = Field(default_factory=list)
    colors_avoided: list[ColorPreferenceOption] = Field(default_factory=list)
    custom_notes: Optional[str] = None


class BudgetPreference(BaseModel):
    """Step 6: budget tier and target figure."""

    tier: BudgetTier = "moderate"
    currency: str = "PKR"
    max_budget: float = Field(ge=0)


class MaterialPreference(BaseModel):
    """Step 7: per-category material preference, e.g. flooring -> natural."""

    category: MaterialCategoryPreference
    preference: MaterialPreferenceOption = "budget_friendly"
    custom_notes: Optional[str] = None


class TimelinePreference(BaseModel):
    """Step 8: desired timeline for the renovation."""

    target_days: Optional[int] = Field(default=None, ge=1)
    flexible: bool = True
    notes: Optional[str] = None


class RenovationBrief(BaseModel):
    """Aggregate of every step's input. Routes build this from form/JSON
    input and pass it to the orchestrator to produce a RenovationPlan."""

    room_type: RoomType
    current_space: CurrentSpace = Field(default_factory=CurrentSpace)
    goals: list[RenovationGoal] = Field(default_factory=list)
    goal_description: Optional[str] = None
    style: DesignStylePreference = Field(default_factory=DesignStylePreference)
    colors: ColorPreference = Field(default_factory=ColorPreference)
    budget: BudgetPreference
    materials: list[MaterialPreference] = Field(default_factory=list)
    timeline: TimelinePreference = Field(default_factory=TimelinePreference)


# ---------------------------------------------------------------------------
# Agent structured output models (section 23-28)
# ---------------------------------------------------------------------------


class DesignConcept(BaseModel):
    """Output of app/agents/design_agent.py (section 23)."""

    concept_name: str
    design_summary: str
    style: str
    color_palette: list[str] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)
    furniture_direction: list[str] = Field(default_factory=list)
    lighting_direction: list[str] = Field(default_factory=list)
    decor_direction: list[str] = Field(default_factory=list)
    design_priorities: list[str] = Field(default_factory=list)


class SpaceZone(BaseModel):
    name: str
    purpose: str
    notes: Optional[str] = None


class SpacePlan(BaseModel):
    """Output of app/agents/space_planning_agent.py (section 22)."""

    dimensions_summary: str
    zones: list[SpaceZone] = Field(default_factory=list)
    furniture_strategy: list[str] = Field(default_factory=list)
    storage_strategy: list[str] = Field(default_factory=list)
    movement_flow: str
    lighting_zones: list[str] = Field(default_factory=list)
    is_approximate: bool = True
    planning_note: str = (
        "Planning based on user-provided approximate information. "
        "This is a planning concept, not a construction-grade floor plan."
    )


class BudgetCategory(BaseModel):
    name: str
    amount: float
    percentage: float


class BudgetPlan(BaseModel):
    """Output of app/agents/budget_agent.py (section 24)."""

    currency: str
    total_estimate: float
    categories: list[BudgetCategory] = Field(default_factory=list)
    contingency: float = 0
    savings_opportunities: list[str] = Field(default_factory=list)
    budget_risk: RiskLevel = "Medium"
    assumptions: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "These are planning estimates, not contractor quotations. "
        "Actual costs vary by location, labor, materials, availability, and project conditions."
    )


class BudgetScenario(BaseModel):
    """One entry of a budget-scenario comparison (section 35)."""

    tier: BudgetScenarioTier
    label: str
    estimated_total: float
    description: str
    changes: list[str] = Field(default_factory=list)


class MaterialRecommendation(BaseModel):
    """A single material recommendation with rationale (section 21)."""

    category: str
    material_name: str
    why: str
    cost_level: CostLevel
    maintenance: RiskLevel
    style_fit: str
    alternative: Optional[str] = None
    trade_off: Optional[str] = None


class MaterialComparisonOption(BaseModel):
    name: str
    cost: CostLevel
    maintenance: RiskLevel
    style_fit: str
    notes: Optional[str] = None


class MaterialComparison(BaseModel):
    """Comparison of two or more material alternatives (section 36)."""

    category: str
    options: list[MaterialComparisonOption] = Field(default_factory=list)
    ai_recommendation: str


class MaterialPlan(BaseModel):
    """Full output of app/agents/material_agent.py."""

    recommendations: list[MaterialRecommendation] = Field(default_factory=list)
    comparisons: list[MaterialComparison] = Field(default_factory=list)


class ShoppingItem(BaseModel):
    name: str
    category: str
    quantity: str
    estimated_cost: float
    priority: Priority = "recommended"
    alternative: Optional[str] = None
    notes: Optional[str] = None
    checked: bool = False


class ShoppingList(BaseModel):
    """Output of app/agents/shopping_agent.py (section 25)."""

    items: list[ShoppingItem] = Field(default_factory=list)


class TimelinePhase(BaseModel):
    phase_number: int
    name: str
    duration_days: str
    description: Optional[str] = None
    depends_on: list[str] = Field(default_factory=list)
    can_run_in_parallel: bool = False


class Timeline(BaseModel):
    """Output of app/agents/timeline_agent.py (section 26)."""

    total_estimated_days: str
    phases: list[TimelinePhase] = Field(default_factory=list)
    critical_path: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "Durations are planning estimates only, not guarantees about contractor timelines."
    )


class ExecutionTask(BaseModel):
    task: str
    dependencies: list[str] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)
    requires_professional: bool = False
    recommended_skill_note: Optional[str] = None
    stage: Literal[
        "before_renovation",
        "during_renovation",
        "installation",
        "styling",
        "final_inspection",
    ] = "during_renovation"
    status: TaskStatus = "not_started"


class ExecutionPlan(BaseModel):
    """Output of app/agents/execution_agent.py (section 27)."""

    tasks: list[ExecutionTask] = Field(default_factory=list)
    preparation_checklist: list[str] = Field(default_factory=list)
    final_inspection_checklist: list[str] = Field(default_factory=list)


class CriticReview(BaseModel):
    """Output of app/agents/critic_agent.py (section 28)."""

    issues: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
    approved: bool = True


# ---------------------------------------------------------------------------
# Final aggregate output (section 31)
# ---------------------------------------------------------------------------


class RenovationPlan(BaseModel):
    """The complete renovation plan returned to the frontend after the
    orchestrator finishes running all agents and the critic."""

    concept_name: str
    design_summary: str
    style: str
    estimated_budget: float
    currency: str = "PKR"
    estimated_timeline: str
    design_match: ConfidenceLevel = "High"
    budget_risk: RiskLevel = "Medium"

    design_concept: DesignConcept
    space_plan: SpacePlan
    budget: BudgetPlan
    materials: MaterialPlan
    shopping_list: ShoppingList
    timeline: Timeline
    execution_plan: ExecutionPlan

    alternatives: list[BudgetScenario] = Field(default_factory=list)
    ai_recommendations: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    generated_at: datetime = Field(default_factory=datetime.utcnow)
