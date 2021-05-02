"""
Advent of Code 2020: Day 6
https://adventofcode.com/2020/day/6
"""


with open("input_6.txt") as f:
    raw_input = "".join(list(f))
    x_input = [group.strip().split("\n") for group in raw_input.split("\n\n")]


group_unions = [set("".join(group)) for group in x_input]
union_sizes = [len(s) for s in group_unions]

group_intersections = [
    set.intersection(*(set(person) for person in group)) for group in x_input
]
intersection_sizes = [len(s) for s in group_intersections]


if __name__ == "__main__":
    print(sum(union_sizes))
    print(sum(intersection_sizes))