import re
from typing import TextIO

grouping_digits = re.compile(r"(\d)(.*(\d))?")


def day_1(content: TextIO, is_example: bool = False) -> int:
    numbers: list[int] = []
    for line in content:
        clean = line.strip()
        result = re.search(grouping_digits, clean)
        print(clean, result)
        if result is not None:
            result = result.group()
            first, last = result[0], result[-1]
            number = f"{first}{last}"
            numbers.append(int(number))

    return sum(numbers)
