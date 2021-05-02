"""
Advent of Code 2020: Day 5
https://adventofcode.com/2020/day/5
"""


from typing import Tuple


def parse_as_binary(s: str) -> Tuple[int, int]:
    d = str.maketrans({"F": "0", "B": "1", "L": "0", "R": "1"})
    s = s.translate(d)
    row_b = s[:-3]
    column_b = s[-3:]
    return int(row_b, 2), int(column_b, 2)


def seat_id(row: int, column: int) -> int:
    return 8 * row + column


def my_seat_cond(sid: int, id_set: set) -> bool:
    id_missing = sid not in id_set
    neighbors_present = (sid + 1) in id_set and (sid - 1) in id_set
    return id_missing and neighbors_present


##############

with open("input_5.txt") as f:
    x_input = [row.strip() for row in f]


if __name__ == "__main__":
    seats = (parse_as_binary(boarding_pass) for boarding_pass in x_input)
    max_id = max(seat_id(*seat) for seat in seats)
    print(max_id)

    seats = (parse_as_binary(boarding_pass) for boarding_pass in x_input)
    id_set = set(seat_id(*seat) for seat in seats)
    my_id = [sid for sid in range(max_id) if my_seat_cond(sid, id_set)]
    print(my_id)
