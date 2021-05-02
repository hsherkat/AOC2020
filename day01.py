"""
Advent of Code 2020: Day 1
https://adventofcode.com/2020/day/1
"""

from typing import List, Tuple
from collections import Counter
from itertools import product


def find_pair_sums_to_N(nums: List[int], N: int) -> Tuple[int, int]:
    if (N % 2 == 0) and nums.count(N // 2) > 1:
        return (N // 2, N // 2)
    nums_set = set(nums)
    for n in nums_set:
        if N - n in nums_set and (n != N - n):
            return (n, N - n)
    raise ValueError("No pair found.")


def overcounted(arr: List, limits: Counter) -> bool:
    """Determines whether any item in arr appears more times than allowed by count_limits."""
    return any(arr.count(x) > limits[x] for x in set(arr))


def find_triplet_sums_to_N(nums: List[int], N: int) -> Tuple[int, int, int]:
    nums_counter = Counter(nums)
    if (N % 3 == 0) and not overcounted([N // 3] * 3, nums_counter):
        return (N // 3, N // 3, N // 3)
    nums_set = set(nums)
    for (m, n) in product(nums_set, nums_set):
        if N - m - n in nums_set and not overcounted([m, n, N - m - n], nums_counter):
            return (m, n, N - m - n)
    raise ValueError("No triplet found.")


#################

with open("input_1.txt") as f:
    x_input = [int(x) for x in f]


if __name__ == "__main__":
    x, y = find_pair_sums_to_N(x_input, 2020)
    print(f"Part 1: {x * y}")
    x, y, z = find_triplet_sums_to_N(x_input, 2020)
    print(f"Part 2: {x * y* z}")
