"""
Advent of Code 2020: Day 20
https://adventofcode.com/2020/day/20
"""

from typing import List, Tuple, Dict
import re
from math import sqrt, prod
from time import perf_counter
from itertools import product
import numpy as np


class Tile:
    def __init__(self, num_id: int, image: List[str]):
        self.num_id = num_id
        self.image = image

    @staticmethod
    def from_str(s: str) -> "Tile":
        pattern = r"(\d+)"
        ss = s.split("\n")
        if m := re.search(pattern, ss[0]):
            num_id = int(m.group())
        else:
            raise ValueError("Bad input")
        image = [line.strip() for line in ss[1:]]
        return Tile(num_id, image)

    def top(self):
        return self.image[0]

    def bottom(self):
        return self.image[-1]

    def left(self):
        return "".join([row[0] for row in self.image])

    def right(self):
        return "".join([row[-1] for row in self.image])

    def reorient(self, turns, flip):
        image = self.image[:]
        for _ in range(turns % 4):
            M, N = len(image), len(image[0])
            new_image = [
                "".join([image[row][N - 1 - column] for row in range(M)])
                for column in range(N)
            ]
            image = new_image[:]
        if flip:
            image = [row[::-1] for row in image]
        return Tile(self.num_id, image)

    def orientations(self):
        return (self.reorient(turn, flip) for turn in range(4) for flip in (0, 1))

    def print(self):
        print(self.num_id, "\n" + "-----")
        for row in self.image:
            print(row)
        print("\n")


def acceptable(tile: Tile, current_state: Tuple[Tile, ...], tiles: List[Tile]):
    """Does adding this tile to the current state produce an acceptable state?
    0 1 2
    3 4 _
    _ _ _
    """
    N = int(sqrt(len(tiles)))
    loc = len(current_state)
    if loc % N != 0 and tile.left() != current_state[loc - 1].right():
        return False
    if loc >= N and tile.top() != current_state[loc - N].bottom():
        return False
    return True


def candidates(current_state: Tuple[Tile, ...], tiles: List[Tile]):
    """Go through all the possible oriented tiles to add to the current state.
    """
    return (
        oriented
        for tile in tiles
        if tile.num_id not in [t.num_id for t in current_state]
        for oriented in tile.orientations()
    )


def backtrack(current_state: Tuple[Tile, ...], tiles: List[Tile]):
    if len(current_state) == len(tiles):
        return current_state
    for tile in candidates(current_state, tiles):
        if acceptable(tile, current_state, tiles):
            if solution := backtrack(current_state + (tile,), tiles):
                return solution


def remove_border(tile: Tile) -> List[str]:
    image = tile.image
    new_image = [row[1:-1] for row in image[1:-1]]
    return new_image


DRAGON = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.split(
    "\n"
)


def convert_numerical(image):
    new_image = [[1 if c == "#" else 0 for c in row] for row in image]
    return np.array(new_image)


d_rows, d_cols = len(DRAGON), len(DRAGON[0])
DRAGON_locs = [
    (i, j) for (i, j) in product(range(d_rows), range(d_cols)) if DRAGON[i][j] == "#"
]


def get_joined_image(solution: List[Tile]):
    images = [convert_numerical(remove_border(tile)) for tile in solution]
    N = int(sqrt(len(images)))
    joined = np.vstack([np.hstack(images[N * i : N * i + N]) for i in range(N)])
    return joined


def get_matching_indices(template, image):
    out = set()
    m, n = template.shape
    M, N = image.shape
    template_locs = np.where(template != 0)
    for (i, j) in product(range(M + 1 - m), range(N + 1 - n)):
        shifted_locs = tuple((template_locs[0] + i, template_locs[1] + j))
        if all(image[shifted_locs]):
            out.update(zip(*shifted_locs))
    return out


def part2(joined):
    out = set()
    dragon_tile = Tile(-1, DRAGON)
    oriented_dragons = [convert_numerical(t.image) for t in dragon_tile.orientations()]
    for dragon in oriented_dragons:
        out.update(get_matching_indices(dragon, joined))
    return joined.sum().sum() - len(out)


################

with open("input_20.txt") as f:
    RAW_INPUT = f.read()  # "".join([line for line in f])
    TILES = [Tile.from_str(block) for block in RAW_INPUT.strip().split("\n\n")]

if __name__ == "__main__":
    N = int(sqrt(len(TILES)))
    start = perf_counter()
    solution = backtrack(tuple(), TILES)
    stop = perf_counter()
    corners = [solution[0], solution[N - 1], solution[-N], solution[-1]]
    ids = [int(tile.num_id) for tile in corners]
    out = prod(ids)
    print(out)
    print(f"{stop-start} seconds to backtrack")

    joined = get_joined_image(solution)
    print(part2(joined))

