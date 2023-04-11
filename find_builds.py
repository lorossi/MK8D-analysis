"""This module contains the code to create the builds with part names instead of ids,  \
as they are saved in the database.

The class offers the ability to sort, filter and score each of them.
"""
from sys import argv
from modules.database import MK8DeluxeBuilds


def gather_parameters(argv: list) -> dict:
    """Gather the parameters from the command line and return them as a dictionary."""
    if "-h" in argv:
        print(
            "Usage: python3 find_builds.py "
            "[--csv] [--json] [--json-pretty] [--markdown]"
        )
        return None

    params = {}
    params["csv"] = "--csv" in argv
    params["json"] = "--json" in argv
    params["json_pretty"] = "--json-pretty" in argv
    params["markdown"] = "--markdown" in argv

    if sum(1 for v in params.values() if v) > 1:
        print("Only one format can be specified.")
        return None

    params["default"] = not any(params.values())

    return params


def main(parameters: dict[str, bool]) -> None:
    """Run the main function for the create named builds script."""
    m = MK8DeluxeBuilds()
    # use m.available_filters to get a list of available filters
    # assign the value to the corresponding attribute of the MK8DeluxeBuilds object
    m.min_ground_speed = 12
    m.min_acceleration = 12
    m.min_miniturbo = 5

    # use m.available_sorts_order to get a list of available sort options
    # assign the value to the corresponding attribute of the MK8DeluxeBuilds object
    # -1 to sort descending, 1 to sort ascending
    m.sort_score = -1
    m.sort_score_dev = 1
    m.sort_miniturbo = -1

    # the weights are used to calculate the score as a weighted average
    #   of the parts attributes
    # use m.available_weights to get a list of available weights options
    # assign the value to the corresponding attribute of the MK8DeluxeBuilds object
    # the default value is 0.5 for ground_speed and acceleration while
    # all the other weights are 0
    m.weight_ground_speed = 0.5
    m.weight_acceleration = 0.4
    m.weight_miniturbo = 0.1

    # use m.limit to set the maximum number of results to return
    m.limit = 5

    for x, b in enumerate(m.named_builds):
        match parameters:
            case {"csv": True}:
                if x == 0:
                    print(b.csvHeader())
                print(b.csv)
            case {"json": True}:
                print(b.json)
            case {"json_pretty": True}:
                print(b.toJSON(indent=4))
            case {"markdown": True}:
                if x == 0:
                    print(b.markdownHeader())
                print(b.markdown)
            case {"default": True}:
                print(b)


if __name__ == "__main__":
    parameters = gather_parameters(argv)
    if parameters:
        main(parameters)
