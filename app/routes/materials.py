"""Material library JSON API + inspiration + cross-library search
(task.md section 56, 48, 49).

Design choice: /api/inspiration and /api/search are folded into this module
rather than a separate file, since both are simple read-only lookups over
the same JSON-backed library data as /api/materials and don't warrant their
own router.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from app.models.material import Material
from app.services import json_store

router = APIRouter(prefix="/api", tags=["materials"])


def _materials() -> list[dict]:
    data = json_store.read_json("materials.json")
    return data if isinstance(data, list) else []


def _inspiration() -> list[dict]:
    data = json_store.read_json("inspiration.json")
    return data if isinstance(data, list) else []


def _room_types() -> list[dict]:
    data = json_store.read_json("room_types.json")
    return data if isinstance(data, list) else []


def _design_styles() -> list[dict]:
    data = json_store.read_json("design_styles.json")
    return data if isinstance(data, list) else []


@router.get("/materials", response_model=list[Material])
async def list_materials(category: Optional[str] = None, q: Optional[str] = None):
    items = _materials()

    if category:
        cat_lower = category.lower()
        items = [m for m in items if str(m.get("category", "")).lower() == cat_lower]

    if q:
        q_lower = q.lower()
        items = [
            m
            for m in items
            if q_lower in str(m.get("name", "")).lower()
            or q_lower in str(m.get("description", "")).lower()
        ]

    return items


@router.get("/materials/{material_id}", response_model=Material)
async def get_material(material_id: str):
    for m in _materials():
        if m.get("id") == material_id or m.get("slug") == material_id:
            return m
    raise HTTPException(status_code=404, detail="Material not found")


@router.get("/inspiration")
async def list_inspiration(category: Optional[str] = None, q: Optional[str] = None):
    items = _inspiration()

    if category:
        cat_lower = category.lower()
        items = [
            item
            for item in items
            if cat_lower in [str(c).lower() for c in item.get("category", [])]
        ]

    if q:
        q_lower = q.lower()
        items = [
            item
            for item in items
            if q_lower in str(item.get("title", "")).lower()
            or q_lower in str(item.get("description", "")).lower()
        ]

    return items


@router.get("/search")
async def search(q: str = ""):
    """Unified search across materials, inspiration, room types, and design
    styles by substring match on name/title/description (section 49).
    Project search is client-side/localStorage and is intentionally
    excluded here."""

    q_lower = q.strip().lower()
    if not q_lower:
        return {"materials": [], "inspiration": [], "room_types": [], "design_styles": []}

    materials = [
        m
        for m in _materials()
        if q_lower in str(m.get("name", "")).lower()
        or q_lower in str(m.get("description", "")).lower()
        or q_lower in str(m.get("category", "")).lower()
    ]

    inspiration = [
        item
        for item in _inspiration()
        if q_lower in str(item.get("title", "")).lower()
        or q_lower in str(item.get("description", "")).lower()
        or q_lower in " ".join(str(c) for c in item.get("category", [])).lower()
    ]

    room_types = [
        r
        for r in _room_types()
        if q_lower in str(r.get("name", "")).lower()
        or q_lower in str(r.get("description", "")).lower()
    ]

    design_styles = [
        s
        for s in _design_styles()
        if q_lower in str(s.get("name", "")).lower()
        or q_lower in str(s.get("description", "")).lower()
    ]

    return {
        "materials": materials,
        "inspiration": inspiration,
        "room_types": room_types,
        "design_styles": design_styles,
    }
