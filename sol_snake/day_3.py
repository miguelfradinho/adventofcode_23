import re
from dataclasses import dataclass
from typing import TextIO

from datatypes import Coordinate, Direction
from utils import get_coords

input_pattern = r"(\d+)|[*$+#]"

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
                start,end = part_input.span()
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

def is_adjacent(part : PartNumber, coords : list[Coordinate]) -> bool:
    for i in range(part.range):
        curr_x = part.start_pos[0]+i
        curr_y = part.start_pos[1]
        for d in Direction:
            if get_coords((curr_x,curr_y), d) in coords:
                return True
    return False

def day_3(content: TextIO, is_example: bool = False) -> int:

    all_parts, all_symbols = parse_input(content)
    valid_part_numbers = [0]

    for part in all_parts:
        # so far, for part 1, we don't really about which specific symbol
        symbols_coords = [i.pos for i in all_symbols]
        if is_adjacent(part, symbols_coords):
            valid_part_numbers.append(part.value)
    return sum(valid_part_numbers)