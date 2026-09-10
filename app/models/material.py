"""Material library models used by /materials and /material/{slug}."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

MaterialCategory = Literal[
    "Flooring",
    "Paint",
    "Wall Finishes",
    "Lighting",
    "Countertops",
    "Cabinet Materials",
    "Hardware",
    "Furniture Materials",
]

CostLevel = Literal["Low", "Medium", "High"]
MaintenanceLevel = Literal["Low", "Medium", "High"]
DurabilityLevel = Literal["Low", "Medium", "High"]


class Material(BaseModel):
    """A single material library entry (app/data/materials.json)."""

    id: str
    slug: str
    name: str
    category: MaterialCategory
    description: str
    style_compatibility: list[str] = Field(default_factory=list)
    cost_level: CostLevel
    maintenance: MaintenanceLevel
    durability: DurabilityLevel
    common_uses: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    ai_notes: Optional[str] = None
