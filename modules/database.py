"""This module contains the Database class and all its subclasses."""
from __future__ import annotations

import sqlite3
from re import Match, match

from .constants import (
    DATA_ATTRIBUTES,
    ID_ATTRIBUTES,
    PARTS_ATTRIBUTES,
    TABLE_NAMES,
    EntityId,
)
from .entities import (
    Build,
    Entity,
    NamedBuild,
    PartFactory,
)


class Database:
    """Class handling a generic database."""

    def __init__(self, path: str) -> Database:
        """Create a database object.

        Args:
            path (str): Path to the SQLite database file.
        """
        self._path = path
        self._con = sqlite3.connect(self._path)
        self._cur = self._con.cursor()

    def query(self, q: str) -> list:
        """Make a query to the database.

        Args:
            q (str): Query to make to the database.

        Returns:
            list: Result of the query.
        """
        self._cur.execute(q)
        return self._cur.fetchall()

    def getCols(self, q: str) -> list[str]:
        """Get the column names relative to a query in the database.

        Args:
            q (str): Query to make to the database.

        Returns:
            list[str]: list of column names.
        """
        self._cur.execute(q)
        return [i[0] for i in self._cur.description]

    def tableExists(self, table: str) -> bool:
        """Check if a table exists in the database.

        Args:
            table (str): Name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        q = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
        return bool(self.query(q))

    def deleteTable(self, table: str):
        """Delete (drop) a table from the database.

        Args:
            table (str): Name of the table to drop.
        """
        q = f"DROP TABLE {table}"
        try:
            self._cur.execute(q)
        except sqlite3.OperationalError:
            print(f"Cannot delete table {table} because it does not exist.")

    def createTable(self, table: str, cols: list, types: list = None, pk: str = None):
        """Create a table in the database.

        Args:
            table (str): name of the table to create.
            cols (list): list of columns to create.
        """
        if types is None:
            types = ["STRING"] * len(cols)

        if pk is None:
            pk = cols[0]

        cols_typed = [f"{c} {t}" for c, t in zip(cols, types)]

        q = f"CREATE TABLE {table} ({', '.join(cols_typed)}, PRIMARY KEY ({pk}))"
        self._cur.execute(q)

    def insert(self, table: str, cols: list, values: list):
        """Insert a row in a table.

        Args:
            table (str): name of the table to insert into.
            cols (list): name of the columns to insert into.
            values (list): values to insert.
        """
        q = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ("

        for v in values:
            if isinstance(v, str):
                q += f"'{v}',"
            else:
                q += f"{v},"

        q = q[:-1] + ")"

        self._cur.execute(q)

    def commitChanges(self):
        """Apply changes to the database."""
        self._con.commit()


class MK8Deluxe(Database):
    """Class handling the MK8 Deluxe database."""

    def __init__(self) -> MK8Deluxe:
        """Create a MK8Deluxe object."""
        super().__init__("MK8D")

    def _buildQuery(self, entity: EntityId) -> str:
        """Build a string query to get the data from the database.

        Args:
            entity (EntityId): Id of the entity to query.

        Returns:
            str: Query to pass to the database.
        """
        return (
            f"select d.id as {entity.value}_id, "
            f"{', '.join(PARTS_ATTRIBUTES)} "
            f"from {TABLE_NAMES[entity]} as d"
        )

    def _queryEntities(
        self,
        entity: EntityId,
    ) -> list[dict[str, float | str]]:
        """Query the database for a specific entity.

        Args:
            entity (EntityId): Id of the entity to query.

        Returns:
            list[dict[str, float | str]]: list of dictionaries containing the data.
        """
        query = self._buildQuery(entity)
        rows = self.query(query)
        cols = self.getCols(query)

        return [dict(zip(cols, row)) for row in rows]

    def __getattr__(self, __name: str) -> list[Entity]:
        """Get an entity from the database.

        Args:
            __name (str): name of the entity.

        Returns:
            list[Entity]: list of entities.
        """
        if __name not in [x.value for x in EntityId]:
            return super().__getattribute__(__name)

        results = self._queryEntities(EntityId(__name))

        if not results:
            raise AttributeError(f"Entity {__name} does not exist")

        return (PartFactory(EntityId(__name)).build(**row) for row in results)


class MK8DeluxeBuilds(MK8Deluxe):
    """Class handling the MK8Deluxe builds database."""

    def __init__(self) -> MK8DeluxeBuilds:
        """Create a MK8DeluxeBuilds object."""
        super().__init__()
        self._sql_filter = []  # filter for attributes
        self._data_filter = []  # filter for data attributes such as score or stddev
        self._sort = []  # list of attributes to sort by
        self._limit = None

        # weights of the attributes for the score calculation
        self._weights = {k: 0 for k in PARTS_ATTRIBUTES}
        # attributes to consider for the skyline query
        self._rank_attributes = dict.fromkeys(PARTS_ATTRIBUTES, False)

    def _buildQuery(self, *_) -> str:
        """Build a query to get the data from the database.

        Returns:
            str: query to pass to the database.
        """
        q = "SELECT * FROM builds AS b "

        # add filters to the query
        if self._sql_filter:
            q += f"where {' and '.join(self._sql_filter)}"

        return q

    def _setFilter(self, match: Match, value: int) -> None:
        """Set a filter for the query.

        Args:
            match (Match): Match object containing the filter.
            value (int): Value of the filter.

        Raises:
            AttributeError: Filter is not valid.
        """
        # filter any part attribute
        # these filters are passed to the SQL query
        if match.group(2) in PARTS_ATTRIBUTES:
            # differentiate between min and max
            match match.group(1):
                case "min":
                    self._sql_filter.append(f"b.{match.group(2)} >= {value}")
                case "max":
                    self._sql_filter.append(f"b.{match.group(2)} <= {value}")
            return

        # filter any data attribute
        # these filters are passed to the data after the query
        if match.group(2) in DATA_ATTRIBUTES:
            match match.group(1):
                case "min":
                    self._data_filter.append(
                        lambda x: x.__getattribute__(match.group(2)) >= value
                    )
                case "max":
                    self._data_filter.append(
                        lambda x: x.__getattribute__(match.group(2)) <= value
                    )

            return

        # raise error for invalid filter
        raise AttributeError(f"{match.group(2)} is not a valid filter")

    def _setSort(self, match: Match, direction: int) -> None:
        """Set a sort for the query.

        Args:
            match (Match): Match object containing the sort.
            direction (int): Direction of the sort (1 ascending, -1 descending).

        Raises:
            AttributeError: sort is not valid.
        """
        if match.group(1) in PARTS_ATTRIBUTES + DATA_ATTRIBUTES and direction in [
            -1,
            1,
        ]:
            self._sort.append((match.group(1), direction == -1))
            return

        raise AttributeError(f"{match.group(1)} is not a valid sort")

    def _setWeight(self, match: Match, value: float) -> None:
        """Set weight for score calculation for a specific attribute.

        Args:
            match (Match): Match object containing the attribute.
            value (float): Weight of the attribute.

        Raises:
            AttributeError: Attribute is not valid.
            TypeError: Value is not a float.
            ValueError: Value is less than 0.
        """
        if match.group(1) not in PARTS_ATTRIBUTES:
            raise AttributeError(f"{match.group(1)} is not a valid weight")

        if not isinstance(value, float):
            raise TypeError(f"{value} is not a valid weight")
        if value < 0:
            raise ValueError(f"{value} is not a valid weight")

        self._weights[match.group(1)] = value

    def _setRankingAttribute(self, match: Match, value: int) -> None:
        """Set a ranking attribute.

        Args:
            match (Match): Match object containing the attribute.
            value (int): Value of the attribute.

        Raises:
            AttributeError: Attribute is not valid.
        """
        if match.group(1) not in PARTS_ATTRIBUTES:
            raise AttributeError(f"{match.group(1)} is not a valid attributes")

        if value not in [0, 1]:
            raise ValueError(f"{value} is not a valid attributes")

        self._rank_attributes[match.group(1)] = bool(value)

    def _getNamedBuilds(self) -> list[NamedBuild]:
        # get all results
        results = self._queryEntities(EntityId.BUILD)

        for x, r in enumerate(results):
            names = {}
            # get names for each part
            for e in EntityId:
                # skip the build Entities as they are not named
                if e == EntityId.BUILD:
                    continue

                # save all the names for the part
                names[e.value] = [x for x in self.getNames(e, r.get(f"{e.value}_id"))]

            # save the names in the results
            results[x].update(names)

            # delete the ids from the results
            for i in ID_ATTRIBUTES:
                del results[x][i]

        # create the named builds
        return [
            b
            for b in [NamedBuild(**row, _weights=self._weights) for row in results]
            if all(f(b) for f in self._data_filter)  # apply data filters
        ]

    def __setattr__(self, __name: str, __value) -> None:
        """Set an attribute of the object.

        Args:
            __name (str): name of the attribute.
            __value (_type_): value of the attribute.
        """
        # try to match the attribute name to a filter
        if f := match(r"(min|max)_([a-z_]+)", __name):
            self._setFilter(f, __value)
            return

        # try to match the attribute name to a sort
        if f := match(r"sort_([a-z_]+)", __name):
            self._setSort(f, __value)
            return

        # try to match the attribute name to a weight
        if f := match(r"weight_([a-z_]+)", __name):
            self._setWeight(f, __value)
            return

        # try to match the attribute name to a rank attribute
        if f := match(r"rank_([a-z_]+)", __name):
            self._setRankingAttribute(f, __value)
            return

        # set the limit
        if __name == "limit":
            if __value is None:
                self._limit = None
                return
            if not isinstance(__value, int):
                raise TypeError(f"{__value} is not a valid limit")
            self._limit = __value
            return

        # reset the sorting order
        if __name == "sort" and __value is None:
            self._sort = []
            return

        return super().__setattr__(__name, __value)

    def getNames(self, entity_id: EntityId, entity_code: int) -> list[str]:
        """Get names relative to a specific part, given its code.

        Args:
            entity_id (EntityId): Id of the entity.
            entity_code (int): Code of the entity.

        Returns:
            list[str]: List of names relative to the entity.
        """
        q = (
            f"SELECT E.NAME "
            f"FROM {TABLE_NAMES[entity_id]}_names AS E "
            f"WHERE e.id = {entity_code}"
        )
        return [r[0] for r in self.query(q)]

    def _bnlAlgorithm(self, builds: list[NamedBuild]) -> list[NamedBuild]:
        attributes = [k for k, v in self._rank_attributes.items() if v is True]
        w = set()

        for p in builds:
            if any(pp.dominate(p) for pp in w):
                continue

            w -= {pp for pp in w if p.dominate(pp, attributes)}
            w.add(p)

        return list(w)

    def _returnBuilds(self, builds: list[NamedBuild]) -> list[NamedBuild]:
        # sort the builds by score
        for f in self._sort[::-1]:
            builds.sort(key=lambda x: x.__getattribute__(f[0]), reverse=f[1])

        # limit the number of builds
        if self._limit is not None:
            builds = builds[: self._limit]

        return builds

    @property
    def builds(self) -> list[Build]:
        """Get the builds.

        Returns:
            list[Build]: list of builds.
        """
        results = self._queryEntities(EntityId.BUILD)
        return [Build(**row) for row in results]

    @property
    def scored_named_builds(self) -> list[NamedBuild]:
        """Get the builds with parts names.

        Returns:
            list[NamedBuild]: list of builds with parts names.
        """
        builds = self._getNamedBuilds()
        return self._returnBuilds(builds)

    @property
    def dominating_named_builds(self) -> list[NamedBuild]:
        """Get the dominating builds with parts names.

        Returns:
            list[NamedBuild]: list of dominating builds with parts names.
        """
        builds = self._getNamedBuilds()
        dominating = self._bnlAlgorithm(builds)
        return self._returnBuilds(dominating)

    @staticmethod
    def getAvailableFilters() -> list[str]:
        """List all the available filters for the build.

        Pass the filter name to the instance of the object to set it.
        The attribute accepts a value.


        Returns:
            list[str]
        """
        return [
            (f"{a}_{b}")
            for a in ["min", "max"]
            for b in PARTS_ATTRIBUTES + DATA_ATTRIBUTES
        ]

    @property
    def available_filters(self) -> list[str]:
        """List all the available filters for the build.

        Pass the filter name to the instance of the object to set it.
        The attribute accepts a value.


        Returns:
            list[str]
        """
        return MK8DeluxeBuilds.getAvailableFilters()

    @staticmethod
    def getAvailableSortOrders() -> list[str]:
        """List all the available sorts for the build.

        Pass the sort name to the instance of the object to set it.
        The attribute accepts a value of 1 for ascending and -1 for descending.

        Returns:
            list[str]
        """
        return [f"sort_{a}" for a in PARTS_ATTRIBUTES + DATA_ATTRIBUTES]

    @property
    def available_sorts_order(self) -> list[str]:
        """List all the available sorts for the build.

        Pass the sort name to the instance of the object to set it.
        The attribute accepts a value of 1 for ascending and -1 for descending.

        Returns:
            list[str]
        """
        return MK8DeluxeBuilds.getAvailableSortOrders()

    @staticmethod
    def getAvailableWeights() -> list[str]:
        """List all the available weights for the scoring of the builds.

        Pass the weight name to the instance of the object to set it.
        The attribute accepts a value of type float.

        Returns:
            list[str]
        """
        return [f"weight_{a}" for a in PARTS_ATTRIBUTES]

    @property
    def available_weights(self) -> list[str]:
        """List all the available weights for the scoring of the builds.

        Pass the weight name to the instance of the object to set it.
        The attribute accepts a value of type float.

        Returns:
            list[str]
        """
        return MK8DeluxeBuilds.getAvailableWeights()

    @staticmethod
    def getAvailableRankingAttributes() -> list[str]:
        """List all the available ranking attributes for the build.

        Returns:
            list[str]
        """
        return [f"attributes_{a}" for a in PARTS_ATTRIBUTES]

    @property
    def ranking_attributes(self) -> list[str]:
        """List all the available attributes for the build.

        Returns:
            list[str]
        """
        return MK8DeluxeBuilds.getAvailableRankingAttributes()

    @property
    def weights(self) -> dict[str, float]:
        """Return all the weights used for the scoring of the builds.

        Returns:
            dict[str, float]
        """
        return self._weights
