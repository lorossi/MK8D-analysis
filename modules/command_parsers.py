"""Command parsers for the command line interface."""

from __future__ import annotations

from argparse import Action, ArgumentParser, Namespace
from typing import Any, Sequence

from .database import MK8DeluxeBuilds


class CommandParser(Action):
    """Base class for command parsers."""

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Sequence[Any],
        dest: str = None,
        option_string: str = None,
    ) -> None:
        """Call the parser."""
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")

            if not self.validateValue(value):
                raise ValueError(f"Value {value} is not valid")

            if not self.validateKey(key):
                raise ValueError(f"Key {key} is not valid")

            getattr(namespace, self.dest)[key] = float(value)

    def validateValue(self, value: str) -> bool:
        """Validate the value of a parameter.

        Args:
            value (str)

        Returns:
            bool
        """
        raise NotImplementedError

    def validateKey(self, key: str) -> bool:
        """Validate the key of a parameter.

        Args:
            key (str)

        Returns:
            bool
        """
        raise NotImplementedError


class FilterParser(CommandParser):
    """Command parser for filters."""

    def __call__(self, *args: Any):
        """Call the parser."""
        super().__call__(*args)

    def validateValue(self, value: str) -> bool:
        """Validate the value of a parameter."""
        try:
            int(value)
        except ValueError:
            return False

        return True

    def validateKey(self, key: str) -> bool:
        """Validate the key of a parameter."""
        return key in MK8DeluxeBuilds.getAvailableFilters()


class SortParser(CommandParser):
    """Command parser for sort orders."""

    def __call__(self, *args: Any):
        """Call the parser."""
        super().__call__(*args)

    def validateValue(self, value: str) -> bool:
        """Validate the value of a parameter."""
        return value in ["1", "-1"]

    def validateKey(self, key: str) -> bool:
        """Validate the key of a parameter."""
        return key in MK8DeluxeBuilds.getAvailableSortOrders()


class WeightParser(CommandParser):
    """Command parser for weights."""

    def __call__(self, *args: Any):
        """Call the parser."""
        super().__call__(*args)

    def validateValue(self, value: str) -> bool:
        """Validate the value of a parameter."""
        try:
            float(value)
        except ValueError:
            return False

        return True

    def validateKey(self, key: str) -> bool:
        """Validate the key of a parameter."""
        return key in MK8DeluxeBuilds.getAvailableWeights()


class AttributesParser(CommandParser):
    """Command parser for ranking attributes."""

    def __call__(self, *args: Any):
        """Call the parser."""
        super().__call__(*args)

    def validateValue(self, value: str) -> bool:
        """Validate the value of a parameter."""
        return value in ["1", "0"]

    def validateKey(self, key: str) -> bool:
        """Validate the key of a parameter."""
        return key in MK8DeluxeBuilds.getAvailableRankingAttributes()
