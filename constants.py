from enum import Enum


class EntityId(Enum):
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
    "speed",
    "acceleration",
    "weight",
    "handling",
    "traction",
    "miniturbo",
]

ID_ATTRIBUTES = ["driver_id", "vehicle_id", "tyre_id", "glider_id"]

DATA_ATTRIBUTES = ["score", "std_dev"]
