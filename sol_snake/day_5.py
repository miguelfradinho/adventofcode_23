from dataclasses import dataclass
from enum import Enum
from typing import TextIO

from utils import parse_ints


def day_5_boo(content: TextIO, is_example: bool = False) -> tuple[int, int]:

    seeds : list[int]
    maps : dict[Mapping, list[tuple[range, range]]]

    with content as f:
        # First line is always seeds
        seeds_line = f.readline().strip()
        seeds = parse_ints(seeds_line.split(" ")[1:])
        # getting rid of the next blank line
        f.readline()

        # reading the map
        # map_header
        source, destination = f.readline().split(" ")[0].split("-to-")
        mapping = Mapping(Category[source], Category[destination])


        map_ranges = []
        for line in f.readlines():
            start, dest, length = parse_ints(line)
            range_start = range(start, start+length)
            range_dest = range(dest, dest+length)
            map_ranges.append((range_start, range_dest))

        print(mapping, map_ranges)
    return 0, 0


class CategoryNew(int, Enum):
    seed = 1
    soil = 2
    fertilizer = 3
    light = 4
    temperature = 5
    humidity = 6
    location = 7

class Category(str, Enum):
    seed = "seed"
    soil = "soil"
    fertilizer = "fertilizer"
    water = "water"
    light = "light"
    temperature = "temperature"
    humidity = "humidity"
    location = "location"

    def __repr__(self) -> str:
        return self.value

@dataclass
class Mapping:
    source : Category
    destination : Category
    def __hash__(self) -> int:
        return hash((self.source, self.destination))




def next_value(elem : int, source_range : list, next_range : list) -> int:
    try:
        return next_range[source_range.index(elem)]
    except ValueError:
        return elem

def solve(
        initial_value: int,
        initial_category : Category,
        final_category : Category,
        category_path_map : dict,
        category_ranges: dict) -> int:
    # init
    passed_through = [initial_value]
    curr_category = initial_category
    curr_elem = initial_value
    # search
    while curr_category != final_category:
        # fetch
        source, dest = category_ranges[curr_category]
        next_category = category_path_map[curr_category]

        # do
        curr_elem = next_value(curr_elem, source, dest)

        # update state
        curr_category = next_category
        passed_through.append(curr_elem)
    return passed_through[-1]

def parse_map(lines) -> tuple[tuple[Category, list[int]], tuple[Category, list[int]]]:
    # first line is always the header
    source, destination = lines[0].split(" ")[0].split("-to-")
    source_list = []
    dest_list = []

    for range_line in lines[1:]:
        dest_start, source_start, length = parse_ints(range_line)
        range_source_start = range(source_start, source_start+length)
        range_dest = range(dest_start, dest_start+length)
        source_list.extend(range_source_start)
        dest_list.extend(range_dest)

    return (Category[source], source_list), (Category[destination], dest_list)

def day_5(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    seeds : list[int]

    #maps : dict[Mapping, list[tuple[range, range]]]
    categories : dict[Category, Category] = {}
    range_map : dict[Category, tuple[list, list]]= {}

    with content as f:
        # First line is always seeds
        seeds_line = f.readline().strip()
        seeds = parse_ints(seeds_line.split(" ")[1:])
        # getting rid of the next blank line
        f.readline()

        map_lines : list[str] = []
        for line in f.read().split("\n"):
            if line == "":
                source_info, dest_info = parse_map(map_lines)
                source_category, source_range = source_info
                dest_category, dest_range = dest_info
                categories[source_category] = dest_category
                range_map[source_category] = (source_range, dest_range)
                map_lines = []
            else:
                map_lines.append(line)
        #print(categories, range_map)

    results = []
    for seed in seeds:
        value = solve(seed, Category.seed, Category.location, categories, range_map)
        print(seed, value)
        results.append(value)
    return min(results)