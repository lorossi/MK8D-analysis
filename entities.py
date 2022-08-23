from statistics import stdev
from constants import EntityId, PARTS_ATTRIBUTES, ID_ATTRIBUTES

from ujson import dumps


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
        return ",".join(self.getCols())

    def getCols(self) -> list[str]:
        return [k for k in self.__dict__.keys() if not k.startswith("_")]

    def getRow(self) -> list[str | int]:
        return [self.__getattribute__(k) for k in self.getCols()]


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

        self._weights = {k: 0 for k in PARTS_ATTRIBUTES}
        self._weights["ground_speed"] = 0.5
        self._weights["acceleration"] = 0.5

    def __str__(self) -> str:
        return f"('score': {self.score}), ('stdev': {self.score_dev}), " + ", ".join(
            str(a) for a in self.__dict__.items()
        )

    def toJSON(self, indent=0, sort_keys=False) -> str:
        json_dict = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        json_dict["score"] = self.score
        json_dict["score_dev"] = self.score_dev
        return dumps(json_dict, indent=indent, sort_keys=sort_keys)

    @property
    def score(self) -> float:
        items = set(self.__dict__.keys()) & set(PARTS_ATTRIBUTES)
        return sum(self._weights[v] * self.__getattribute__(v) for v in list(items))

    @property
    def score_dev(self) -> float:
        return stdev(
            [self.__dict__[k] for k in PARTS_ATTRIBUTES if self._weights[k] != 0]
        )

    @property
    def weights(self) -> dict[str, float]:
        return self._weights

    @weights.setter
    def weights(self, w: dict[str, float]) -> None:
        if sum(w.values()) != 1:
            raise ValueError("weights must sum to 1")

        for k, v in w.items():
            if k not in PARTS_ATTRIBUTES:
                raise ValueError(f"{w} is not a valid weight")
            if not isinstance(k, float):
                raise TypeError(f"{w} is not a valid weight")
            if v < 0 or v > 1:
                raise ValueError(f"{w} is not a valid weight")

        for k, v in w.items():
            self._weights[k] = v
