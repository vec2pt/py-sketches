"""
20230808

Travelling salesman problem (Recursion solution)

Links:
    https://en.wikipedia.org/wiki/Travelling_salesman_problem
"""

import math
import random

import matplotlib.pyplot as plt


def distance2pt(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


class TravellingSalesmanProblem:
    def __init__(self, points) -> None:
        self._points = points
        self._minimum_distance = math.inf
        self._minimum_path = []

    @property
    def minimum_distance(self) -> float:
        return self._minimum_distance

    @property
    def minimum_path(self) -> list:
        return self._minimum_path

    def _recursion_solution(self, point, distance, input_ls, output_ls=None):
        if output_ls is None:
            output_ls = []
        if input_ls:
            for i in input_ls:
                new_input_ls = input_ls.copy()
                new_input_ls.remove(i)
                self._recursion_solution(
                    i,
                    distance + distance2pt(point, i),
                    new_input_ls,
                    output_ls + [i],
                )
        else:
            new_distance = distance + distance2pt(point, self._points[0])
            if new_distance < self._minimum_distance:
                self._minimum_distance = new_distance
                self._minimum_path = (
                    [self._points[0]] + output_ls + [self._points[0]]
                )

    def calculate(self):
        self._recursion_solution(self._points[0], 0, self._points[1:])


if __name__ == "__main__":
    pts = [[random.random(), random.random()] for _ in range(10)]

    tsp = TravellingSalesmanProblem(pts)
    tsp.calculate()

    plt.plot(*zip(*tsp.minimum_path), marker="o", color="r")
    plt.show()
