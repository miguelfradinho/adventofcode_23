from enum import Enum
from typing import TextIO

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
    initial_category: Category,
    final_category: Category,
    categories: dict,
    almanac: dict,
) -> int:
    curr_elem = initial_value
    passed_through = [curr_elem]
    curr_category = initial_category
    # search
    while curr_category != final_category:
        # fetch
        almanac_ranges = almanac[curr_category]
        # Get next elem
        for s_min, s_max, diff in almanac_ranges:
            if s_min <= curr_elem < s_max:
                curr_elem = curr_elem + diff
                break
        # if we didnt' break out of for, we don't modify the curr_elem
        # update state
        next_category = categories[curr_category]
        curr_category = next_category
        passed_through.append(curr_elem)
    return passed_through[-1]


def solve_interval(
    initial_value: tuple[int, int],
    initial_category: Category,
    final_category: Category,
    categories: dict,
    almanac: dict,
) -> tuple[int, int]:
    curr_ranges = [initial_value]
    curr_category = initial_category
    # solution by reddit user u/Synedh, in https://www.reddit.com/r/adventofcode/comments/18b4b0r/comment/kc2v876/

    # search
    while curr_category != final_category:
        # fetch
        ranges_to_check = []
        almanac_ranges = almanac[curr_category]

        # Get next elem
        while curr_ranges != []:
            curr_start, curr_end = curr_ranges.pop()
            found_overlap = False
            for ref_start, ref_end, diff in almanac_ranges:
                # e.g for [50, 100]
                # [20, 25] 25 < 50, too far to the left, no overlap
                # [150, 155] 150 > 100, too far to the right, no overlap
                if curr_end <= ref_start or curr_start >= ref_end:
                    # since this interval is mapped to itself, just skip
                    # if in the end we didn't find anything, then we'll append it
                    continue
                # we already checked that there's overlap from here on
                # for same [50, 100]
                # [40, 55], we need to consider the [40,50) interval too so
                if curr_start < ref_start:
                    left_partial = (curr_start, ref_start)
                    curr_ranges.append(left_partial)
                    # since are already including the missing left-side, move our reference to the inner interval
                    curr_start = ref_start
                # for same [50, 100]
                # [75, 110], we need to consider the (100,110] interval
                if curr_end > ref_end:
                    right_partial = (ref_end, curr_end)
                    curr_ranges.append(right_partial)
                    # same as above, move our reference point to the inner interval
                    curr_end = ref_end
                # By this point, we only have the intersection of intervals, so add it
                inner_interval = (curr_start + diff, curr_end + diff)
                ranges_to_check.append(inner_interval)
                found_overlap = True
                break
            if not found_overlap:
                # if we didn't found any overlapping range,
                # that means it doesn't suffer a transformation (diff), so also include it
                non_overlap = (curr_start, curr_end)
                ranges_to_check.append(non_overlap)

        # update state
        next_category = categories[curr_category]
        curr_category = next_category
        # We already finished splitting the intervals, so now we have a pretty streamlined intervals list
        # to check for the next category
        curr_ranges = ranges_to_check

    # whatever we're left are the locations, so just get the local min
    return min(curr_ranges)


def parse_map(lines) -> tuple[Category, Category, list[tuple[int, int, int, int]]]:
    # first line is always the header
    source, destination = lines[0].split(" ")[0].split("-to-")

    ranges_list = []

    for range_line in lines[1:]:
        dest_start, source_start, length = parse_ints(range_line)
        source_end = source_start + length
        diff = dest_start - source_start
        source_to_dest = (source_start, source_end, diff)
        ranges_list.append(source_to_dest)

    return (Category[source], Category[destination], ranges_list)


def day_5(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    seeds: list[int] = [79, 14, 55, 13]

    categories: dict[Category, Category] = {}
    smart_map: dict = {}

    with content as f:
        seeds_line = f.readline().strip()
        seeds = parse_ints(seeds_line.split(" ")[1:])
        f.readline()

        map_lines: list[str] = []
        for line in f.read().split("\n"):
            if line == "":
                source, dest, ranges = parse_map(map_lines)
                categories[source] = dest
                smart_map[source] = ranges
                map_lines = []
            else:
                map_lines.append(line)

    results = []
    for seed in seeds:
        value = solve(seed, Category.seed, Category.location, categories, smart_map)
        results.append(value)

    results_part_2 = []
    for seed_start, seed_length in zip(seeds[::2], seeds[1::2]):
        seed_end = seed_start + seed_length
        initial_seed = (seed_start, seed_end)
        values = solve_interval(initial_seed, Category.seed, Category.location, categories, smart_map)
        results_part_2.extend(values)

    return min(results), min(results_part_2)
