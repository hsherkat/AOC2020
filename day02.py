"""
Advent of Code 2020: Day 2
https://adventofcode.com/2020/day/2
"""

import re
from typing import List, NamedTuple


class PasswordRow(NamedTuple):
    lo_bound: int
    hi_bound: int
    letter: str
    password: str


def parse_row(row: str) -> PasswordRow:
    """Parse row to make PasswordRow namedtuple."""
    nums, letter, password = row.split()
    lo, hi = nums.split("-")
    letter = letter[0]
    password = password.strip()
    return PasswordRow._make((int(lo), int(hi), letter, password))


def is_valid(row: PasswordRow) -> bool:
    return row.lo_bound <= row.password.count(row.letter) <= row.hi_bound


def is_valid_2(row: PasswordRow) -> bool:
    i, j = row.lo_bound - 1, row.hi_bound - 1
    c = row.letter
    return (row.password[i] == c) ^ (row.password[j] == c)


###############

with open("input_2.txt") as f:
    raw_input = list(f)
    x_input = (parse_row(x) for x in raw_input)


if __name__ == "__main__":
    password_rows = list(x_input)
    part1 = sum(is_valid(row) for row in password_rows)
    print(part1)
    part2 = sum(is_valid_2(row) for row in password_rows)
    print(part2)
