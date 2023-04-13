from abc import ABC

from .entities import NamedBuild


class AbstractPrinter(ABC):
    @classmethod
    def print(cls, named_builds: list[NamedBuild]) -> str:
        raise NotImplementedError

    @classmethod
    def printCSV(cls, named_builds: list[NamedBuild]) -> str:
        raise NotImplementedError

    @classmethod
    def printJSON(cls, named_builds: list[NamedBuild]) -> str:
        raise NotImplementedError

    @classmethod
    def printJSONPretty(cls, named_builds: list[NamedBuild]) -> str:
        raise NotImplementedError

    @classmethod
    def printMarkdown(cls, named_builds: list[NamedBuild]) -> str:
        raise NotImplementedError

    @classmethod
    def printTOML(cls, named_builds: list[NamedBuild]) -> str:
        raise NotImplementedError


class BuildsPrinter(AbstractPrinter):
    @classmethod
    def printCSV(cls, named_builds: list[NamedBuild]) -> str:
        for x, b in enumerate(named_builds):
            if x == 0:
                print(b.csvHeader())
            print(b.csv)

    @classmethod
    def printJSON(cls, named_builds: list[NamedBuild]) -> str:
        print(f"[{', '.join([b.json for b in named_builds])}")

    @classmethod
    def printJSONPretty(cls, named_builds: list[NamedBuild]) -> str:
        print(f"[{', '.join([b.toJSON(indent=2) for b in named_builds])}")

    @classmethod
    def printMarkdown(cls, named_builds: list[NamedBuild]) -> str:
        for x, b in enumerate(named_builds):
            if x == 0:
                print(b.markdownHeader())
            print(b.markdown)

    @classmethod
    def getPrinters(cls) -> dict[str, callable]:
        return {
            "csv": cls.printCSV,
            "json": cls.printJSON,
            "json-pretty": cls.printJSONPretty,
            "markdown": cls.printMarkdown,
            "toml": cls.printTOML,
        }
