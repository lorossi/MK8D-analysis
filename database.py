import sqlite3
from re import findall, match

from entities import (
    Entity,
    NamedBuild,
    Build,
    PartFactory,
)
from constants import (
    PARTS_ATTRIBUTES,
    EntityId,
    TABLE_NAMES,
    ID_ATTRIBUTES,
    DATA_ATTRIBUTES,
)


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
            "drivers": EntityId.DRIVER,
            "vehicles": EntityId.VEHICLE,
            "tyres": EntityId.TYRE,
            "gliders": EntityId.GLIDER,
        }

        if __name not in attributes_map:
            return super().__getattribute__(__name)

        results = self._queryEntities(attributes_map[__name])
        return (PartFactory(attributes_map[__name]).build(**row) for row in results)


class MK8DeluxeBuilds(MK8Deluxe):
    """Return a list of builds. Accept filters as parameters.

    Args:
        MK8Deluxe (_type_): _description_
    """

    def __init__(self):
        super().__init__()
        self._sql_filter = []
        self._data_filter = []
        self._sort = []
        self._limit = None

    def _buildQuery(self, *_) -> str:
        q = (
            "select  b.driver_id, b.vehicle_id, b.tyre_id, b.glider_id, "
            "b.speed, b.acceleration, b.weight, b.handling, b.traction, b.miniturbo "
            "from builds as b "
        )

        if self._sql_filter:
            q += f"where {' and '.join(self._sql_filter)}"

        return q

    def __setattr__(self, __name: str, __value) -> None:
        if f := match(r"(min|max)_([a-z]+)", __name):

            if f.group(2) in PARTS_ATTRIBUTES:
                match f.group(1):
                    case "min":
                        self._sql_filter.append(f"b.{f.group(2)} >= {__value}")
                    case "max":
                        self._sql_filter.append(f"b.{f.group(2)} <= {__value}")
                return

            if f.group(2) in DATA_ATTRIBUTES:
                match f.group(1):
                    case "min":
                        self._data_filter.append(
                            lambda x: x.__getattribute__(f.group(2)) >= __value
                        )
                    case "max":
                        self._data_filter.append(
                            lambda x: x.__getattribute__(f.group(2)) <= __value
                        )

                return

        if f := match(r"sort_([a-z]+)", __name):
            if f.group(1) in DATA_ATTRIBUTES and __value in [-1, 1]:
                self._sort.append((f.group(1), __value == -1))
                return

        if __name == "limit":
            self._limit = __value
            return

        if __name == "sort" and __value is None:
            self._sort = []
            return

        return super().__setattr__(__name, __value)

    def getNames(self, entity_id: EntityId, entity_code: int) -> list[str]:
        q = (
            f"select e.name "
            f"from {TABLE_NAMES[entity_id]}_names as e "
            f"where e.id = {entity_code}"
        )
        return [r[0] for r in self.query(q)]

    @property
    def builds(self) -> list[Build]:
        results = self._queryEntities(EntityId.BUILD)
        return [Build(**row) for row in results]

    @property
    def named_builds(self) -> list[NamedBuild]:
        results = self._queryEntities(EntityId.BUILD)
        for x, r in enumerate(results):
            names = {}
            for e in EntityId:
                if e == EntityId.BUILD:
                    continue

                names[e.value] = [x for x in self.getNames(e, r.get(f"{e.value}_id"))]

            results[x].update(names)

            for i in ID_ATTRIBUTES:
                del results[x][i]

        builds = [
            b
            for b in [NamedBuild(**row) for row in results]
            if all(f(b) for f in self._data_filter)
        ]

        for f in self._sort:
            builds.sort(key=lambda x: x.__getattribute__(f[0]), reverse=f[1])

        if self._limit is not None:
            builds = builds[: self._limit]

        return builds

    @property
    def available_filters(self) -> str:
        return [
            (f"{a}_{b}")
            for a in ["min", "max"]
            for b in PARTS_ATTRIBUTES + DATA_ATTRIBUTES
        ]

    @property
    def available_sorts(self) -> str:
        return [f"sort_{a}" for a in DATA_ATTRIBUTES]
