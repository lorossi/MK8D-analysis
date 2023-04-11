from __future__ import annotations

from argparse import Action, ArgumentParser, Namespace
from typing import Any, Sequence

from .database import MK8DeluxeBuilds


class CommandParser(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Sequence[Any],
        dest: str = None,
        option_string: str = None,
    ) -> None:
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")

            if not self.validateValue(value):
                raise ValueError(f"Value {value} is not valid")

            if not self.validateKey(key):
                raise ValueError(f"Key {key} is not valid")

            getattr(namespace, self.dest)[key] = float(value)

    def validateValue(self, value: str) -> bool:
        raise NotImplementedError

    def validateKey(self, key: str) -> bool:
        raise NotImplementedError


class FilterParser(CommandParser):
    def __call__(self, *args: Any):
        super().__call__(
            *args,
        )

    def validateValue(self, value: str) -> bool:
        try:
            int(value)
        except ValueError:
            return False

        return True

    def validateKey(self, key: str) -> bool:
        return key in MK8DeluxeBuilds.getAvailableFilters()


class SortParser(CommandParser):
    def __call__(self, *args: Any):
        super().__call__(
            *args,
        )

    def validateValue(self, value: str) -> bool:
        return value in ["1", "-1"]

    def validateKey(self, key: str) -> bool:
        return key in MK8DeluxeBuilds.getAvailableSortOrders()


class WeightParser(CommandParser):
    def __call__(self, *args: Any):
        super().__call__(
            *args,
        )

    def validateValue(self, value: str) -> bool:
        try:
            float(value)
        except ValueError:
            return False

        return True

    def validateKey(self, key: str) -> bool:
        return key in MK8DeluxeBuilds.getAvailableWeights()
