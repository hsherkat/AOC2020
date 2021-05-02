"""
Advent of Code 2020: Day 3
https://adventofcode.com/2020/day/3
"""

from itertools import islice, chain, count
from math import prod
from typing import List


def location_gen(ground_map: List[str], slope_over: int, slope_down: int):
    return zip(islice(ground_map, None, None, slope_down), count(0, slope_over))


def tree_here(row: str, loc: int) -> bool:
    return row[loc % len(row)] == "#"


def tree_count(ground_map: List[str], slope_over: int, slope_down: int) -> int:
    locations = location_gen(ground_map, slope_over, slope_down)
    return sum(tree_here(row, loc) for row, loc in locations)


##################

with open("input_3.txt") as f:
    x_input = [row.strip() for row in f]


if __name__ == "__main__":
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    results = [tree_count(x_input, over, down) for (over, down) in slopes]
    print(results[1])
    print(prod(results))
