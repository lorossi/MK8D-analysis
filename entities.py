"""This module contains the classes for the entities in the program."""

from __future__ import annotations
from ujson import dumps
from statistics import stdev

from constants import EntityId, PARTS_ATTRIBUTES, ID_ATTRIBUTES


class Entity:
    """Single entity used in the program. It can be a driver, a vehicle, a tyre or a glider."""

    def __init__(self, entity_id: EntityId, **kwargs) -> None:
        """Initialize the entity.

        Args:
            entity_id (EntityId): The id of the entity.
        """
        self._entity_id = entity_id

        for v in PARTS_ATTRIBUTES:
            self.__setattr__(v, kwargs.get(v, 0))

        for i in ID_ATTRIBUTES:
            self.__setattr__(i, kwargs.get(i, None))

    def __str__(self) -> str:
        """Return the string representation of the entity.

        Returns:
            str
        """
        return ", ".join(
            str(a) for a in self.__dict__.items() if not a[0].startswith("_")
        )

    def __repr__(self) -> str:
        """Return the string representation of the entity.

        Returns:
            str
        """
        return self.__str__()

    def __add__(self, other: object) -> Build:
        """Dunder method for the addition of two entities.

        Args:
            other (object): The other entity.

        Raises:
            TypeError: If the other entity is not an Entity.

        Returns:
            Build: The build created from the addition.
        """
        if not isinstance(other, Entity):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{self.__class__.__name__}' and '{type(other)}'"
            )

        kwargs = self._addAttributes(other)
        return Build(**kwargs)

    def _addAttributes(self, other: Entity) -> dict[str, int | str]:
        """Add the attributes of the other entity to the current entity.

        Args:
            other (Entity): The other entity.

        Returns:
            dict[str, int | str]: dict of kwargs for the new build.
        """
        # get common attributes
        common = set(self.__dict__.keys()) & set(other.__dict__.keys()) - set(
            ID_ATTRIBUTES
        )

        kwargs = {}

        # sum the common attributes
        for k in common:
            if isinstance(self.__dict__[k], int) or isinstance(other.__dict__[k], int):
                kwargs[k] = self.__dict__[k] + other.__dict__[k]

        # get the id attributes
        for i in ID_ATTRIBUTES:
            if self.__getattribute__(i) is None:
                if other.__getattribute__(i) is not None:
                    # if the current entity has no id, but the other has, use the other's id
                    kwargs[i] = other.__getattribute__(i)
            else:
                # otherwise, use the current entity's id
                kwargs[i] = self.__getattribute__(i)

        return kwargs

    @property
    def csv(self) -> str:
        """Return the csv representation of the entity.

        Returns:
            str: comma separated values.
        """
        return ",".join(
            str(v) for k, v in self.__dict__.items() if not k.startswith("_")
        )

    @property
    def csv_cols(self) -> str:
        """Return the csv columns of the entity.

        Returns:
            str: comma separated values.
        """
        return ",".join(self.cols)

    @property
    def cols(self) -> list[str]:
        """Return the columns of the entity.

        Returns:
            list[str]
        """
        return [k for k in self.__dict__.keys() if not k.startswith("_")]

    @property
    def rows(self) -> list[str | int]:
        """Return the rows of the entity.

        Returns:
            list[str | int]
        """
        return [self.__getattribute__(k) for k in self.cols]


class Part(Entity):
    def __init__(self, entity_id: EntityId, **kwargs) -> None:
        super().__init__(entity_id, **kwargs)


class PartFactory:
    """Factory for the parts."""

    def __init__(self, entity_id: EntityId) -> None:
        """Build a new part factory.

        Args:
            entity_id (EntityId): The id of the part.
        """
        self._entity_id = entity_id

    def build(self, **kwargs) -> Entity:
        """Create a new part.

        Returns:
            Entity: The new part.
        """
        return Part(self._entity_id, **kwargs)


class Build(Entity):
    """Class for a build."""

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the build."""
        super().__init__(entity_id=None, **kwargs)


class NamedBuild:
    """Class for a named build.
    Instead of having ids for the parts, it has the corresponding names."""

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the named build.

        Raises:
            ValueError: If any of the args is an id.
        """
        if any(k.endswith("_id") for k in kwargs.keys()):
            raise ValueError("NamedBuild cannot have an id")

        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __str__(self) -> str:
        """Return the string representation of the named build.

        Returns:
            str
        """
        return f"('score': {self.score}), ('stdev': {self.score_dev}), " + ", ".join(
            str(a) for a in self.__dict__.items() if not a[0].startswith("_")
        )

    def toJSON(self, indent=0, sort_keys=False) -> str:
        """Return the JSON representation of the named build.

        Args:
            indent (int, optional): Indentation of the lines. Defaults to 0.
            sort_keys (bool, optional). Defaults to False.

        Returns:
            str
        """
        json_dict = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        json_dict["score"] = self.score
        json_dict["score_dev"] = self.score_dev
        return dumps(json_dict, indent=indent, sort_keys=sort_keys)

    @property
    def json(self) -> str:
        """Return the JSON representation of the named build.

        Returns:
            str: JSON representation.
        """
        return self.toJSON(indent=0, sort_keys=True)

    @property
    def score(self) -> float:
        """Return the score of the named build.

        Returns:
            float
        """
        items = set(self.__dict__.keys()) & set(PARTS_ATTRIBUTES)
        return sum(
            self._weights[v] * self.__getattribute__(v) for v in list(items)
        ) / sum(self._weights.values())

    @property
    def score_dev(self) -> float:
        """Return the score deviation of the named build.

        The deviation is calculated with respect to the considered parameters.

        Returns:
            float
        """
        return stdev(
            [self.__dict__[k] for k in PARTS_ATTRIBUTES if self._weights[k] != 0]
        )
