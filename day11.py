"""
Advent of Code 2020: Day 11
https://adventofcode.com/2020/day/11
"""

from typing import List, Tuple


class FerrySeats:
    def __init__(self, seats: List[str]) -> None:
        self.seats = seats
        self.rows = len(seats)
        self.cols = len(seats[0])

    def in_bounds(self, i: int, j: int) -> bool:
        return (0 <= i < self.rows) and (0 <= j < self.cols)

    def neighbors(self, i: int, j: int) -> List[str]:
        return [
            self.seats[m][n]
            for m in (i - 1, i, i + 1)
            for n in (j - 1, j, j + 1)
            if self.in_bounds(m, n) and (m, n) != (i, j)
        ]

    def seat_update(self, i: int, j: int) -> str:
        if self.seats[i][j] == "L" and not any(
            nbr == "#" for nbr in self.neighbors(i, j)
        ):
            return "#"
        if self.seats[i][j] == "#" and self.neighbors(i, j).count("#") > 3:
            return "L"
        return self.seats[i][j]

    def update_seats(self):
        new_seats = [
            [self.seat_update(i, j) for j in range(self.cols)] for i in range(self.rows)
        ]
        self.seats = new_seats
        return self

    def final_occupied_seat_count(self) -> int:
        """Update until no change, then count."""
        prev = self.seats
        curr = self.update_seats().seats
        while prev != curr:
            prev = curr
            curr = self.update_seats().seats
        return sum(row.count("#") for row in curr)


class FerrySeatsModified(FerrySeats):
    def occupied_seat_visible(self, i: int, j: int, direction: Tuple[int, int]) -> int:
        x, y = direction
        while True:
            i, j = i + x, j + y
            if self.in_bounds(i, j):
                if self.seats[i][j] == "#":
                    return True
                if self.seats[i][j] == "L":
                    return False
            else:
                return False
        return False

    def visible_occupied_seats_count(self, i: int, j: int) -> int:
        directions = [
            (x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)
        ]
        return sum(
            self.occupied_seat_visible(i, j, direction) for direction in directions
        )

    def seat_update(self, i: int, j: int) -> str:
        if self.seats[i][j] == "L" and self.visible_occupied_seats_count(i, j) == 0:
            return "#"
        if self.seats[i][j] == "#" and self.visible_occupied_seats_count(i, j) > 4:
            return "L"
        return self.seats[i][j]


############

with open("input_11.txt") as f:
    raw_input = list(f)
    x_input = [row.strip() for row in raw_input]


if __name__ == "__main__":
    ferry = FerrySeats(x_input)
    print(ferry.final_occupied_seat_count())
    ferry2 = FerrySeatsModified(x_input)
    print(ferry2.final_occupied_seat_count())
