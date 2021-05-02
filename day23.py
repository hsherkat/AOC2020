"""
Advent of Code 2020: Day 23
https://adventofcode.com/2020/day/23
"""

from collections import deque
from typing import Iterable
from math import prod


def shift_left(q: deque, dest=None):
    if dest is None:
        q.append(q.popleft())
        return
    if q[0] == dest:
        return
    for _ in range(len(q)):
        q.append(q.popleft())
        if q[0] == dest:
            return


def move(qq: Iterable, lo, hi):
    q = deque(qq)
    current = q[0]
    shift_left(q)
    a, b, c = q.popleft(), q.popleft(), q.popleft()
    destination = current - 1 if (current > lo) else hi
    while destination in (a, b, c):
        destination -= 1
        if destination < lo:
            destination = hi
    shift_left(q, destination)
    shift_left(q)
    # q = deque([a, b, c]) + q
    q.extendleft([c, b, a])
    shift_left(q, current)
    shift_left(q)
    return q


def part_1(qq):
    q = deque(qq)
    shift_left(q, dest=1)
    q.popleft()
    out = "".join(str(n) for n in q)
    return int(out)


def get_d_next(cups):
    nums = [int(n) for n in cups]
    initial, final = nums[0], nums[-1]
    d_next = {m: n for (m, n) in zip(range(10, 1_000_001), range(11, 1_000_001))}
    for (m, n) in zip(nums, nums[1:]):
        d_next[m] = n
    d_next[final] = 10
    d_next[1_000_000] = initial
    return d_next, initial


def get_dest(a, b, c, curr):
    dest = curr - 1
    if dest == 0:
        dest = 1_000_000
    while dest in (a, b, c):
        dest -= 1
        if dest == 0:
            dest = 1_000_000
    return dest


def update(d_next, initial, repetitions):
    d = d_next
    curr = initial
    for _ in range(repetitions):
        a, b, c = d[curr], d[d[curr]], d[d[d[curr]]]
        d[curr] = d[c]
        dest = get_dest(a, b, c, curr)
        d[c] = d[dest]
        d[dest] = a
        curr = d[curr]


def part2(cups):
    d_next, initial = get_d_next(cups)
    update(d_next, initial, 10_000_000)
    return d_next[1], d_next[d_next[1]]


###############

if __name__ == "__main__":
    cups = "318946572"

    q_input = deque((int(n) for n in cups))
    for _ in range(100):
        q_input = move(q_input, 1, 9)
    out = part_1(q_input)
    print(out)

    out = part2(cups)
    print(prod(out))
