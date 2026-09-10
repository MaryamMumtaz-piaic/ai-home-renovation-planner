"""FastAPI application entry point for AI Home Renovation Planner.

Run with: uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import ai, feedback, materials, pages, projects

app = FastAPI(title="AI Home Renovation Planner")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(pages.router)
app.include_router(projects.router)
app.include_router(materials.router)
app.include_router(ai.router)
app.include_router(feedback.router)


@app.exception_handler(StarletteHTTPException)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404,
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
