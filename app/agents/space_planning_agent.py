"""Space planning agent (task.md section 22 / 43). Adapts its guidance per
room type instead of applying identical planning logic to every room."""

from __future__ import annotations

from app.models.renovation import RenovationBrief, SpacePlan
from app.services import openai_service

# Room-specific considerations the prompt should foreground (section 43).
_ROOM_CONSIDERATIONS: dict[str, str] = {
    "kitchen": (
        "Kitchen space planning must consider: cabinetry layout, countertop "
        "workspace, storage (pantry/cabinets/drawers), task and ambient "
        "lighting, appliance placement, and the kitchen work triangle/workflow."
    ),
    "bedroom": (
        "Bedroom space planning must consider: bed placement and clearances, "
        "storage (closet/wardrobe/dresser), layered lighting, comfort, color "
        "scheme, and privacy from doors/windows/sightlines."
    ),
    "bathroom": (
        "Bathroom space planning must consider: fixture placement (sink, "
        "toilet, shower/tub), storage, moisture-safe lighting, durable/"
        "water-resistant surfaces, and ease of maintenance."
    ),
    "living_room": (
        "Living room space planning must consider: seating arrangement and "
        "conversation areas, entertainment/media placement, layered lighting, "
        "circulation paths, storage, and decor placement."
    ),
}

_DEFAULT_CONSIDERATION = (
    "Adapt the space plan to this room's typical use, adjacencies, and "
    "traffic patterns rather than using generic furniture-layout logic."
)


async def create_space_plan(brief: RenovationBrief) -> SpacePlan:
    """Generate a room-aware space plan, incorporating room-type-specific
    planning intelligence per section 43."""
    hint = _ROOM_CONSIDERATIONS.get(brief.room_type, _DEFAULT_CONSIDERATION)
    return await openai_service.generate_space_plan(brief, room_hint=hint)
