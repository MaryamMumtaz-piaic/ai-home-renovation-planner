"""HTML page routes rendered via Jinja2Templates (task.md section 56).

Each route renders one of the templates under templates/ with the context
that template needs. All data comes from the JSON-backed library via
app.services.json_store — no AI calls happen on page routes.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from app.services import json_store

router = APIRouter(tags=["pages"])

templates = Jinja2Templates(directory="templates")


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


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "active_nav": "home",
            "room_types": _room_types(),
            "design_styles": _design_styles(),
            "featured_inspiration": _inspiration()[:6],
        },
    )


@router.get("/planner")
async def planner(request: Request):
    return templates.TemplateResponse(
        "planner.html",
        {
            "request": request,
            "active_nav": "planner",
            "room_types": _room_types(),
            "design_styles": _design_styles(),
        },
    )


@router.get("/projects")
async def projects(request: Request):
    # Projects are stored client-side in localStorage (section 46) -- this
    # route only renders the shell; all data is loaded/rendered by JS.
    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "active_nav": "projects",
        },
    )


@router.get("/plan")
async def plan_page(request: Request):
    # Plan data is generated client-side (POST /api/ai/create-plan) and held
    # in sessionStorage/localStorage; this route only renders the shell.
    return templates.TemplateResponse(
        "plan.html",
        {"request": request, "active_nav": "planner"},
    )


@router.get("/project")
async def project_page(request: Request):
    # Reads ?id= client-side and loads the matching saved project from
    # localStorage; this route only renders the shell.
    return templates.TemplateResponse(
        "project.html",
        {"request": request, "active_nav": "projects"},
    )


@router.get("/inspiration")
async def inspiration(
    request: Request,
    category: Optional[str] = None,
    q: Optional[str] = None,
):
    items = _inspiration()

    if category:
        cat_lower = category.lower()
        items = [
            item
            for item in items
            if cat_lower
            in [str(c).lower() for c in item.get("category", [])]
        ]

    if q:
        q_lower = q.lower()
        items = [
            item
            for item in items
            if q_lower in str(item.get("title", "")).lower()
            or q_lower in str(item.get("description", "")).lower()
        ]

    categories: list[str] = sorted(
        {c for item in _inspiration() for c in item.get("category", [])}
    )

    return templates.TemplateResponse(
        "inspiration.html",
        {
            "request": request,
            "active_nav": "inspiration",
            "inspiration_items": items,
            "categories": categories,
            "selected_category": category,
            "query": q,
        },
    )


@router.get("/materials")
async def materials(
    request: Request,
    category: Optional[str] = None,
    q: Optional[str] = None,
):
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

    categories: list[str] = sorted({m.get("category", "") for m in _materials() if m.get("category")})

    return templates.TemplateResponse(
        "materials.html",
        {
            "request": request,
            "active_nav": "materials",
            "materials": items,
            "categories": categories,
            "selected_category": category,
            "query": q,
        },
    )


@router.get("/material/{slug}")
async def material_detail(request: Request, slug: str):
    all_materials = _materials()
    material = next((m for m in all_materials if m.get("slug") == slug), None)

    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")

    alt_slugs = material.get("alternatives", [])
    alternatives = [m for m in all_materials if m.get("slug") in alt_slugs][:3]

    return templates.TemplateResponse(
        "material.html",
        {
            "request": request,
            "active_nav": "materials",
            "material": material,
            "alternatives": alternatives,
        },
    )


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "active_nav": "about"},
    )


@router.get("/faq")
async def faq(request: Request):
    return templates.TemplateResponse(
        "faq.html",
        {"request": request, "active_nav": "faq"},
    )


@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "active_nav": "contact"},
    )
