"""
Advent of Code 2020: Day 19
https://adventofcode.com/2020/day/19
"""

import re
from itertools import product
from typing import Dict


def get_matches(rule: str, rules_dict: Dict[str, str]):
    pattern = r'"([a-z]+)"'
    if (match := re.search(pattern, rule)) :  # base case, single letter
        c = match.group(1)
        return [c]
    elif "|" in rule:  # two possibilities
        rule1, rule2 = [r.strip() for r in rule.split("|")]
        return get_matches(rule1, rules_dict) + (get_matches(rule2, rules_dict))
    else:  # join them together
        return [
            "".join(x)
            for x in product(
                *[get_matches(rules_dict[i], rules_dict) for i in rule.split()]
            )
        ]


def parse_input(raw_input):
    d = dict(line.split(":") for line in raw_input.split("\n"))
    return {k.strip(): v.strip() for k, v in d.items()}


def hacky(s):
    N = len(s)
    if N % 8 != 0:
        return False
    ss = "".join(
        [
            str(
                "a" * ((chunk := s[8 * i : 8 * i + 8]) in matches42)
                + "b" * (chunk in matches31)
                + "c" * (chunk not in matches42 and chunk not in matches31)
            )
            for i in range(N // 8)
        ]
    )
    c42, c31, ccs = ss.count("a"), ss.count("b"), ss.count("c")
    return (c42 > c31) and (c31 > 0) and ccs == 0 and ss.endswith("b" * c31)


###############

with open("input_19.txt") as f:
    raw_input = f.read()  # "".join([line for line in f])
    rules = parse_input(raw_input.split("\n\n")[0])


if __name__ == "__main__":
    msgs = set(line.strip() for line in raw_input.strip().split("\n\n")[1].split("\n"))
    matches42 = get_matches(rules["42"], rules)
    matches31 = get_matches(rules["31"], rules)
    out = sum(hacky(msg) for msg in msgs)
    print(out)
