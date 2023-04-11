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
    "miniturbo",
    "on_road_traction",
    "off_road_traction",
]

ID_ATTRIBUTES = ["driver_id", "vehicle_id", "tyre_id", "glider_id"]

DATA_ATTRIBUTES = ["score", "score_dev"]

CSV_ATTRIBUTES = {
    "id": "id",
    "name": "name",
    "WG": "weight",
    "AC": "acceleration",
    "ON": "on_road_traction",
    "OF": "off_road_traction",
    "MT": "miniturbo",
    "SL": "ground_speed",
    "SW": "water_speed",
    "SA": "antigravity_speed",
    "SG": "air_speed",
    "TL": "ground_handling",
    "TW": "water_handling",
    "TA": "antigravity_handling",
    "TG": "air_handling",
}
