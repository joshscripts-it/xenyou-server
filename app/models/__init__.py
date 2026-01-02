"""Top-level exports for app.models package.

This module re-exports the SQLModel classes defined in
`app.models.models` so callers can use `from app.models import X`.
It also provides a couple of compatibility aliases (Hostel -> Property,
Interaction -> InteractionEvent) for older naming.
"""

from .models import (
    User,
    StudentProfile,
    LandlordProfile,
    AdminProfile,
    Property,
    PropertyFeature,
    PropertyImage,
    InteractionEvent,
    Recommendation,
    SavedProperty,
    Match,
)

# Backwards-compatible aliases
Hostel = Property
Interaction = InteractionEvent

__all__ = [
    "User",
    "StudentProfile",
    "LandlordProfile",
    "AdminProfile",
    "Property",
    "PropertyFeature",
    "PropertyImage",
    "InteractionEvent",
    "Recommendation",
    "SavedProperty",
    "Match",
    "Hostel",
    "Interaction",
]
