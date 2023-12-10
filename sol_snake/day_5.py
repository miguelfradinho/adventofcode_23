from enum import Enum
from typing import Optional, Self, TextIO

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
    category_path_map: dict,
    category_ranges: dict,
) -> int:
    # init
    passed_through = initial_value
    curr_category = initial_category
    curr_elem = initial_value
    # search
    while curr_category != final_category:
        # fetch
        ranges = category_ranges[curr_category]
        next_category = category_path_map[curr_category]

        # Do
        # found = False
        for s_start, d_start, diff, length in ranges:
            s_min = s_start
            s_max = s_start + length - 1
            # print(f"{curr_elem} within ({s_min}, {s_max}) to map to ({d_start}, {d_start+length})")
            if s_min <= curr_elem <= s_max:
                # print(f"Found it, mapping it to {curr_elem+diff}")
                curr_elem = curr_elem + diff
                # found = True
                break
        # if not found:
        #    print(f"Welp, keeping {curr_elem}")
        # update state
        curr_category = next_category
        passed_through = curr_elem
    return passed_through


def parse_map(lines) -> tuple[Category, Category, list[tuple[int, int, int, int]]]:
    # first line is always the header
    source, destination = lines[0].split(" ")[0].split("-to-")

    ranges_list = []

    for range_line in lines[1:]:
        dest_start, source_start, length = parse_ints(range_line)
        range_start = source_start
        range_end = source_start + length - 1
        transformation = dest_start - source_start
        source_to_dest = (range_start, range_end, transformation, length)
        ranges_list.append(source_to_dest)

    # because we're dealing with intervals, it's easier to check them when they're ordered
    sorted_ranges = sorted(ranges_list, key=lambda x: (x[0],x[1]))

    print(sorted([i[2] for i in sorted_ranges], key=lambda x: x))
    return (Category[source], Category[destination], sorted_ranges)

def ranges_overlap(x : tuple[int, int], y : tuple[int, int]) -> True:
    """
    Perhaps not the mathematical definition, but we've defined as such

    Returns
    -------
    bool
        Returns True if Y is completely contained in X e.g. given
        x = [0, 10) and y = [2, 9) -> True

    """
    return 0
    #seed_start <= s_max and seed_start+seed_length >= s_min

# Le rustic implementation of an augmented tree
# see https://en.wikipedia.org/wiki/Interval_tree#Augmented_tree
class TreeNode:
    left_node : Optional[Self] = None
    right_node : Optional[Self] = None

    low_bound : int
    high_bound : int
    diff_to_map : int
    subtree_max : int

    def __init__(self, source_start: int, diff:int, length:int):
        # Our interval will be [low_bound, high_bound]
        self.low_bound = source_start
        self.high_bound = source_start + length -1
        self.diff_to_map = diff

        # when we're initalizing, we don't have any frame of reference, so
        self.subtree_max = self.high_bound

    def add_node(self, other : Self):
        # Not 100% self-balancing, but close enough given it doesn't get misused

        # If we're adding a node in which we can reach a higher interval than we already have, match that
        if self.subtree_max < other.subtree_max:
            self.subtree_max = other.subtree_max
        # adding to the left, where
        if self.low_bound > other.low_bound:
            # if we don't have subtrees just add it
            if self.left_node is None:
                self.left_node = other
            else:
                # if we do, instead add to the subtree
                self.left_node.add_node(other)
        # adding to the right
        # self.low_bound <= other.low_bound
        else:
            if self.right_node is None:
                self.right_node = other
            else:
                # if we do, instead add to the subtree
                self.right_node.add_node(other)

    def __repr__(self) -> str:
        return f"[{self.low_bound}, {self.high_bound}] ({self.subtree_max}) -> {self.diff_to_map}"



    def is_in(self, r_min, r_max) -> tuple[bool,int,int,int]:
        found = False
        found_diff = -1
        # check if it's completely contained, trivial solution
        if self.low_bound <= r_max and self.high_bound >= r_min:
            print("found it", self.low_bound, self.high_bound, self.diff_to_map)
            found = True
            found_diff = self.diff_to_map
        elif self.subtree_max >= r_min:
            print("Going down")
            if self.subtree_max >= r_max:
                found, found_diff, _, _ = self.left_node.is_in(r_min, r_max)
            else:
                found, found_diff, _, _ = self.right_node.is_in(r_min, r_max)
        # self.subtree_max < r_min
        else:
            print("Searching", self.low_bound, self.high_bound)
            found, found_diff, _, _ = self.right_node.is_in(r_min, r_max)

        return (found, found_diff, 0, 0)


def compare_intervals(reference : tuple[int,int], other : tuple[int, int]) -> tuple[bool,str]:
    # returns
    # Overlap, IsContained, Left | Right

    # edge case, they're the same interval
    r_low, r_high = reference
    o_low, o_high = other
    if o_low == r_low and  o_high == r_high:
        return True, 0, 0, "Same interval"
    # Other is contained completely in reference
    elif o_low >= r_low and o_high <= r_high:
        return True, 0, 1, "Is Contained in Reference"
    # Other contains completely reference
    elif r_low >= o_low and r_high <= o_high:
        print(reference, other)
        return True, 0, -1, "Other contains Reference"

    # Other doesn't overlap, and it's to the left of reference
    elif o_high < r_low:
        return False, -1, None, "Left, no overlap"
    elif o_low > r_high:
        return False, 1, None, "Right, no overlap"

    elif o_low < r_low and o_high <= r_high:
        return True, -1, r_low-o_low, "Left, partly overlap"
    elif o_low >= r_low and o_high > r_high:
        return True, 1, o_high-r_high, "Right, partly overlap"
    else:
        raise ArithmeticError("We should never reach here")

def day_5(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    """
    root = TreeNode(20,4, 17)
    print("root", root)

    root_left = TreeNode(3, 3, 39)
    print("Left of root", root_left)
    root.add_node(root_left)

    root_left_left = TreeNode(0,1,2)
    root_left_right = TreeNode(10, 2, 6)
    root.add_node(root_left_left)
    root.add_node(root_left_right)

    #print("Potato", root, root.left_node, root.left_node.right_node)
    #print("Root", root)
    #root_left.add_node(root_left_right)


    c = TreeNode(29,5, 71)
    root.add_node(c)
    #print("Root", root)
    source, length= 40, 21
    start, end = source, source + length -1

    overlapping_interval = root.is_in(start, end)
    expected = (True, 5, 0, 0)
    print((start,end), overlapping_interval, overlapping_interval == expected)
    return
    """
    """
    seeds: list[int] = [79, 14, 45, 13]

    my_ranges = [(98, 50, -48, 2), (50, 52, 2, 48)]

    seed_min, seed_max = (45, 45+14-1)
    for s, d, diff, l in sorted(my_ranges, key=lambda x: x[0]+x[3]):

        node_min = s
        node_max = s+l-1

        print(node_min, node_max, "from", s,d,diff,l)

        # Edge case, no overlap (technically we don't need to check)
        print(f"{seed_min} < {node_min} and {seed_max} > {node_max}")
        if seed_min < node_min and seed_max > node_max:
            print("No overlap at all")
        # Edge  case, fully contained
        elif seed_min >= node_min and seed_max <= node_max:
            print(f"{seed_min} >= {node_min} and {seed_max} <= {node_max}")
            print("fully, contained", diff)
        # Big case
        else:
            # There's not overlap on the left side only
            if seed_min < node_min:
                print("Left side doesn't overlap, don't change", list(range(seed_min, node_min)))
    return
    """

    # maps : dict[Mapping, list[tuple[range, range]]]
    categories: dict[Category, Category] = {
        #Category.seed : Category.soil,
        #Category.soil : Category.fertilizer
    }
    # range_map : dict[Category, tupl e[list, list]]= {}
    smart_map: dict = {
        #Category.seed: [(98, 50, -48, 2), (50, 52, 2, 48)],
        #Category.soil:  [(15, 0, -15, 37), (52, 37, -15, 2), (0, 39, 39, 15)],
    }

    with content as f:
        # First line is always seeds
        seeds_line = f.readline().strip()
        seeds = parse_ints(seeds_line.split(" ")[1:])
        # getting rid of the next blank line
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
        # print(categories, range_map)


    def get_next_number(seed_interval, ref_intervals):
        intervals_transform = []
        le_contains = []
        with_overlaps = []
        for low, high, diff, _ in ref_intervals:
            ref = (low, high)
            comparison = compare_intervals(ref, seed_interval)
            has_overlap, direction, cutoff, _  = comparison
            if has_overlap:
                with_overlaps.append((ref, diff, comparison))

        for ref_range, transform, result  in sorted(with_overlaps, key=lambda x: x[-1][1]):
            _, direction, cutoff, _ = result
            if direction != 0:
                print(result)
            else:
                le_contains.append((ref_range, result))
        print(le_contains)
        print("--------------")

    for seed_start, seed_length in zip(seeds[::2], seeds[1::2]):
        seed_interval =  (seed_start, seed_start+seed_length-1)
        curr_category = Category.seed
        ranges = smart_map[curr_category]
        next_number = get_next_number(seed_interval, ranges)

        break
    return
    # part 1
    results = []
    for seed in seeds:
        # print("------------------")
        value = solve(seed, Category.seed, Category.location, categories, smart_map)
        # print(seed, value)
        results.append(value)

    # part 2
    results_part_2 = []


    return
    print("Starting part 2")
    for seed_start, seed_length in zip(seeds[::2], seeds[1::2]):
        local_vals = []
        start_cat = Category.seed
        curr_category = start_cat
        # let's just think 1 level deep
        ranges = smart_map[curr_category]
        for s_start, d_start, diff, length in ranges:
            s_min = s_start
            s_max = s_start + length - 1

            # everything inclosed, best case
            if seed_start <= s_max and seed_start+seed_length >= s_min:
                print(seed_start, seed_length, s_start, d_start, diff, length)
                break
            else:
                print("Not found, ", s_start)


        return
        for seed in range(seed_start, seed_start+seed_length):
            curr_category = Category.seed
            # 1 deep only
            ranges = smart_map[curr_category]
            found = -1
            #next_category = category_path_map[curr_category]
            for s_start, d_start, diff, length in ranges:
                s_min = s_start
                s_max = s_start + length - 1
                # print(f"{curr_elem} within ({s_min}, {s_max}) to map to ({d_start}, {d_start+length})")
                if s_min <= seed <= s_max:
                    # print(f"Found it, mapping it to {curr_elem+diff}")
                    found = seed + diff
                    print(found)
                    break
            if found == -1:
                print("Not found, using ", seed)
                found = seed
            local_vals.append(found)
            print(f"Finished {seed}", local_vals)
        results_part_2.append(min(local_vals))
        local_vals = []
    """
    for seed_start, seed_length in zip(seeds[::2], seeds[1::2]):
        local_vals = []
        for seed in range(seed_start, seed_start+seed_length):
            le_start = (seed_start, seed)
            value = solve(seed, Category.seed, Category.location, categories, smart_map)
            local_vals.append(value)
        results_part_2.append(min(local_vals))
    """
    return min(results), min(results_part_2)
