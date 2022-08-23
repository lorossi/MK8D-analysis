from constants import EntityId, COLUMN_IDS, VARIABLES


class Entity:
    def __init__(self, entity_id: EntityId, **kwargs) -> None:
        self.entity_id = entity_id
        self.name = kwargs.get("name")

        for v in VARIABLES:
            self.__setattr__(v, kwargs.get(v, 0))

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

        kwargs = self._sumAttributes(other)
        return Build(**kwargs)

    def _sumAttributes(self, other: object) -> dict[str, int | str]:
        common = set(self.__dict__.keys()) & set(other.__dict__.keys())

        kwargs = {}

        for k in common:
            if k in COLUMN_IDS:
                continue

            if isinstance(self.__dict__[k], int) or isinstance(other.__dict__[k], int):
                kwargs[k] = self.__dict__[k] + other.__dict__[k]
            elif isinstance(self.__dict__[k], str) or isinstance(
                other.__dict__[k], str
            ):
                kwargs[k] = self.__dict__[k] + " - " + other.__dict__[k]

        return kwargs

    def toCSV(self) -> str:
        return ",".join(str(v) for v in self.__dict__.values())

    def getCSVCols(self) -> str:
        return ",".join(str(v) for v in self.__dict__.keys())


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

    def _sumAttributes(self, other: object) -> dict[str, int | str]:
        return super()._sumAttributes(other)


class SlimComponent(Entity):
    def __init__(self, entity_id: EntityId, **kwargs) -> None:
        self.entity_id = entity_id
        for v in VARIABLES:
            self.__setattr__(v, kwargs.get(v, 0))

        for v in COLUMN_IDS:
            self.__setattr__(v, kwargs.get(v, None))

    def _addIds(self, *others: list[object]) -> dict[str, int]:
        ids = ["driver_id", "vehicle_id", "tyre_id", "glider_id"]
        for i in ids:
            for o in others:
                if (v := o.__getattribute__(i)) is not None:
                    self.__setattr__(i, v)

    def __add__(self, other: object):
        if all(
            not isinstance(other, c)
            for c in [SlimDriver, SlimVehicle, SlimTyre, SlimGlider, SlimBuild]
        ):
            raise TypeError(
                f"unsupported operand type(s) for +: "
                f"'{self.__class__.__name__}' and '{type(other)}'"
            )

        kwargs = self._sumAttributes(other)

        new_build = SlimBuild(**kwargs)
        new_build._addIds(self, other)
        return new_build


class SlimDriver(SlimComponent):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.DRIVER, **kwargs)


class SlimVehicle(SlimComponent):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.VEHICLE, **kwargs)


class SlimTyre(SlimComponent):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.TYRE, **kwargs)


class SlimGlider(SlimComponent):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.GLIDER, **kwargs)


class SlimBuild(SlimComponent):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(entity_id=EntityId.SLIM_BUILD, **kwargs)
        for i in COLUMN_IDS:
            self.__setattr__(i, None)
