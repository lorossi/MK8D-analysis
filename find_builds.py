"""This module contains the code to create the builds with part names instead of ids,  \
as they are saved in the database.

The class offers the ability to sort, filter and score each of them.
"""
import argparse


from modules.database import MK8DeluxeBuilds
from modules.builds_printer import BuildsPrinter
from modules.command_parsers import (
    FilterParser,
    SortParser,
    WeightParser,
)


def find(parameters: argparse.Namespace) -> None:
    """Run the main function for the create named builds script."""

    if parameters.list_filters:
        print(MK8DeluxeBuilds.getAvailableFilters())
        return
    if parameters.list_sort_orders:
        print(MK8DeluxeBuilds.getAvailableSortOrders())
        return
    if parameters.list_weights:
        print(MK8DeluxeBuilds.getAvailableWeights())
        return

    m = MK8DeluxeBuilds()
    # use m.available_filters or MK8DeluxeBuilds.getAvailableFilters() to get a
    # list of available filters
    # assign the value to the corresponding attribute of the MK8DeluxeBuilds object
    if parameters.query_filters is not None:
        for key, value in parameters.query_filters.items():
            setattr(m, key, value)

    # use m.available_sorts_order or MK8DeluxeBuilds.getAvailableSortOrders() to get a
    # list of available sort options
    # assign the value to the corresponding attribute of the MK8DeluxeBuilds object
    # -1 to sort descending, 1 to sort ascending
    if parameters.query_sort is not None:
        for key, value in parameters.query_sort.items():
            setattr(m, key, value)

    if parameters.query_weights is not None:
        for key, value in parameters.query_weights.items():
            setattr(m, key, value)

    # use m.limit to set the maximum number of results to return
    m.limit = parameters.limit

    # builds can be either be scored (and then accessed via m.scored_named_builds)
    # or the best builds can be computed via the BNL algorithm (for skyline queries,
    # check the readme for more info)

    if parameters.dominating:
        builds = m.dominating_named_builds
    elif parameters.score:
        builds = m.scored_named_builds

    # use the BuildsPrinter class to print the builds
    if parameters.csv:
        BuildsPrinter.printCSV(builds)
    elif parameters.json:
        BuildsPrinter.printJSON(builds)
    elif parameters.json_pretty:
        BuildsPrinter.printJSONPretty(builds)
    elif parameters.markdown:
        BuildsPrinter.printMarkdown(builds)
    elif parameters.toml:
        BuildsPrinter.printTOML(builds)
    else:
        for x, b in enumerate(builds):
            print(f"{x}: {b}")


def main():
    parser = argparse.ArgumentParser(
        "Find builds",
        description="Find builds with the specified parameters.",
    )

    # parser group for listing available filters and sort orders
    list_parser = parser.add_mutually_exclusive_group(required=False)
    list_parser.add_argument(
        "--list-filters",
        action="store_true",
        help="List the available filters.",
    )

    list_parser.add_argument(
        "--list-sort-orders",
        action="store_true",
        help="List the available sort orders.",
    )

    list_parser.add_argument(
        "--list-weights",
        action="store_true",
        help="List the available weights.",
    )

    # parser group for query options
    query_parser = parser.add_argument_group("Query options")

    # parser group for mode output
    output_parser = query_parser.add_mutually_exclusive_group(required=False)
    output_parser.add_argument(
        "--csv",
        action="store_true",
        help="Print the builds in CSV format.",
    )

    output_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the builds in JSON format.",
    )

    output_parser.add_argument(
        "--json-pretty",
        action="store_true",
        help="Print the builds in JSON format with indentation.",
    )

    output_parser.add_argument(
        "--markdown",
        action="store_true",
        help="Print the builds in Markdown format.",
    )

    output_parser.add_argument(
        "--toml",
        action="store_true",
        help="Print the builds in TOML format.",
    )

    # parser group for query algorithm
    algorithm_parser = query_parser.add_mutually_exclusive_group(required=False)
    algorithm_parser.add_argument(
        "--score",
        action="store_true",
        default=True,
        help="Find the builds according to their scores (default).",
    )

    algorithm_parser.add_argument(
        "--dominating",
        action="store_true",
        help="Find the builds according to the BNL algorithm.",
    )

    # parser group for query parameters
    parameters_parser = query_parser.add_argument_group("Query parameters")
    parameters_parser.add_argument(
        "--limit",
        type=int,
        required=True,
        help="Limit the number of results to return.",
    )

    parameters_parser.add_argument(
        "--query-filters",
        dest="query_filters",
        nargs="+",
        help="Filters to apply to the query.",
        action=FilterParser,
    )

    parameters_parser.add_argument(
        "--query-sort",
        dest="query_sort",
        nargs="+",
        help="Sorting order to apply to the query.",
        action=SortParser,
    )

    parameters_parser.add_argument(
        "--query-weights",
        dest="query_weights",
        nargs="+",
        help="Weights to apply to the query.",
        action=WeightParser,
    )

    args = parser.parse_args()

    find(args)


if __name__ == "__main__":
    main()
