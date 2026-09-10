"""Heuristic scoring helpers: design match confidence and budget risk.

These are local, deterministic heuristics (no AI call) used to fill in
confidence/risk fields when composing the final RenovationPlan, and to
sanity-check what an agent returns.
"""

from __future__ import annotations

from app.models.renovation import BudgetCategory, ConfidenceLevel, RenovationBrief, RiskLevel

# Minimum viable per-room budget by tier, in the user's stated currency
# units (rough order-of-magnitude planning heuristic, not a price feed).
_TIER_BASELINE = {
    "low": 100_000,
    "moderate": 300_000,
    "premium": 700_000,
    "luxury": 1_500_000,
    "custom": 300_000,
}


def compute_design_match(brief: RenovationBrief) -> ConfidenceLevel:
    """Heuristically estimate how well the brief's constraints let the AI
    produce a confident design match: more complete, less contradictory
    input -> higher confidence."""
    score = 0

    # Style clarity
    if brief.style.style != "custom" or (brief.style.custom_description or "").strip():
        score += 1

    # Goals specified
    if brief.goals or (brief.goal_description or "").strip():
        score += 1

    # Dimensions known
    if not brief.current_space.dimensions.unknown and brief.current_space.dimensions.length:
        score += 1

    # Budget realistic for tier
    baseline = _TIER_BASELINE.get(brief.budget.tier, 300_000)
    if brief.budget.max_budget >= baseline * 0.6:
        score += 1

    # Color preferences given (helps the design agent avoid guessing)
    if brief.colors.colors_wanted or brief.colors.custom_notes:
        score += 1

    if score >= 4:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def compute_budget_risk(
    total_estimate: float, max_budget: float, categories: list[BudgetCategory] | None = None
) -> RiskLevel:
    """Estimate budget risk from how close the plan's total estimate is to
    the user's stated maximum, and whether contingency looks adequate."""
    if max_budget <= 0:
        return "Medium"

    ratio = total_estimate / max_budget

    contingency_pct = 0.0
    if categories:
        for c in categories:
            if c.name.strip().lower() == "contingency":
                contingency_pct = c.percentage
                break

    if ratio > 1.05:
        return "High"
    if ratio > 0.95 or contingency_pct < 5:
        return "Medium"
    return "Low"


def budget_tier_baseline(tier: str) -> float:
    """Return the rough per-room baseline budget used for scoring/tier
    comparisons for a given budget tier."""
    return _TIER_BASELINE.get(tier, 300_000)
