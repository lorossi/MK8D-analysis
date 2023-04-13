"""Builds Printer Module."""
from abc import ABC

from .entities import NamedBuild


class AbstractPrinter(ABC):
    """Base class for printers."""

    @classmethod
    def print(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as plaintext."""
        raise NotImplementedError

    @classmethod
    def printCSV(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as CSV."""
        raise NotImplementedError

    @classmethod
    def printJSON(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as JSON."""
        raise NotImplementedError

    @classmethod
    def printJSONPretty(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as pretty JSON."""
        raise NotImplementedError

    @classmethod
    def printMarkdown(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as Markdown table."""
        raise NotImplementedError

    @classmethod
    def printTOML(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as TOML."""
        raise NotImplementedError


class BuildsPrinter(AbstractPrinter):
    """Class for printing builds, extends AbstractPrinter."""

    @classmethod
    def printCSV(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as CSV.

        Args:
            named_builds (list[NamedBuild])
        """
        for x, b in enumerate(named_builds):
            if x == 0:
                print(b.csvHeader())
            print(b.csv)

    @classmethod
    def printJSON(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as JSON.

        Args:
            named_builds (list[NamedBuild])
        """
        print(f"[{', '.join([b.json for b in named_builds])}")

    @classmethod
    def printJSONPretty(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as pretty JSON.

        Args:
            named_builds (list[NamedBuild])
        """
        print(f"[{', '.join([b.toJSON(indent=2) for b in named_builds])}")

    @classmethod
    def printMarkdown(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as Markdown table.

        Args:
            named_builds (list[NamedBuild])
        """
        for x, b in enumerate(named_builds):
            if x == 0:
                print(b.markdownHeader())
            print(b.markdown)

    @classmethod
    def getPrinters(cls) -> dict[str, callable]:
        """Get the printers.

        Returns:
            dict[str, callable]: The printers.
        """
        return {
            "csv": cls.printCSV,
            "json": cls.printJSON,
            "json-pretty": cls.printJSONPretty,
            "markdown": cls.printMarkdown,
            "toml": cls.printTOML,
        }
