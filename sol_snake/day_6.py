import math
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


def solve_naive(race_duration: int, record_distance: int) -> int:
    return sum([
        1 if calculates_distance(i, race_duration) > record_distance
        else 0
        for i in range(1, race_duration)
    ])


def solve_smart(race_duration: int, record_distance: int) -> int:
    # we already know beforehand some numbers won't work, so we don't actually need to go through ALL the numbers (Leaking a bit of the calculates_distance method)

    # Given that t := race_duration, r := record_distance, and x := button_time
    # distance = x * (t - x), so that distance >  r
    # which is the same as
    # distance = -x^2 + tx, so that distance > r, which means we just need to find
    # -x^2 + tx > r <=> -x^2 + tx - r > 0
    # which then can be solved using the formula for solving quadratic equations

    sqrt_part = math.sqrt(math.pow(race_duration, 2) - 4 * record_distance)

    # since we're looking for d - r > 0, we need to extend to the nearest integer that still falls within our solutions
    # lower bound with also also include d - r = 0, we'll fix  this in a bit
    lower_bound = math.floor((race_duration - sqrt_part) / 2)
    upper_bound = math.ceil((race_duration + sqrt_part) / 2)

    # Doing this, we're now excluding the d = r solution (the lower root), and all of our ranges will include values such that d - r > 0
    lower_bound = lower_bound + 1

    # Instead, we could also do upper_bound-1
    # But while that'd still solve the exercise (because the length of the interval still is the same), we'd be including solutions outside of our domain
    # i.e we'd be including lower root [d = r] incorrectly

    return len(range(lower_bound, upper_bound))


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

    solutions_part1 = [solve_smart(d, r) for (d, r) in races_info_part1]
    # part 2, we need to assume it's all the same number, so
    races_info_part2 = [(int("".join(time_line)), int("".join(distance_line)))]
    solutions_part2 = [solve_smart(d, r) for d, r in races_info_part2]

    return np.prod(solutions_part1), solutions_part2[0]
