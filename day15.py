"""
Advent of Code 2020: Day 15
https://adventofcode.com/2020/day/15
"""

from itertools import count, islice
from collections import defaultdict
import time


def take(n, it):
    return list(islice(it, None, n))


def nth(n, it):
    """Note: 0-indexed.
    """
    for _ in range(n):
        next(it)
    return next(it)


class ElfGame:
    def __init__(self, starting_nums):
        self.starting_nums = starting_nums[::-1]
        self.turn = 1
        self.last_times = defaultdict(int)
        self.last_spoken = None

    def update(self, speak):
        """Update with info from turn.
        Note we have a lag in updating last_times, since we want to know 
        back two times when it was spoken last turn.
        """
        self.last_times[self.last_spoken] = self.turn - 1
        self.last_spoken = speak
        self.turn += 1

    def get_word(self):
        if self.starting_nums:
            return self.starting_nums.pop()
        else:
            last_time = self.last_times[self.last_spoken]
            return self.turn - 1 - last_time if last_time else 0

    def play_turn(self):
        speak = self.get_word()
        out = (self.turn, speak)
        self.update(speak)
        return out

    def __iter__(self):
        return self

    def __next__(self):
        return self.play_turn()


#########################

x_input = [8, 0, 17, 4, 1, 12]

if __name__ == "__main__":
    g = ElfGame(x_input)
    part1 = nth(2020 - 1, g)
    print(part1)

    g = ElfGame(x_input)
    part2 = nth(30_000_000 - 1, g)
    print(part2)
