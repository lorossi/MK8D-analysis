"""Builds Printer Module."""

import tomllib

from .entities import NamedBuild


class BuildsPrinter:
    """Class for printing builds."""

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
        print(f"[{', '.join([b.json_pretty for b in named_builds])}")

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
    def printTOML(cls, named_builds: list[NamedBuild]) -> None:
        """Print the builds as TOML.

        Args:
            named_builds (list[NamedBuild])
        """
        print(tomllib.dumps([b.toDict() for b in named_builds]))

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
