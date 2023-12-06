from typing import TextIO

import numpy as np

from utils import parse_ints


def calculates_distance(button_time: int, race_duration: int) -> int:
    # the more time we spend holding the button, the less we have
    remaining_duration = race_duration - button_time
    # we get 1 speed per 1 unit of holding down the button
    speed = button_time * 1
    # distance travelled
    return speed * remaining_duration


def solve(race_duration: int, record_distance: int) -> int:
    return sum([
        1 if calculates_distance(i, race_duration) > record_distance
        else 0
        for i in range(1, race_duration)
    ])


def day_6(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    time_line: list[str]
    distance_line: list[str]
    with content as f:
        # For part 1, input is
        # Time : Number Number
        # Distance : Number Number
        time_line = f.readline().split(":")[1].strip().split(" ")
        distance_line = f.readline().split(":")[1].strip().split(" ")

    # part 1, races are separated by spaces
    races_info_part1 = list(zip(parse_ints(time_line), parse_ints(distance_line)))

    solutions_part1 = [solve(d, r) for (d, r) in races_info_part1]
    # part 2, we need to assume it's all the same number, so
    races_info_part2 = [(int("".join(time_line)), int("".join(distance_line)))]
    solutions_part2 = [solve(d, r) for d, r in races_info_part2]

    return np.prod(solutions_part1), solutions_part2[0]
