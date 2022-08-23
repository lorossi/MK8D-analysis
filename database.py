import sqlite3

from entities import (
    Driver,
    Entity,
    SlimBuild,
    Vehicle,
    Tyre,
    Glider,
    SlimDriver,
    SlimVehicle,
    SlimTyre,
    SlimGlider,
    Build,
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
        q = (
            "select dd.name, d.ground_speed as speed, d.acceleration, "
            "d.weight, d.ground_handling as handling, d.traction, d.miniturbo "
        )

        if entity == EntityId.DRIVER:
            q += ", dd.size "

        q += (
            f"from {TABLE_NAMES[entity]} as d join {TABLE_NAMES[entity]}_names as dd "
            "on d.id = dd.id"
        )

        return q

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


class SlimMK8Deluxe(Database):
    def __init__(self):
        return super().__init__("MK8D")

    def _buildQuery(self, entity: EntityId = None) -> str:
        return (
            f"select d.id as {entity.value}_id, d.ground_speed as speed, d.acceleration, "
            "d.weight, d.ground_handling as handling, d.traction, d.miniturbo "
            f"from {TABLE_NAMES[entity]} as d"
        )

    def _queryEntities(self, entity: EntityId):
        query = self._buildQuery(entity)
        rows = self.query(query)
        cols = self.getCols(query)

        return [dict(zip(cols, row)) for row in rows]

    def __getattribute__(self, __name: str) -> list[Entity]:
        attributes_map = {
            "drivers": {"entity": EntityId.DRIVER, "class": SlimDriver},
            "vehicles": {"entity": EntityId.VEHICLE, "class": SlimVehicle},
            "tyres": {"entity": EntityId.TYRE, "class": SlimTyre},
            "gliders": {"entity": EntityId.GLIDER, "class": SlimGlider},
        }

        if __name not in attributes_map:
            return super().__getattribute__(__name)

        results = self._queryEntities(attributes_map[__name]["entity"])
        return (attributes_map[__name]["class"](**row) for row in results)


class MK8DeluxeBuilds(Database):
    def __init__(self):
        return super().__init__("MK8D")

    def _buildQuery(self, slim: bool = False) -> str:
        queries = {
            True: (
                "select * "
                "from builds_slim "
                "GROUP by speed, acceleration, weight, miniturbo "
                "order by speed desc "
            ),
            False: (
                "select d.name as driver, v.name as vehicle, t.name as tyre, g.name as glider, "
                "(b.speed * 0.5 + b.acceleration * 0.5) as score, "
                "b.speed, b.acceleration, b.miniturbo, b.handling, b.traction "
                "from builds_slim as b join drivers_names as d on b.driver_id = d.id "
                "join vehicles_names as v on b.vehicle_id = v.id "
                "join tyres_names as t on b.tyre_id = t.id "
                "join gliders_names as g on b.glider_id = g.id "
                "group by speed, acceleration, miniturbo, handling, traction "
                "order by score desc "
            ),
        }

        return queries[slim]

    def _buildList(self, slim: bool = False) -> list[Build | SlimBuild]:
        query = self._buildQuery(slim)
        rows = self.query(query)
        cols = self.getCols(query)

        return [Build(**dict(zip(cols, row))) for row in rows]

    @property
    def slim_builds(self) -> list[SlimBuild]:
        return self._buildList(slim=True)

    @property
    def builds(self) -> list[Build]:
        return self._buildList(slim=False)
