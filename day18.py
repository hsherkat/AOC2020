"""
Advent of Code 2020: Day 18
https://adventofcode.com/2020/day/18
"""


from typing import Callable, Optional, Tuple
import re
from math import prod


def apply(op: str, x: int, y: int) -> int:
    if op == "+":
        return x + y
    elif op == "*":
        return x * y
    else:
        raise ValueError(f"Unknown operator {op}")


def find_parenthetical(s: str) -> Optional[Tuple[int, int]]:
    """Finds the start and end of the first parenthetical subexpression.
    Returns None if there isn't any.
    """
    if (start := s.find("(")) != -1:
        height = 1
        for i, c in enumerate(s[start + 1 :]):
            if c == "(":
                height += 1
            elif c == ")":
                height -= 1
            else:
                continue
            if height == 0:
                end = i + start + 1
                return start, end
        else:
            raise ValueError("Invalid expression, no ending paren.")
    else:
        return None


def compute_no_parens_left_to_right(formula: str) -> int:
    """Recursively compute by evaluating first operation and substituting the result in its place.
    Priority of + and * is just left to right.
    """
    if formula.isnumeric():
        return int(formula)

    pattern = r"(\d+)\s*([\+\*])\s*(\d+)"  # x + y, x * y
    if not (match := re.search(pattern, formula)):
        raise ValueError("Bad formula: not a single number, but can't find a+b or a*b ")
    x, op, y = match.groups()

    ans = apply(op, int(x), int(y))

    if formula.count("+") + formula.count("*") == 1:
        return ans
    else:
        reduced = str(ans) + formula[match.end() :]
        return compute_no_parens_left_to_right(reduced)


def compute_no_parens_add_first(formula: str) -> int:
    """Recursively compute by evaluating first sum and substituting the result in its place.
    If there are no sums, just compute the product.
    + has priority over *.
    """
    pattern = r"(\d+)\s*\+\s*(\d+)"  # x + y

    if not (match := re.search(pattern, formula)):
        return prod(int(n.strip()) for n in formula.split("*"))
    else:
        x, y = match.groups()
        ans = int(x) + int(y)
        reduced = formula[: match.start()] + str(ans) + formula[match.end() :]
        return compute_no_parens_add_first(reduced)


def compute(formula: str, compute_no_parens: Callable[[str], int]) -> int:
    """Recursively compute by evaluating first parenthetical subexpression and substituting the result in its place.
    If there aren't any, pass to helper function.
    """
    if paren_indices := find_parenthetical(formula):
        start, end = paren_indices
        inner = formula[start + 1 : end]
        reduced = (
            formula[:start]
            + str(compute(inner, compute_no_parens))
            + formula[end + 1 :]
        )
        return compute(reduced, compute_no_parens)
    else:
        return compute_no_parens(formula)


#############


with open("input_18.txt") as f:
    x_input = [line for line in f]

left_to_right = compute_no_parens_left_to_right
add_first = compute_no_parens_add_first

if __name__ == "__main__":
    out = sum(compute(formula, left_to_right) for formula in x_input)
    print(out)
    out2 = sum(compute(formula, add_first) for formula in x_input)
    print(out2)