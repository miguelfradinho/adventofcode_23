import math
from typing import TextIO


def solve(instructions, nodes_map, begin, finish) -> int:
    curr_node = begin
    steps_taken = 0
    n_instructions = len(instructions)
    while curr_node != finish:
        left, right = nodes_map[curr_node]
        next_instruction = instructions[steps_taken % n_instructions]
        if next_instruction == "R":
            curr_node = right
        elif next_instruction == "L":
            curr_node = left
        steps_taken += 1
    return steps_taken

## A  bit of slow search slow but at least it's usable
def solve_part_2(instructions, nodes_map, begin_nodes) -> int:
    curr_nodes = [i for i in begin_nodes]
    steps_taken = 0
    n_instructions = len(instructions)

    while any([True for i in curr_nodes if i[-1] != "Z"]):
        new_positions = []
        next_instruction = instructions[steps_taken % n_instructions]
        while curr_nodes != []:
            curr = curr_nodes.pop()
            left, right = nodes_map[curr]
            if next_instruction == "R":
                new_positions.append(right)
            elif next_instruction == "L":
                new_positions.append(left)
        curr_nodes = list(set(new_positions))
        steps_taken += 1
    return steps_taken

def day_8(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    instructions = []
    nodes_map : dict[str, tuple[str,str]] = {}

    with content as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            line = line.strip()
            # AAA = (BBB, CCC)
            pos, moves = line.strip().split("=")
            pos = pos.strip()
            l, r = moves.strip("() ").split(", ")
            moves = (l,r)
            nodes_map[pos] = moves

    # Part 1 with example_1
    #steps_taken = solve(instructions, nodes_map, "AAA", "ZZZ")

    # part 2
    start_nodes = [i for i in nodes_map.keys() if i[-1] == "A"]
    all_steps = []
    for i in start_nodes:
        steps = solve_part_2(instructions, nodes_map, [i])
        print(i, steps)
        all_steps.append(steps)


    return 0, math.lcm(*all_steps)