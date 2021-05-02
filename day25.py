"""
Advent of Code 2020: Day 25
https://adventofcode.com/2020/day/25
"""


def transform(subject, val=1):
    val *= subject
    val = val % 20201227
    return val


def transform_loop(subject, loop_size):
    val = 1
    for _ in range(loop_size):
        val = transform(subject, val)
    return val


def get_loop_size(public_key, subject):
    loop_size = 0
    val = 1
    while val != public_key:
        val = transform(subject, val)
        loop_size += 1
    return loop_size


###############

key1 = 14012298
key2 = 74241

if __name__ == "__main__":
    loop_size_1 = get_loop_size(key1, 7)
    loop_size_2 = get_loop_size(key2, 7)
    print(transform_loop(key1, loop_size_2))
    print(transform_loop(key2, loop_size_1))
