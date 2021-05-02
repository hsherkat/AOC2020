"""
Advent of Code 2020: Day 21
https://adventofcode.com/2020/day/21
"""

from typing import Tuple, List, Dict, Union, Set


def parse(raw_input: str) -> Tuple[Dict[str, Set[str]], Set[str]]:
    potential_source: Dict[str, Set[str]] = dict()
    all_ingredients: Set[str] = set()
    for line in raw_input.strip().split("\n"):
        s1, s2 = line.strip().split(" (contains ")
        ingredients = s1.split()
        allergens = s2[:-1].split(", ")
        all_ingredients.update(ingredients)
        for a in allergens:
            if a in potential_source:
                potential_source[a].intersection_update(ingredients)
            else:
                potential_source[a] = set(ingredients)
    return potential_source, all_ingredients


def part_1(
    potential_sources: Dict[str, Set[str]], all_ingredients: Set[str], raw_input: str
) -> int:
    possible_bad_ingredients = set.union(*potential_sources.values())
    good_ingredients = set(
        [food for food in all_ingredients if food not in possible_bad_ingredients]
    )
    good_count = sum(
        line.split().count(good)
        for line in raw_input.split("\n")
        for good in good_ingredients
    )
    return good_count


def part_2(potential_sources: Dict[str, Set[str]]):
    N = len(potential_sources)
    for _ in range(N):
        nailed_down = [
            (allergen, source)
            for (allergen, source) in potential_sources.items()
            if len(source) == 1
        ]
        for allergen, source in nailed_down:
            ing = list(source).pop()
            for other_sources in potential_sources.values():
                if len(other_sources) > 1:
                    other_sources.discard(ing)
    return sorted(potential_sources.items(), key=lambda x: x[0])


################


with open("input_21.txt") as f:
    raw_input = f.read()  # "".join([line for line in f])
    potential_sources, all_ingredients = parse(raw_input)


if __name__ == "__main__":
    out = part_1(potential_sources, all_ingredients, raw_input)
    print(out)
    ings = [list(x[1]).pop() for x in part_2(potential_sources)]
    print(",".join(ings))
