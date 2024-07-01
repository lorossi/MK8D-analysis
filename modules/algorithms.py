"""This module contains the algorithms used to rank builds."""

from __future__ import annotations

import random
from enum import Enum
from time import time

from modules.entities import NamedBuild


class AlgorithmName(Enum):
    """Name of the algorithms available."""

    TOPK = "topk"
    SKYLINE = "skyline"
    KMEANS = "kmeans"
    MEDRANK = "medrank"


class Algorithms:
    """This class contains the algorithms used to rank builds."""

    def __init__(self) -> Algorithms:
        """Initialize the algorithms.

        Returns:
            Algorithms
        """
        self._algorithms = {
            AlgorithmName.TOPK.value: self._topk,
            AlgorithmName.SKYLINE.value: self._skyline,
            AlgorithmName.KMEANS.value: self._kmeans,
            AlgorithmName.MEDRANK.value: self._medrank,
        }

        self._current_algorithm = None

    def setAlgorithm(self, algorithm: AlgorithmName) -> None:
        """Set the algorithm to use.

        Args:
            algorithm (AlgorithmName)
        """
        self._current_algorithm = self._algorithms[algorithm.value]

    def runAlgorithm(self, builds: list[NamedBuild], **kwargs) -> list[NamedBuild]:
        """Run the algorithm.

        Args:
            builds (list[NamedBuild])

        Returns:
            list[NamedBuild]
        """
        if self._current_algorithm is None:
            raise ValueError("No algorithm set")

        return self._current_algorithm(builds, **kwargs)

    def _topk(self, builds: list[NamedBuild], **kwargs) -> list[NamedBuild]:
        for f in kwargs["sort"][::-1]:
            builds.sort(key=lambda x: x.__getattribute__(f[0]), reverse=f[1])

        if kwargs.get("limit") is not None:
            builds = builds[: kwargs["limit"]]

        return builds

    def _skyline(self, builds: list[NamedBuild], **kwargs) -> list[NamedBuild]:
        attributes = [k for k, v in kwargs["rank_attributes"].items() if v]
        w: set[NamedBuild] = set()

        for p in builds:
            if any(pp.dominate(p, attributes) for pp in w):
                continue
            w.add(p)

        return list(w)

    def _kmeans(self, builds: list[NamedBuild], **kwargs) -> list[NamedBuild]:
        seed = kwargs.get("seed", time())
        limit = kwargs.get("limit", 5)

        random.seed(seed)

        attributes = [k for k, v in kwargs["rank_attributes"].items() if v]
        centroids = random.sample(builds, limit)

        while True:
            new_centroids = []
            for c in centroids:
                closest = min(builds, key=lambda x: c.distance(x, attributes))
                new_centroids.append(closest)

            if new_centroids == centroids:
                break

            centroids = new_centroids

        return centroids

    def _medrank(self, builds: list[NamedBuild], **kwargs) -> list[NamedBuild]:
        limit = kwargs.get("limit", 5)
        attributes = [k for k, v in kwargs["rank_attributes"].items() if v]
        lists = [[] for _ in range(len(attributes))]
        sorted_builds = []

        for x, a in enumerate(attributes):
            lists[x] = sorted(builds, key=lambda x: x.__getattribute__(a), reverse=True)

        for x, b in enumerate(builds):
            positions = [len(builds) for _ in range(len(attributes))]
            for y, a in enumerate(attributes):
                # get the position of the build in the list
                positions[y] = lists[y].index(b)

            # get the median position
            median = sorted(positions)[len(positions) // 2]
            sorted_builds.append((median, b))

        sorted_builds.sort(key=lambda x: x[0], reverse=True)

        return [b for _, b in sorted_builds[:limit]]
