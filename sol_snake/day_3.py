import re
from dataclasses import dataclass
from typing import TextIO

from datatypes import Coordinate, Direction
from utils import get_coords


@dataclass
class Symbol:
    pos : Coordinate
    value : str

    def __repr__(self) -> str:
        return f"Symbol<\"{self.value}\", line={self.pos[1]}, pos={self.pos[0]})>"

@dataclass
class PartNumber:
    start_pos : Coordinate
    range : int
    value : int

    def __repr__(self) -> str:
        return f"PartNumber<value={self.value}, line={self.start_pos[1]}, range={range}>"

def parse_input(content: TextIO) -> tuple[list[PartNumber], list[Symbol]]:
    parts = []
    symbols = []

    part_pattern = r"(\d+)"
    symbol_pattern = r"[#$*%=\-&+/@?~^]"
    with content as f:
        y_coord = 0
        for line in f:
            for part_input in re.finditer(part_pattern, line):
                # start is always index of the first match
                start, end = part_input.span()
                # end - start is always the range of the match (similar to how spawn does)
                number_size = end - start
                value = part_input.group()
                part = PartNumber((start,y_coord), number_size, int(value))
                parts.append(part)

            for symbol_input in re.finditer(symbol_pattern, line):
                pos = symbol_input.start()
                value = symbol_input.group()
                symbol = Symbol((pos, y_coord), value)
                symbols.append(symbol)
            y_coord += 1

    return parts, symbols

def part_is_adjacent(part : PartNumber, coords : list[Coordinate]) -> bool:
    # numbers are only horizontal, so y is always the same
    y = part.start_pos[1]
    for i in range(part.range):
        # x changes because of the number position
        x = part.start_pos[0]+i
        any_adjacent, _ = find_adjacent_coords((x,y), coords)
        if any_adjacent:
            return True
    return False

def find_adjacent_coords(pos : Coordinate, coords : list[Coordinate]) -> tuple[bool, list[Coordinate]]:
    adjacent_coords = [get_coords(pos,d) for d in Direction if (get_coords(pos,d) in coords)]
    return (adjacent_coords != [], adjacent_coords)

def day_3(content: TextIO, is_example: bool = False) -> tuple[int, int]:

    all_parts, all_symbols = parse_input(content)
    valid_part_numbers = []

    # For part 1, we don't really about which specific symbol
    symbols_coords = [i.pos for i in all_symbols]
    # first part
    for part in all_parts:
        # Part 1
        if part_is_adjacent(part, symbols_coords):
            valid_part_numbers.append(part.value)

    # Part 2, gear ratios
    gear_ratios = []
    valid_symbols = [i for i in all_symbols if i.value == "*"]
    # this is a very ugly solution because our Part 1 solution is inverted from part 2, so we need an unique way of identifying the numbers to be unique and not duplicating...
    parts_coord_map = {
        (p.start_pos[0]+i, p.start_pos[1]) : p.value
        for p in all_parts for i in range(p.range)
    }

    for i in valid_symbols:
        _, adjacent_coords = find_adjacent_coords(i.pos, list(parts_coord_map.keys()))
        # this is very likely to fail on very specific input, since we're relying on non-duplicates
        numbers_adjacent = list(set([parts_coord_map[j] for j in adjacent_coords]))

        if len(numbers_adjacent) == 2:
            first, second = numbers_adjacent
            ratio = first * second
            gear_ratios.append(ratio)

    return sum(valid_part_numbers), sum(gear_ratios)