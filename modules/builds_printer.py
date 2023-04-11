from ujson import dumps
from .entities import NamedBuild


class BuildsPrinter:
    @classmethod
    def printCSV(cls, named_builds: list[NamedBuild]) -> str:
        for x, b in enumerate(named_builds):
            if x == 0:
                print(b.csvHeader())
            print(b.csv)

    @classmethod
    def printJSON(cls, named_builds: list[NamedBuild]) -> str:
        json_dict = [b.json for b in named_builds]
        print(dumps(json_dict))

    @classmethod
    def printJSONPretty(cls, named_builds: list[NamedBuild]) -> str:
        json_dict = [b.json for b in named_builds]
        print(dumps(json_dict, indent=4))

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
        }
