"""Server-side support for saved projects (task.md section 46, 68).

Projects themselves are persisted client-side via localStorage -- there is
no server-side project storage. The only server-side need is generating a
downloadable PDF export of a RenovationPlan (section 68), since that isn't
practical to do purely in the browser with a polished layout.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from app.models.renovation import RenovationPlan
from app.services.pdf_service import generate_plan_pdf

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("/export-pdf")
async def export_pdf(plan: RenovationPlan) -> Response:
    """Generate a polished PDF export of a renovation plan."""

    pdf_bytes = generate_plan_pdf(plan)
    headers = {"Content-Disposition": "attachment; filename=renovation-plan.pdf"}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
