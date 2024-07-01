"""This module contains the code to create the builds with part names instead of ids,  \
as they are saved in the database.

The class offers the ability to sort, filter and score each of them.
"""

import argparse

from modules.algorithms import AlgorithmName
from modules.builds_printer import BuildsPrinter
from modules.command_parsers import (
    AttributesParser,
    FilterParser,
    SortParser,
    WeightParser,
)
from modules.database import MK8DeluxeBuilds


def find(parameters: argparse.Namespace) -> None:
    """Run the main function for the create named builds script."""
    m = MK8DeluxeBuilds()

    if parameters.list_filters:
        print(MK8DeluxeBuilds.available_filters)
        return
    if parameters.list_sort_orders:
        print(MK8DeluxeBuilds.available_sorts_orders)
        return
    if parameters.list_weights:
        print(MK8DeluxeBuilds.available_weights)
        return
    if parameters.list_ranking_attributes:
        print(MK8DeluxeBuilds.available_ranking_attributes)
        return

    if parameters.query_filters is not None:
        for key, value in parameters.query_filters.items():
            setattr(m, key, value)

    if parameters.query_sort is not None:
        for key, value in parameters.query_sort.items():
            setattr(m, key, value)

    if parameters.query_weights is not None:
        for key, value in parameters.query_weights.items():
            setattr(m, key, value)

    if parameters.ranking_attributes is not None:
        for key, value in parameters.ranking_attributes.items():
            setattr(m, key, value)

    # use m.limit to set the maximum number of results to return
    m.limit = parameters.limit

    # builds can be either be scored (and then accessed via m.scored_named_builds)
    # or the best builds can be computed via the various implemented algorithms
    # (skyline, topk, kmeans, medrank)
    if parameters.skyline:
        m.algorithm = AlgorithmName.SKYLINE
    elif parameters.topk:
        m.algorithm = AlgorithmName.TOPK
    elif parameters.k_means:
        m.algorithm = AlgorithmName.KMEANS
    elif parameters.medrank:
        m.algorithm = AlgorithmName.MEDRANK

    builds = m.sortBuilds()

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
    """Run the main function for the find builds script."""
    # start the argument parser
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

    list_parser.add_argument(
        "--list-ranking-attributes",
        action="store_true",
        help="List the available ranking attributes.",
    )

    # parser group for mode output
    output_parser = parser.add_mutually_exclusive_group(required=False)
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
    algorithm_parser = parser.add_mutually_exclusive_group(required=False)
    algorithm_parser.add_argument(
        "--topk",
        action="store_true",
        help="Find the builds according to their score, using the top-k algorithm.",
    )

    algorithm_parser.add_argument(
        "--skyline",
        action="store_true",
        help="Find the builds according to the BNL algorithm.",
    )

    algorithm_parser.add_argument(
        "--k-means",
        action="store_true",
        help="Find the builds according to the K-Means algorithm.",
    )

    algorithm_parser.add_argument(
        "--medrank",
        action="store_true",
        help="Find the builds according to the MedRank algorithm.",
    )

    # parser group for query parameters
    parameters_parser = parser.add_argument_group("Query parameters")
    parameters_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Limit the number of results to return.",
    )

    parameters_parser.add_argument(
        "--query-filters",
        nargs="+",
        help="Filters to apply to the query.",
        action=FilterParser,
    )

    parameters_parser.add_argument(
        "--query-sort",
        nargs="+",
        help="Sorting order to apply to the query.",
        action=SortParser,
    )

    parameters_parser.add_argument(
        "--query-weights",
        nargs="+",
        help="Weights to apply to the query.",
        action=WeightParser,
    )

    parameters_parser.add_argument(
        "--ranking-attributes",
        nargs="+",
        help="Attributes to apply to the ranked query.",
        action=AttributesParser,
    )

    args = parser.parse_args()

    find(args)


if __name__ == "__main__":
    main()
