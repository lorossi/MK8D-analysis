from statistics import stdev
from constants import EntityId, PARTS_ATTRIBUTES, ID_ATTRIBUTES


class Entity:
    def __init__(self, entity_id: EntityId, **kwargs) -> None:
        self._entity_id = entity_id

        for v in PARTS_ATTRIBUTES:
            self.__setattr__(v, kwargs.get(v, 0))

        for i in ID_ATTRIBUTES:
            self.__setattr__(i, kwargs.get(i, None))

    def __str__(self) -> str:
        return ", ".join(
            str(a) for a in self.__dict__.items() if not a[0].startswith("_")
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other: object):
        if not isinstance(other, Entity):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{self.__class__.__name__}' and '{type(other)}'"
            )

        kwargs = self._addAttributes(other)
        return Build(**kwargs)

    def _addAttributes(self, other: object) -> dict[str, int | str]:
        common = set(self.__dict__.keys()) & set(other.__dict__.keys()) - set(
            ID_ATTRIBUTES
        )

        kwargs = {}

        for k in common:
            if isinstance(self.__dict__[k], int) or isinstance(other.__dict__[k], int):
                kwargs[k] = self.__dict__[k] + other.__dict__[k]
            elif isinstance(self.__dict__[k], str) or isinstance(
                other.__dict__[k], str
            ):
                kwargs[k] = self.__dict__[k] + " - " + other.__dict__[k]

        for i in ID_ATTRIBUTES:
            if self.__getattribute__(i) is None:
                if other.__getattribute__(i) is not None:
                    kwargs[i] = other.__getattribute__(i)
            else:
                kwargs[i] = self.__getattribute__(i)

        return kwargs

    def toCSV(self) -> str:
        return ",".join(
            str(v) for k, v in self.__dict__.items() if not k.startswith("_")
        )

    def getCSVCols(self) -> str:
        return ",".join(str(k) for k in self.__dict__.keys() if not k.startswith("_"))


class Part(Entity):
    def __init__(self, entity_id: EntityId, **kwargs) -> None:
        super().__init__(entity_id, **kwargs)


class PartFactory:
    def __init__(self, entity_id: EntityId) -> None:
        self._entity_id = entity_id

    def build(self, **kwargs) -> Entity:
        return Part(self._entity_id, **kwargs)


class Build(Entity):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=None, **kwargs)


class NamedBuild:
    def __init__(self, **kwargs: dict) -> None:
        if any(k.endswith("_id") for k in kwargs.keys()):
            raise ValueError("NamedBuild cannot have an id")

        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __str__(self) -> str:
        return f"('score': {self.score}), ('stdev': {self.score_dev}), " + ", ".join(
            str(a) for a in self.__dict__.items()
        )

    @property
    def score(self) -> float:
        return (self.speed + self.acceleration) / 2

    @property
    def score_dev(self) -> float:
        return stdev([self.speed, self.acceleration])
