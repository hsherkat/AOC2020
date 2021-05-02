"""
Advent of Code 2020: Day 12
https://adventofcode.com/2020/day/12
"""


class Ferry:
    def __init__(self, x: int = 0, y: int = 0, facing: str = "E"):
        self.x = x
        self.y = y
        self.facing = facing

    @staticmethod
    def parse_move(s: str):
        direction = s[0]
        dist = int(s[1:])
        return direction, dist

    def move(self, direction: str, dist: int):
        if direction == "N":
            self.y += dist
        elif direction == "E":
            self.x += dist
        elif direction == "S":
            self.move("N", -dist)
        elif direction == "W":
            self.move("E", -dist)
        elif direction == "F":
            self.move(self.facing, dist)
        elif direction == "R":
            directions = "NESW"
            change = dist // 90
            curr_idx = directions.index(self.facing)
            self.facing = directions[(curr_idx + change) % 4]
        elif direction == "L":
            self.move("R", 360 - dist)
        return

    def manhatten_norm(self):
        return abs(self.x) + abs(self.y)


class Ferry2(Ferry):
    def __init__(self, x: int = 0, y: int = 0, wx: int = 10, wy: int = 1):
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy

    def move(self, direction: str, dist: int):
        if direction == "N":
            self.wy += dist
        elif direction == "E":
            self.wx += dist
        elif direction == "S":
            self.move("N", -dist)
        elif direction == "W":
            self.move("E", -dist)
        elif direction == "F":
            self.x += dist * self.wx
            self.y += dist * self.wy
        elif direction == "R":
            change = dist // 90
            for _ in range(change):
                self.wx, self.wy = self.wy, -self.wx
        elif direction == "L":
            self.move("R", 360 - dist)
        return


############


with open("input_12.txt") as f:
    raw_input = list(f)
    x_input = [Ferry.parse_move(row.strip()) for row in raw_input]

if __name__ == "__main__":
    ferry = Ferry()
    for move in x_input:
        ferry.move(*move)
    print(ferry.manhatten_norm())

    ferry2 = Ferry2()
    for move in x_input:
        ferry2.move(*move)
    print(ferry2.manhatten_norm())
