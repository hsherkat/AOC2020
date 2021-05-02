"""
Advent of Code 2020: Day 24
https://adventofcode.com/2020/day/24
"""

from collections import defaultdict


def count_directions(s: str):
    counts = dict()
    for direction in ["ne", "nw", "se", "sw"]:
        counts[direction] = s.count(direction)
        s = s.replace(direction, "")
    for direction in ["e", "w"]:
        counts[direction] = s.count(direction)
    return counts


def get_coords(counts):
    pairs = [("ne", "sw"), ("e", "w"), ("nw", "se")]
    for p, m in pairs:
        counts[p] -= counts[m]
        # del counts[m]
    counts["e"] -= counts["nw"]
    counts["ne"] += counts["nw"]
    # del counts['nw']
    return (counts["e"], counts["ne"])


def neighbors(tile):
    x, y = tile
    return [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
    ]


def stay_black(tile, black_tiles):
    return sum(nbr in black_tiles for nbr in neighbors(tile)) in (1, 2,)


def become_black(tile, black_tiles):
    return sum(nbr in black_tiles for nbr in neighbors(tile)) == 2


def update_tiles(black_tiles):
    new_blacks = set()
    white_tiles = (
        nbr for tile in black_tiles for nbr in neighbors(tile) if nbr not in black_tiles
    )
    for tile in black_tiles:
        if stay_black(tile, black_tiles):
            new_blacks.add(tile)
    for tile in white_tiles:
        if become_black(tile, black_tiles):
            new_blacks.add(tile)
    return new_blacks


def get_black_tiles(x_input):
    flips = defaultdict(int)
    for line in x_input:
        counts = count_directions(line)
        flips[get_coords(counts)] += 1
    black_tiles = set(tile for tile, flip_count in flips.items() if flip_count % 2)
    return black_tiles


def part1(x_input):
    black_tiles = get_black_tiles(x_input)
    return len(black_tiles)


def part2(x_input, days):
    black_tiles = get_black_tiles(x_input)
    for day in range(days):
        black_tiles = update_tiles(black_tiles)
    return len(black_tiles)


###############

with open("input_24.txt") as f:
    x_input = [line for line in f]

if __name__ == "__main__":
    print(part1(x_input))
    print(part2(x_input, 100))
