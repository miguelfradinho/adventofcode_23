from enum import Enum
from typing import TextIO

import portion as P

from utils import parse_ints


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
        ranges = category_ranges[curr_category]
        next_category = category_path_map[curr_category]

        # Do
        for s_start, d_start, diff, length  in ranges:
            s_min = s_start
            s_max =  s_start + length-1
            if s_min <= curr_elem <= s_max:
                curr_elem = curr_elem + diff
        # update state
        curr_category = next_category
        passed_through.append(curr_elem)
    return passed_through[-1]

def parse_map(lines) -> tuple[Category, Category, list[tuple[int,int, int, int]]]:
    # first line is always the header
    source, destination = lines[0].split(" ")[0].split("-to-")

    possible_sources = []
    possible_destination = []
    ranges_list = []
    for range_line in lines[1:]:
        dest_start, source_start, length = parse_ints(range_line)

        source_interval = P.closedopen(source_start, source_start+length)
        dest_interval =  P.closedopen(dest_start, dest_start+length)

        possible_sources.append(source_interval)
        possible_destination.append(dest_interval)
        source_to_dest = (source_start, dest_start, dest_start - source_start, length)
        ranges_list.append(source_to_dest)

    union_source = possible_sources[0]
    for source_int in possible_sources[1:]:
        union_source = union_source | source_int

    union_dest = possible_destination[0]
    for dest_int in possible_destination[1:]:
        union_dest = union_dest | dest_int

    return (Category[source], Category[destination], ranges_list, union_source, union_dest)


def day_5(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    seeds : list[int] = [79, 14, 55, 13]

    categories : dict[Category, Category] = {}
    smart_map : dict = {}

    with content as f:
        seeds_line = f.readline().strip()
        seeds = parse_ints(seeds_line.split(" ")[1:])
        f.readline()

        map_lines : list[str] = []
        for line in f.read().split("\n"):
            if line == "":
                source, dest, ranges, s_union, d_union = parse_map(map_lines)
                categories[source] = dest
                smart_map[source] = (ranges,  s_union, d_union)
                map_lines = []
            else:
                map_lines.append(line)



    #results = []
    #for seed in seeds:
    #    value = solve(seed, Category.seed, Category.location, categories, smart_map)
    #    print(seed, value)
    #    results.append(value)

    print("Starting part 2")
    for seed_start, seed_length in zip(seeds[::2], seeds[1::2]):
        curr_category = Category.seed
        seed_interval = P.closedopen(seed_start, seed_start+seed_length)
        ranges, s_union, d_union = smart_map[curr_category]

        print(seed_interval,"Checking" , s_union, d_union)



    return 0, 0 #min(results), 0