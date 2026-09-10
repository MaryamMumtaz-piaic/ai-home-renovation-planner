"""Misc formatting helpers shared across routes/services/templates."""

from __future__ import annotations

import re
import unicodedata

_CURRENCY_SYMBOLS = {
    "PKR": "PKR",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "AED": "AED",
    "SAR": "SAR",
    "INR": "₹",
}


def format_currency(amount: float, currency: str = "PKR") -> str:
    """Format an amount with thousands separators and a currency label.

    Examples:
        format_currency(500000, "PKR") -> "PKR 500,000"
        format_currency(4999.5, "USD") -> "$4,999.50"
    """
    currency = (currency or "PKR").upper()
    symbol = _CURRENCY_SYMBOLS.get(currency, currency)

    if float(amount).is_integer():
        formatted_amount = f"{int(amount):,}"
    else:
        formatted_amount = f"{amount:,.2f}"

    if symbol in ("$", "€", "£", "₹"):
        return f"{symbol}{formatted_amount}"
    return f"{symbol} {formatted_amount}"


def slugify(value: str) -> str:
    """Convert a string into a URL-safe slug, e.g. 'Engineered Wood
    Flooring' -> 'engineered-wood-flooring'."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[-\s]+", "-", value)
    return value


def format_percentage(value: float, decimals: int = 0) -> str:
    """Format a numeric percentage, e.g. format_percentage(35) -> '35%'."""
    return f"{value:.{decimals}f}%"


def truncate(text: str, max_length: int = 140, suffix: str = "…") -> str:
    """Truncate text to max_length characters, appending suffix if cut."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)].rstrip() + suffix


def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    """Return '<count> <singular|plural>' with correct pluralization."""
    plural = plural or f"{singular}s"
    label = singular if count == 1 else plural
    return f"{count} {label}"


def humanize_slug(value: str) -> str:
    """Turn a slug/enum value like 'mid_century_modern' or 'warm-white'
    into 'Mid Century Modern'."""
    words = re.split(r"[-_]+", value.strip())
    return " ".join(w.capitalize() for w in words if w)
