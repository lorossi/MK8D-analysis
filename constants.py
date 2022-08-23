from enum import Enum


class EntityId(Enum):
    DRIVER = "driver"
    VEHICLE = "vehicle"
    TYRE = "tyre"
    GLIDER = "glider"
    BUILD = "build"
    SLIM_BUILD = "slim_build"


TABLE_NAMES = {
    EntityId.DRIVER: "drivers",
    EntityId.VEHICLE: "vehicles",
    EntityId.TYRE: "tyres",
    EntityId.GLIDER: "gliders",
}

COLUMN_IDS = ["driver_id", "vehicle_id", "tyre_id", "glider_id"]
VARIABLES = ["speed", "acceleration", "weight", "handling", "traction", "miniturbo"]
BUILD_VARIABLES = ["driver", "vehicle", "tyres", "gliders"]
