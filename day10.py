"""
Advent of Code 2020: Day 10
https://adventofcode.com/2020/day/10
"""

from collections import Counter, defaultdict
from typing import List


def sorted_differences(nums: List[int]) -> List[int]:
    nums_sorted = sorted(nums)
    pairs = zip(nums_sorted, nums_sorted[1:])
    return [x1 - x0 for (x0, x1) in pairs]


def adapter_diff_counts(adapters: List[int], last_diff: int) -> Counter:
    diffs = sorted_differences(adapters + [0])
    counts = Counter(diffs)
    counts[last_diff] += 1
    return counts


def dp_path_counts(nums: List[int]) -> int:
    nums_sorted = sorted(nums)
    dp = defaultdict(int)
    dp[0] = 1
    for n in nums_sorted:
        dp[n] = dp[n - 1] + dp[n - 2] + dp[n - 3]
    return dp[nums_sorted[-1]]


###############


with open("input_10.txt") as f:
    raw_input = list(f)
    x_input = [int(row) for row in raw_input]


if __name__ == "__main__":
    counts = adapter_diff_counts(x_input, 3)
    print(counts[1] * counts[3])
    path_counts = dp_path_counts(x_input)
    print(path_counts)
