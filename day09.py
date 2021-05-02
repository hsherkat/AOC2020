"""
Advent of Code 2020: Day 9
https://adventofcode.com/2020/day/9
"""

from collections import deque
from typing import List
from day01 import find_pair_sums_to_N
from itertools import islice


with open("input_9.txt") as f:
    raw_input = list(f)
    x_input = [int(row) for row in raw_input]


def find_invalid_entry(nums: List[int], preamble_size: int) -> int:
    """Have a moving window of size = preamble_size;
    find first number that isn't a sum of two from the window.
    """
    nums_iter = iter(nums)
    q = deque(islice(nums_iter, None, preamble_size), maxlen=preamble_size)
    for n in nums_iter:
        try:
            find_pair_sums_to_N(list(q), n)
        except ValueError:
            return n
        else:
            q.append(n)
    raise ValueError("No invalid number in data.")


def find_continguous_sums_to_N(nums: List[int], N: int) -> List[int]:
    q: deque = deque([])
    nums_q = deque(nums)
    while nums_q:
        if sum(q) == N:
            return list(q)
        elif sum(q) < N:
            q.append(nums_q.popleft())
        elif sum(q) > N:
            q.popleft()
    raise ValueError(f"No continguous subarray sums to {N}.")


if __name__ == "__main__":
    invalid_entry = find_invalid_entry(x_input, 25)
    print(invalid_entry)
    cntg = find_continguous_sums_to_N(x_input, invalid_entry)
    print(min(cntg) + max(cntg))
