from typing import TextIO


def day_8(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    instructions = []
    nodes_map : dict[str, tuple[str,str]] = {}

    with content as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            line = line.strip()
            print(line)
            # AAA = (BBB, CCC)
            pos, moves = line.strip().split("=")
            # TNX
            pos = pos.strip()
            l, r = moves.strip("() ").split(", ")
            moves = (l,r)
            nodes_map[pos] = moves

    steps_taken = 0
    n_instructions = len(instructions)

    start_node = "AAA"
    end_node = "ZZZ"
    curr_node = start_node
    while curr_node != end_node:
        left, right = nodes_map[curr_node]
        next_instruction = instructions[steps_taken % n_instructions]
        if next_instruction == "R":
            curr_node = right
        elif next_instruction == "L":
            curr_node = left

        steps_taken += 1
    return steps_taken, 0
