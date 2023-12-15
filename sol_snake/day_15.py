from collections import deque
from dataclasses import dataclass
from typing import TextIO


def hash_algo(s) -> int:
    hashed_val = 0
    for c in s:
        # Determine the ASCII code for the current character of the string.
        ascii = ord(c)

        # Increase the current value by the ASCII code you just determined.
        hashed_val += ascii
        # Set the current value to itself multiplied by 17.
        hashed_val *= 17
        # Set the current value to the remainder of dividing itself by 256.
        hashed_val = hashed_val % 256
    return hashed_val

@dataclass
class Lense:
    label : str
    focal_length : int
    def __repr__(self) -> str:
        return f"[{self.label} {self.focal_length}]"

def day_15(content: TextIO, is_example: bool = False) -> tuple[int, int]:

    steps = []
    with content as f:
        steps = [line for line in f.readline().strip().split(",")]

    # part 1
    hashes_only = [hash_algo(i) for i in steps]

    # part 2
    type Box = deque[Lense]
    storage : dict[int, Box] = {}
    # pre parsing isn't necessary, just makes the actual steps logic cleaner
    parsed_steps = []
    for step in steps:
        new_step = None
        if "=" in step:
            label, focal_length = step.split("=")
            new_step = (label,"=", int(focal_length))
        elif "-" in step:
            label, _ = step.split("-")
            new_step = (label, "-")
        else:
            continue
        parsed_steps.append(new_step)

    for step in parsed_steps:
        label = step[0]
        operation = step[1]
        relevant_box = hash_algo(label)
        # edge case, initializing the deque
        if relevant_box not in storage:
            storage[relevant_box] = deque()

        curr_box = storage[relevant_box]

        try:
            labeled_lense = [i for i in curr_box if i.label == label][0]
        except IndexError:
            labeled_lense = None

        if operation == "-":
            if labeled_lense is not None:
                curr_box.remove(labeled_lense)
        elif operation == "=":
            focal_length = step[2]
            if labeled_lense is not None:
                labeled_lense.focal_length = focal_length
            else:
                labeled_lense = Lense(label, focal_length)
                curr_box.append(labeled_lense)
        # very small memory footprint optimization just so we're not keeping the empty decks
        # even if it might make it slower due to access
        if not curr_box:
            del storage[relevant_box]

    focusing_power = []
    for box, lenses in storage.items():
        box_power = box+1
        for slot in range(len(lenses)):
            slot_power = slot + 1
            lense = lenses[slot]
            focus_power = box_power * slot_power * lense.focal_length
            focusing_power.append(focus_power)

    return sum(hashes_only), sum(focusing_power)
