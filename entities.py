from constants import EntityId, VARIABLES, IDS


class Entity:
    def __init__(self, entity_id: EntityId, **kwargs) -> None:
        self._entity_id = entity_id

        for v in VARIABLES:
            self.__setattr__(v, kwargs.get(v, 0))

        for i in IDS:
            self.__setattr__(i, kwargs.get(i, None))

    def __str__(self) -> str:
        return ", ".join(
            str(a) for a in self.__dict__.items() if not a[0].startswith("_")
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other: object):
        if all(
            not isinstance(other, c) for c in [Driver, Vehicle, Tyre, Glider, Build]
        ):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{self.__class__.__name__}' and '{type(other)}'"
            )

        kwargs = self._addAttributes(other)
        return Build(**kwargs)

    def _addAttributes(self, other: object) -> dict[str, int | str]:
        common = set(self.__dict__.keys()) & set(other.__dict__.keys()) - set(IDS)

        kwargs = {}

        for k in common:
            if isinstance(self.__dict__[k], int) or isinstance(other.__dict__[k], int):
                kwargs[k] = self.__dict__[k] + other.__dict__[k]
            elif isinstance(self.__dict__[k], str) or isinstance(
                other.__dict__[k], str
            ):
                kwargs[k] = self.__dict__[k] + " - " + other.__dict__[k]

        for i in IDS:
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


class Driver(Entity):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.DRIVER, **kwargs)
        self.size = kwargs.get("size")


class Vehicle(Entity):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.VEHICLE, **kwargs)


class Tyre(Entity):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.TYRE, **kwargs)


class Glider(Entity):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.GLIDER, **kwargs)


class Build(Entity):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.BUILD, **kwargs)
