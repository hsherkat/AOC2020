"""
Advent of Code 2020: Day 4
https://adventofcode.com/2020/day/4
"""

import re


def parse_input_to_str_gen(g):
    passport = []
    for item in g:
        if not item:
            yield " ".join(passport)
            passport = []
        else:
            passport.append(item)


def passport_dict(s: str) -> dict:
    return dict([item.split(":") for item in s.split()])


CONDITIONS = []


def register_condition(condition):
    CONDITIONS.append(condition)
    return condition


@register_condition
def condition_nec_fields(passport: dict) -> bool:
    passport_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    optional_fields = ["cid"]
    necessary_fields = [
        field for field in passport_fields if field not in optional_fields
    ]
    return all(field in passport.keys() for field in necessary_fields)


@register_condition
def condition_byr(passport: dict) -> bool:
    return "1920" <= passport["byr"] <= "2002"


@register_condition
def condition_iyr(passport: dict) -> bool:
    return "2010" <= passport["iyr"] <= "2020"


@register_condition
def condition_eyr(passport: dict) -> bool:
    return "2020" <= passport["eyr"] <= "2030"


@register_condition
def condition_hgt(passport: dict) -> bool:
    pattern = r"([\d]+)(in|cm)"
    match = re.fullmatch(pattern, passport["hgt"])
    if match is None:
        return False
    hgt, units = match.groups()
    return "150" <= hgt <= "193" if units == "cm" else "59" <= hgt <= "76"


@register_condition
def condition_hcl(passport: dict) -> bool:
    pattern = r"#[0-9a-f]{6}"
    hcl = passport["hcl"]
    return re.fullmatch(pattern, hcl) is not None


@register_condition
def condition_ecl(passport: dict) -> bool:
    EYE_COLORS = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    return passport["ecl"] in EYE_COLORS


@register_condition
def condition_pid(passport: dict) -> bool:
    pattern = r"[\d]{9}"
    pid = passport["pid"]
    return re.fullmatch(pattern, pid) is not None


def is_valid(passport: dict) -> bool:
    return condition_nec_fields(passport)


def is_valid_2(passport: dict) -> bool:
    return all(cond(passport) for cond in CONDITIONS)


def count_valid_passports(passports) -> int:
    return sum(is_valid(passport) for passport in passports)


def count_valid_passports_2(passports) -> int:
    return sum(is_valid_2(passport) for passport in passports)


##############

with open("input_4.txt") as f:
    x_input = [row.strip() for row in f]


if __name__ == "__main__":
    passports_str = parse_input_to_str_gen(x_input)
    passports = (passport_dict(p) for p in passports_str)
    print(count_valid_passports(passports))
    passports_str = parse_input_to_str_gen(x_input)
    passports = (passport_dict(p) for p in passports_str)
    print(count_valid_passports_2(passports))
