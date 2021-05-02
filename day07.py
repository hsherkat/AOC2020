"""
Advent of Code 2020: Day 7
https://adventofcode.com/2020/day/7
"""

import re
from collections import defaultdict
from typing import List, Tuple, Set


def parse_input(x: List[str]) -> Tuple[dict, dict]:
    d_contains = dict()
    d_contained_in = defaultdict(list)
    pattern = r"(\d) (\w+ \w+) bags?"

    for row in x:
        L, R = row.split(" bags contain ")
        bag = L
        contained_bags = re.findall(pattern, R)
        d_contains[bag] = contained_bags
        for (num, contained) in contained_bags:
            d_contained_in[contained].append(bag)
    return d_contains, d_contained_in


def generate_containers(bag: str, d: dict) -> Set[str]:
    """Use with d_contained_in."""
    out = set()
    for contained in d[bag]:
        out.add(contained)
        out |= generate_containers(contained, d)
    return out


def count_contained_bags(bag: str, d: dict) -> int:
    """Includes self, so subtract 1 for strictly contained bags. Use with d_contains."""
    out = 1
    for (num, contained) in d[bag]:
        out += int(num) * count_contained_bags(contained, d)
    return out


####################

with open("input_7.txt") as f:
    raw_input = list(f)
    x_input = [row.strip() for row in raw_input]


if __name__ == "__main__":
    d_contains, d_contained_in = parse_input(x_input)
    shiny_gold_containers = generate_containers("shiny gold", d_contained_in)
    print(len(shiny_gold_containers))
    print(count_contained_bags("shiny gold", d_contains) - 1)
