"""
Advent of Code 2020: Day 17
https://adventofcode.com/2020/day/17
"""

from itertools import product
from typing import List, Set, Tuple

# vector
Site3d = Tuple[int, int, int]
Site4d = Tuple[int, int, int, int]
# active sites
Grid3d = Set[Site3d]
Grid4d = Set[Site4d]


def neighbors_3d(v: Site3d) -> List[Site3d]:
    x, y, z = v
    return [
        (x + a, y + b, z + c)
        for (a, b, c) in product((-1, 0, 1), repeat=3)
        if (a, b, c) != (0, 0, 0)
    ]


def process_site_3d(grid: Grid3d, new_grid: Grid3d, v: Site3d):
    # check inactive neighbors_3d to see if they should become active, since inactive sites aren't kept in grid
    for nbr in neighbors_3d(v):
        if (
            nbr not in grid
            and sum(nbr_nbr in grid for nbr_nbr in neighbors_3d(nbr)) == 3
        ):
            new_grid.add(nbr)
    # check if v should stay active
    if sum(nbr in grid for nbr in neighbors_3d(v)) in (2, 3):
        new_grid.add(v)


def update_3d(grid: Grid3d) -> Grid3d:
    new_grid: Grid3d = set()
    for v in grid:
        process_site_3d(grid, new_grid, v)
    return new_grid


def parse_grid_3d(s: str) -> Grid3d:
    """Parse from string representing a 2d slice.
    """
    ss = s.strip().split("\n")
    M, N = len(ss), len(ss[0])
    grid: Grid3d = set()
    for (i, j) in product(range(M), range(N)):
        if ss[i][j] == "#":
            site: Site3d = (i, j, 0)
            grid.add(site)
    return grid


#############


def neighbors_4d(v: Site4d) -> List[Site4d]:
    x, y, z, w = v
    return [
        (x + a, y + b, z + c, w + d)
        for (a, b, c, d) in product((-1, 0, 1), repeat=4)
        if (a, b, c, d) != (0, 0, 0, 0)
    ]


def process_site_4d(grid: Grid4d, new_grid: Grid4d, v: Site4d):
    # check inactive neighbors to see if they should become active, since inactive sites aren't kept in grid
    for nbr in neighbors_4d(v):
        if (
            nbr not in grid
            and sum(nbr_nbr in grid for nbr_nbr in neighbors_4d(nbr)) == 3
        ):
            new_grid.add(nbr)
    # check if v should stay active
    if sum(nbr in grid for nbr in neighbors_4d(v)) in (2, 3):
        new_grid.add(v)


def update_4d(grid: Grid4d) -> Grid4d:
    new_grid: Grid4d = set()
    for v in grid:
        process_site_4d(grid, new_grid, v)
    return new_grid


def parse_grid_4d(s: str) -> Grid4d:
    """Parse from string representing a 2d slice.
    """
    ss = s.strip().split("\n")
    M, N = len(ss), len(ss[0])
    grid: Grid4d = set()
    for (i, j) in product(range(M), range(N)):
        if ss[i][j] == "#":
            site: Site4d = (i, j, 0, 0)
            grid.add(site)
    return grid


#############

s_input = """
####...#
......#.
#..#.##.
.#...#.#
..###.#.
##.###..
.#...###
.##....#
""".strip()


if __name__ == "__main__":
    grid = parse_grid_3d(s_input)
    for rep in range(6):
        grid = update_3d(grid)
    print(len(grid))

    grid2 = parse_grid_4d(s_input)
    for rep in range(6):
        grid2 = update_4d(grid2)
    print(len(grid2))
