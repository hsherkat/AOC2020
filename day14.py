"""
Advent of Code 2020: Day 14
https://adventofcode.com/2020/day/14
"""

import re
from typing import Tuple, Union, List
from collections import deque


def parse_row(row: str):
    """Row either contains a mask or address and value."""
    if row.startswith("mask"):
        mask = row[7:]
        return mask
    elif row.startswith("mem"):
        pattern = r"mem\[(\d+)\] = (\d+)"
        addr, val = re.fullmatch(pattern, row).groups(1)
        return addr, int(val)
    else:
        raise ValueError("Bad input.")


def parse_mask(mask: str) -> Tuple[int, int]:
    """or_mask for setting bits, and_mask for clearing bits."""
    or_mask = mask.replace("X", "0")
    and_mask = mask.replace("X", "1")
    return int(or_mask, 2), int(and_mask, 2)


def write_to_memory(parsed_input) -> dict:
    memory = dict()
    or_mask, and_mask = 0, 0
    for parsed in parsed_input:
        if len(parsed) > 2:
            or_mask, and_mask = parse_mask(parsed)
        else:
            addr, val = parsed
            val |= or_mask
            val &= and_mask
            memory[addr] = val
    return memory


####


def apply_mask_to_address(mask: str, address: str) -> str:
    """Copy 1s and Xs from mask to address.
    address is a decimal string, needs to be converted to binary and padded.
    """
    N = len(mask)
    addr = int(address)
    addr_str = f"{addr:0{N}b}"
    new_str = [a if m == "0" else m for (m, a) in zip(list(mask), list(addr_str))]
    return "".join(new_str)


def get_addresses(addr_Xs: str) -> List[str]:
    """Return all possible replacements of Xs with 0 or 1.
    """
    q = deque([addr_Xs])
    addresses = []
    while q:
        addr = q.popleft()
        idx = addr.find("X")
        if idx == -1:
            addresses.append(addr)
        else:
            q.append(addr[:idx] + "0" + addr[idx + 1 :])
            q.append(addr[:idx] + "1" + addr[idx + 1 :])
    return [str(int(addr, 2)) for addr in addresses]


def get_addresses_recursive(addr_Xs: List[str]) -> List[str]:
    out = []
    for addr in addr_Xs:
        idx = addr.find("X")
        if idx == -1:
            out.append(addr)
        else:
            out.extend(get_addresses_recursive([addr[:idx] + "0" + addr[idx + 1 :]]))
            out.extend(get_addresses_recursive([addr[:idx] + "1" + addr[idx + 1 :]]))
    return out


def write_to_memory_2(parsed_input) -> dict:
    memory = dict()
    mask = ""
    for parsed in parsed_input:
        if isinstance(parsed, str):
            mask = parsed
        else:
            addr, val = parsed
            addr_Xs = apply_mask_to_address(mask, addr)
            for addr in get_addresses(addr_Xs):
                memory[addr] = val
    return memory


####################


with open("input_14.txt") as f:
    raw_input = list(f)
    x_input = [row.strip() for row in raw_input]


if __name__ == "__main__":
    parsed_input = [parse_row(row) for row in x_input]
    memory = write_to_memory(parsed_input)
    part1 = sum(val for addr, val in memory.items())
    print(part1)
    memory_2 = write_to_memory_2(parsed_input)
    part2 = sum(val for addr, val in memory_2.items())
    print(part2)
