"""Module containing constants for the project."""
from enum import Enum


class EntityId(Enum):
    """Id containing the entity of a part.

    Args:
        Enum (str)
    """

    DRIVER = "driver"
    VEHICLE = "vehicle"
    TYRE = "tyre"
    GLIDER = "glider"
    BUILD = "build"


TABLE_NAMES = {
    EntityId.DRIVER: "drivers",
    EntityId.VEHICLE: "vehicles",
    EntityId.TYRE: "tyres",
    EntityId.GLIDER: "gliders",
    EntityId.BUILD: "builds",
}

PARTS_ATTRIBUTES = [
    "ground_speed",
    "water_speed",
    "air_speed",
    "antigravity_speed",
    "acceleration",
    "weight",
    "ground_handling",
    "water_handling",
    "air_handling",
    "antigravity_handling",
    "traction",
    "miniturbo",
]

ID_ATTRIBUTES = ["driver_id", "vehicle_id", "tyre_id", "glider_id"]

DATA_ATTRIBUTES = ["score", "score_dev"]
