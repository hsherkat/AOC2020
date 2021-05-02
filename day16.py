"""
Advent of Code 2020: Day 16
https://adventofcode.com/2020/day/16
"""

import re
from typing import List, Tuple, Set, Dict
from math import prod

Interval = Tuple[int, int]


def process_raw_input(raw_input: str) -> List[List[str]]:
    return [section.strip().split("\n") for section in raw_input.split("\n\n")]


def parse_rules(rule_str: List[str]) -> Dict[str, Tuple[Interval, Interval]]:
    rules_pattern = r"([\s\w]+): (\d+)-(\d+) or (\d+)-(\d+)"
    rules = dict()
    for line in rule_str:
        m = re.search(rules_pattern, line)
        rule_class: str = m[1]
        rule1 = int(m[2]), int(m[3])
        rule2 = int(m[4]), int(m[5])
        rules[rule_class] = (rule1, rule2)
    return rules


def parse_input(x_input: List[List[str]]) -> Tuple:
    rules = parse_rules(x_input[0])
    my_ticket = tuple([int(x) for x in x_input[1][1].split(",")])
    nearby_tickets = [tuple([int(x) for x in y.split(",")]) for y in x_input[2][1:]]
    return rules, my_ticket, nearby_tickets


def valid_nums(rules) -> Set[int]:
    """Numbers not in here cannot be valid.
    """
    f = lambda a, b: range(a, b + 1)  # inclusive range
    valids: Set[int] = set()
    for (rule1, rule2) in rules.values():
        valids.update(f(*rule1))
        valids.update(f(*rule2))
    return valids


def valid_for_some(ticket, valid_set) -> bool:
    """Returns whether every number satisfies some rule.
    Does not determine if the ticket is actually valid, but we seem to be assuming that.
    """
    return all(num in valid_set for num in ticket)


def violates(num: int, rule: Tuple[Interval, Interval]) -> bool:
    """Is the number in neither of the two intervals?
    """
    f = lambda a, b: range(a, b + 1)  # inclusive range
    rule1, rule2 = rule
    return num not in f(*rule1) and num not in f(*rule2)


def process_ticket(ticket: List[int], possible_locations: Dict[str, Set[int]]):
    """Rule out where a rule can be located by looking at violations.
    """
    for idx, num in enumerate(ticket):
        for rule_name, rule in rules.items():
            if violates(num, rule):
                possible_locations[rule_name].discard(idx)


def reason(possible_locations, reps):
    """Reason logically:
    if a rule can be at only one location, once you know where it is, it can't be elsewhere.
    """
    for _ in range(reps):
        fixed_locs = [loc for loc in possible_locations.values() if len(loc) == 1]
        for loc in fixed_locs:
            loc = list(loc)[0]
            for other_locs in possible_locations.values():
                if len(other_locs) > 1:
                    other_locs.discard(loc)


################

with open("input_16.txt") as f:
    raw_input = "".join(list(f))
    x_input = process_raw_input(raw_input)


if __name__ == "__main__":

    rules, my_ticket, nearby_tickets = parse_input(x_input)
    valid_set = valid_nums(rules)
    out = sum(n for ticket in nearby_tickets for n in ticket if n not in valid_set)
    print(out)

    ####

    possible_locations = {
        rule_class: set(range(len(my_ticket))) for rule_class in rules
    }
    valid_tickets = [
        ticket for ticket in nearby_tickets if all(num in valid_set for num in ticket)
    ]
    for ticket in valid_tickets:
        process_ticket(ticket, possible_locations)
    reason(possible_locations, len(my_ticket))
    departure_fields = []
    for rule_name, loc_set in possible_locations.items():
        if rule_name.startswith("departure"):
            departure_fields.append(list(loc_set)[0])
    out = prod([my_ticket[i] for i in departure_fields])
    print(out)
