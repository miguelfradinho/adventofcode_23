from typing import TextIO

import numpy as np


def day_6(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    # part 1
    races_information = [
        (7, 9), # duration (ms), distance (mm)
        (15,40),
        (30, 200),
    ]

    # part 2
    races_information =[
        (54817088, 446129210351007),
    ]
    ways_per_race = []
    for duration, record in races_information:
        ways_of_beating_record = 0
        for button_time in range(1, duration):
            remaining_duration = duration - button_time
            distance_traveled = button_time * remaining_duration
            if (distance_traveled > record):
                ways_of_beating_record += 1
        ways_per_race.append(ways_of_beating_record)
    return np.prod(ways_per_race), 0