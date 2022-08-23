import sqlite3

from entities import (
    Driver,
    Entity,
    Vehicle,
    Tyre,
    Glider,
)
from constants import EntityId, TABLE_NAMES


class Database:
    def __init__(self, path: str):
        self._path = path
        self._con = sqlite3.connect(self._path)
        self._cur = self._con.cursor()

    def query(self, q: str):
        self._cur.execute(q)
        return self._cur.fetchall()

    def getCols(self, q: str):
        self._cur.execute(q)
        return [i[0] for i in self._cur.description]


class MK8Deluxe(Database):
    def __init__(self):
        super().__init__("MK8D")

    def _buildQuery(self, entity: EntityId = None) -> str:
        return (
            f"select d.id as {entity.value}_id, d.ground_speed as speed, d.acceleration, "
            "d.weight, d.ground_handling as handling, d.traction, d.miniturbo "
            f"from {TABLE_NAMES[entity]} as d"
        )

    def _queryEntities(
        self,
        entity: EntityId,
    ) -> list[dict[str, float | str]]:
        query = self._buildQuery(entity)
        rows = self.query(query)
        cols = self.getCols(query)

        return [dict(zip(cols, row)) for row in rows]

    def __getattribute__(self, __name: str) -> list[Entity]:
        attributes_map = {
            "drivers": {"entity": EntityId.DRIVER, "class": Driver},
            "vehicles": {"entity": EntityId.VEHICLE, "class": Vehicle},
            "tyres": {"entity": EntityId.TYRE, "class": Tyre},
            "gliders": {"entity": EntityId.GLIDER, "class": Glider},
        }

        if __name not in attributes_map:
            return super().__getattribute__(__name)

        results = self._queryEntities(attributes_map[__name]["entity"])
        return (attributes_map[__name]["class"](**row) for row in results)
