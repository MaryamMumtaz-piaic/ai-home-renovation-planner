"""Validation helpers for renovation briefs and generated plan data.

Used to keep local validation cheap and avoid unnecessary AI calls
(task.md section 62) by catching incomplete/invalid input before it
reaches an agent.
"""

from __future__ import annotations

from app.models.renovation import BudgetCategory, RenovationBrief

# Percentage tolerance allowed when checking that budget category
# allocations sum to ~100%.
ALLOCATION_TOLERANCE = 1.5


def is_brief_complete(brief: RenovationBrief) -> bool:
    """Return True if the brief has the minimum information required to
    generate a renovation plan: a room type, at least one goal (or a goal
    description), a style, and a positive budget."""
    if not brief.room_type:
        return False
    if not brief.goals and not (brief.goal_description or "").strip():
        return False
    if not brief.style or not brief.style.style:
        return False
    if brief.budget is None or brief.budget.max_budget <= 0:
        return False
    return True


def missing_brief_fields(brief: RenovationBrief) -> list[str]:
    """Return a human-readable list of missing/incomplete required fields."""
    missing: list[str] = []
    if not brief.room_type:
        missing.append("room_type")
    if not brief.goals and not (brief.goal_description or "").strip():
        missing.append("goals")
    if not brief.style or not brief.style.style:
        missing.append("style")
    if brief.budget is None or brief.budget.max_budget <= 0:
        missing.append("budget.max_budget")
    return missing


def is_allocation_valid(
    categories: list[BudgetCategory], tolerance: float = ALLOCATION_TOLERANCE
) -> bool:
    """Sanity-check that budget category percentages sum to ~100%
    (within `tolerance` percentage points)."""
    if not categories:
        return False
    total_pct = sum(c.percentage for c in categories)
    return abs(total_pct - 100.0) <= tolerance


def is_amount_allocation_valid(
    categories: list[BudgetCategory], total_estimate: float, tolerance_ratio: float = 0.02
) -> bool:
    """Sanity-check that budget category amounts sum to ~total_estimate
    (within tolerance_ratio, default 2%)."""
    if not categories or total_estimate <= 0:
        return False
    total_amount = sum(c.amount for c in categories)
    return abs(total_amount - total_estimate) <= total_estimate * tolerance_ratio


def has_dimensions(brief: RenovationBrief) -> bool:
    """True if the user provided at least length and width and did not
    mark dimensions unknown."""
    dims = brief.current_space.dimensions
    if dims.unknown:
        return False
    return dims.length is not None and dims.width is not None
