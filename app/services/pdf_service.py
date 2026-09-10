"""PDF export for a generated RenovationPlan (task.md section 68).

Uses ReportLab (already installed, no external assets required) to build a
clean, multi-section PDF: Project Overview, Design Concept, Budget,
Materials, Shopping List, Timeline, Execution Plan, Warnings, Assumptions.
"""

from __future__ import annotations

import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.models.renovation import RenovationPlan

_STYLES = getSampleStyleSheet()
_TITLE = ParagraphStyle(
    "PlanTitle", parent=_STYLES["Title"], fontSize=22, spaceAfter=6
)
_H2 = ParagraphStyle(
    "PlanH2",
    parent=_STYLES["Heading2"],
    fontSize=14,
    spaceBefore=16,
    spaceAfter=8,
    textColor=colors.HexColor("#1f2937"),
)
_BODY = ParagraphStyle("PlanBody", parent=_STYLES["BodyText"], fontSize=10, leading=14)
_SMALL = ParagraphStyle("PlanSmall", parent=_STYLES["BodyText"], fontSize=9, leading=12)


def _bullets(items: list[str], style: ParagraphStyle = _BODY) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(str(i), style)) for i in items],
        bulletType="bullet",
        leftIndent=14,
    )


def generate_plan_pdf(plan: RenovationPlan) -> bytes:
    """Render a RenovationPlan into a formatted PDF and return its bytes."""

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=plan.concept_name or "Renovation Plan",
    )

    story: list = []

    # --- Project Overview ---------------------------------------------
    story.append(Paragraph(plan.concept_name or "Renovation Plan", _TITLE))
    story.append(Paragraph(plan.design_summary or "", _BODY))
    story.append(Spacer(1, 8))

    overview_rows = [
        ["Style", plan.style],
        ["Estimated Budget", f"{plan.currency} {plan.estimated_budget:,.0f}"],
        ["Estimated Timeline", plan.estimated_timeline],
        ["Design Match", plan.design_match],
        ["Budget Risk", plan.budget_risk],
        ["Generated At", plan.generated_at.strftime("%Y-%m-%d %H:%M")],
    ]
    overview_table = Table(overview_rows, colWidths=[1.8 * inch, 4.2 * inch])
    overview_table.setStyle(
        TableStyle(
            [
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6b7280")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
            ]
        )
    )
    story.append(overview_table)

    # --- Design Concept --------------------------------------------------
    story.append(Paragraph("Design Concept", _H2))
    dc = plan.design_concept
    story.append(Paragraph(f"<b>{dc.concept_name}</b> — {dc.style}", _BODY))
    story.append(Paragraph(dc.design_summary, _BODY))
    if dc.color_palette:
        story.append(Paragraph("<b>Color Palette:</b> " + ", ".join(dc.color_palette), _SMALL))
    if dc.materials:
        story.append(Paragraph("<b>Materials:</b> " + ", ".join(dc.materials), _SMALL))
    if dc.furniture_direction:
        story.append(Paragraph("<b>Furniture Direction</b>", _SMALL))
        story.append(_bullets(dc.furniture_direction, _SMALL))

    # --- Budget ------------------------------------------------------------
    story.append(Paragraph("Budget", _H2))
    b = plan.budget
    story.append(
        Paragraph(f"<b>Total Estimate:</b> {b.currency} {b.total_estimate:,.0f}", _BODY)
    )
    if b.categories:
        rows = [["Category", "Amount", "%"]]
        for c in b.categories:
            rows.append([c.name, f"{b.currency} {c.amount:,.0f}", f"{c.percentage:.0f}%"])
        budget_table = Table(rows, colWidths=[2.5 * inch, 2 * inch, 1 * inch])
        budget_table.setStyle(
            TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f4f6")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e5e7eb")),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(Spacer(1, 4))
        story.append(budget_table)
    if b.contingency:
        story.append(Paragraph(f"<b>Contingency:</b> {b.currency} {b.contingency:,.0f}", _SMALL))
    if b.savings_opportunities:
        story.append(Paragraph("<b>Savings Opportunities</b>", _SMALL))
        story.append(_bullets(b.savings_opportunities, _SMALL))
    story.append(Paragraph(f"<i>{b.disclaimer}</i>", _SMALL))

    # --- Materials ----------------------------------------------------------
    story.append(Paragraph("Materials", _H2))
    if plan.materials.recommendations:
        for rec in plan.materials.recommendations:
            story.append(
                Paragraph(
                    f"<b>{rec.category}: {rec.material_name}</b> "
                    f"(Cost: {rec.cost_level}, Maintenance: {rec.maintenance})",
                    _SMALL,
                )
            )
            story.append(Paragraph(rec.why, _SMALL))
    else:
        story.append(Paragraph("No material recommendations available.", _SMALL))

    # --- Shopping List --------------------------------------------------
    story.append(Paragraph("Shopping List", _H2))
    if plan.shopping_list.items:
        rows = [["Item", "Category", "Qty", "Est. Cost", "Priority"]]
        for item in plan.shopping_list.items:
            rows.append(
                [
                    item.name,
                    item.category,
                    item.quantity,
                    f"{item.estimated_cost:,.0f}",
                    item.priority,
                ]
            )
        shop_table = Table(
            rows, colWidths=[1.7 * inch, 1.2 * inch, 0.8 * inch, 1 * inch, 1 * inch]
        )
        shop_table.setStyle(
            TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f4f6")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e5e7eb")),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(shop_table)
    else:
        story.append(Paragraph("No shopping list items available.", _SMALL))

    # --- Timeline -------------------------------------------------------
    story.append(Paragraph("Timeline", _H2))
    t = plan.timeline
    story.append(Paragraph(f"<b>Total Estimated Duration:</b> {t.total_estimated_days}", _BODY))
    if t.phases:
        for phase in t.phases:
            story.append(
                Paragraph(
                    f"<b>Phase {phase.phase_number}: {phase.name}</b> "
                    f"({phase.duration_days})",
                    _SMALL,
                )
            )
            if phase.description:
                story.append(Paragraph(phase.description, _SMALL))
    story.append(Paragraph(f"<i>{t.disclaimer}</i>", _SMALL))

    # --- Execution Plan ---------------------------------------------------
    story.append(Paragraph("Execution Plan", _H2))
    ep = plan.execution_plan
    if ep.preparation_checklist:
        story.append(Paragraph("<b>Preparation Checklist</b>", _SMALL))
        story.append(_bullets(ep.preparation_checklist, _SMALL))
    if ep.tasks:
        story.append(Paragraph("<b>Tasks</b>", _SMALL))
        story.append(_bullets([task.task for task in ep.tasks], _SMALL))
    if ep.final_inspection_checklist:
        story.append(Paragraph("<b>Final Inspection Checklist</b>", _SMALL))
        story.append(_bullets(ep.final_inspection_checklist, _SMALL))

    # --- Warnings & Assumptions ------------------------------------------
    story.append(Paragraph("Warnings", _H2))
    if plan.warnings:
        story.append(_bullets(plan.warnings, _BODY))
    else:
        story.append(Paragraph("No warnings.", _SMALL))

    story.append(Paragraph("Assumptions", _H2))
    if plan.assumptions:
        story.append(_bullets(plan.assumptions, _BODY))
    else:
        story.append(Paragraph("No assumptions recorded.", _SMALL))

    doc.build(story)
    return buffer.getvalue()
