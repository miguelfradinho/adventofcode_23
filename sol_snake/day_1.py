import re
from typing import TextIO

digits = {
    "one" : 1,
    "two" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5,
    "six" : 6,
    "seven" : 7,
    "eight" : 8,
    "nine" : 9
}

pattern_part_1 = r"(\d)(.*(\d))?"
# TODO: maybe try to make this cleaner?
# if you put +, it misses the right answer by 6...
pattern_part_2 = r"(one|two|three|four|five|six|seven|eight|nine|\d)(?:.*(one|two|three|four|five|six|seven|eight|nine|\d))?"

valid_part_1 = re.compile(pattern_part_1)
valid_part_2 = re.compile(pattern_part_2)

def number_pls(number_or_word : str) -> int:
    try:
        num = digits.get(number_or_word)
        return num if num is not None else int(number_or_word)
    except ValueError:
        raise ValueError(f"Error trying to convert {number_or_word} to an int")

def day_1(content: TextIO, is_example: bool = False) -> int:
    numbers: list[int] = []
    for line in content:
        clean = line.strip()
        result = re.search(valid_part_2, clean)
        if result is not None:
            first, last = result.groups()
            last = first if last is None else last
            #print(first, last)
            first = number_pls(first)
            last = number_pls(last)
            number = f"{first}{last}"
            numbers.append(int(number))

    return sum(numbers)
