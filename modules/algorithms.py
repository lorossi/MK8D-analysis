"""This module contains the algorithms used to rank builds."""
from __future__ import annotations

import random
from datetime import datetime

from modules.entities import NamedBuild


class Algorithms:
    """This class contains the algorithms used to rank builds."""

    def __init__(self) -> Algorithms:
        """Initialize the algorithms.

        Returns:
            Algorithms
        """
        self._algorithms = {
            "topk": self._topk,
            "skyline": self._skyline,
            "kmeans": self._kmeans,
            "medrank": self._medrank,
        }

        self._current_algorithm = None

    def setAlgorithm(self, algorithm: str):
        """Set the algorithm to use.

        Args:
            algorithm (str)
        """
        if algorithm not in self._algorithms:
            raise ValueError(f"Algorithm {algorithm} not supported")

        self._current_algorithm = self._algorithms[algorithm]

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
        attributes = [k for k, v in kwargs["rank_attributes"].items() if v is True]
        w: set[NamedBuild] = set()

        for p in builds:
            if any(pp.dominate(p, attributes) for pp in w):
                continue
            w.add(p)

        return list(w)

    def _kmeans(self, builds: list[NamedBuild], **kwargs) -> list[NamedBuild]:
        if seed := kwargs.get("seed") is None:
            seed = datetime.now()

        if limit := kwargs.get("limit") is None:
            limit = 5

        random.seed(seed)

        attributes = [k for k, v in kwargs["rank_attributes"] if v is True]
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
        raise NotImplementedError

    @property
    def available_algorithms(self) -> list[str]:
        """Get the available algorithms.

        Returns:
            list[str]
        """
        return list(self._algorithms.keys())

    @property
    def current_algorithm(self) -> str:
        """
        Get the current algorithm.

        Returns:
            str
        """
        return self._current_algorithm
