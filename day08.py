"""
Advent of Code 2020: Day 8
https://adventofcode.com/2020/day/8
"""


with open("input_8.txt") as f:
    x_input = [row.strip() for row in f]


def parse_instruction(instr):
    op, num = instr.split(" ")
    val = int(num)
    return op, val


def execute_instruction(instructions, row_num):
    op, val = parse_instruction(instructions[row_num])
    next_row = row_num + 1
    incr = 0
    if op == "jmp":
        next_row = row_num + val
    if op == "acc":
        incr = val
    return next_row, incr


def execute_all(instructions):
    seen_rows = set()
    row_num, increment = (0, 0)
    acc_total = 0
    while True:
        seen_rows.add(row_num)
        row_num, increment = execute_instruction(instructions, row_num)
        acc_total += increment
        if row_num in seen_rows:
            break_cond = f"Repeat: {row_num}"
            break
        if row_num >= len(instructions):
            break_cond = f"Passed the end: {row_num}"
            break
    return acc_total, break_cond


def modify_instructions(instructions, idx):
    new_instructions = instructions[:]
    if "nop" in instructions[idx]:
        new_instructions[idx] = instructions[idx].replace("nop", "jmp")
    elif "jmp" in instructions[idx]:
        new_instructions[idx] = instructions[idx].replace("jmp", "nop")
    return new_instructions


if __name__ == "__main__":
    print(execute_all(x_input))
    N = len(x_input)
    for i in range(N):
        out = execute_all(modify_instructions(x_input, i))
        if "Passed" in out[1] and str(N) in out[1]:
            print(out)
