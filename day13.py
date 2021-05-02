"""
Advent of Code 2020: Day 13
https://adventofcode.com/2020/day/13
"""

from typing import List, Tuple
from functools import reduce


def parse_input(data: List[str]) -> Tuple[int, List[int], list]:
    """First two return values are used for part1; third used for part2.
    """
    earliest_time = int(data[0])
    bus_ids = [int(s) for s in data[1].split(",") if s.isnumeric()]
    enumerated_bus_ids = [
        (-i, int(s)) for (i, s) in enumerate(data[1].split(",")) if s.isnumeric()
    ]
    return earliest_time, bus_ids, enumerated_bus_ids


def wait_time(earliest_time: int, bus: int) -> int:
    """Returns how long you wait until the bus comes along.
    """
    return bus - (earliest_time % bus)


def earliest_bus(earliest_time: int, bus_ids: List[int]) -> int:
    """Returns which bus comes first.
    """
    return min(bus_ids, key=lambda bus: wait_time(earliest_time, bus))


def xgcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean algorithm, also solves Bezout.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)
    Found online somewhere.
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def _solve_system_modular_equations(pair_0, pair_1) -> Tuple[int, int]:
    """Solves a system of 2 equations:
    x = ai mod ni. Pairs are given as (ai, ni)
    """
    a0, n0 = pair_0
    a1, n1 = pair_1
    _, m0, m1 = xgcd(n0, n1)
    out = (a0 * m1 * n1) + (a1 * m0 * n0)
    mod = n0 * n1
    return out % mod, mod


def solve_system_modular_equations(pairs) -> int:
    """Solves a system of 3+ equations, applies previous fn multiple times.
    x = ai mod ni. Pairs are given as (ai, ni)
    """
    return reduce(_solve_system_modular_equations, pairs)[0]


def part_2(x) -> int:
    _, _, pairs = parse_input(x)
    return solve_system_modular_equations(pairs)


####################

with open("input_13.txt") as f:
    raw_input = list(f)
    x_input = [row.strip() for row in raw_input]

if __name__ == "__main__":
    t, ids, enum_ids = parse_input(x_input)
    bus = earliest_bus(t, ids)
    wait = wait_time(t, bus)
    print(wait * bus)
    print(solve_system_modular_equations(enum_ids))
