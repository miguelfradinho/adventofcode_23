from typing import TextIO

import numpy as np
import numpy.typing as nptypes

from datatypes import Coordinate
from utils import manhattan_distance


def find_indices_to_expand(matrix: nptypes.NDArray):
    # lines that are fully 0s (aka, summing over columns will be 0)
    line_indexes = np.nonzero(matrix.sum(axis=1) == 0)[
        0
    ]  # we don't care about the type
    # columns that are fully 0s (aka, summing over lines will be 0)
    col_indexes = np.nonzero(matrix.sum(axis=0) == 0)[0]  # we don't care about the type

    return line_indexes, col_indexes


def expand_universe(u_m: nptypes.NDArray) -> nptypes.NDArray:
    line_indexes, col_indexes = find_indices_to_expand(u_m)
    # insert the lines as 0
    expanded_lines = np.insert(u_m, line_indexes, 0, axis=0)
    # insert the news colums at those indexes with 0
    return np.insert(expanded_lines, col_indexes, 0, axis=1)


def naive_find_expanded_coordinates(matrix: nptypes.NDArray) -> list[Coordinate]:
    # Expand the universe
    expanded = expand_universe(matrix)
    # Find non zero values
    galaxies = np.nonzero(expanded)
    # Get their coordinates
    expanded_coords = np.rec.fromarrays([galaxies[0], galaxies[1]]).tolist()
    return expanded_coords


def smart_find_expanded_coordinates(
    matrix: nptypes.NDArray, expand_by: int = 2
) -> list[Coordinate]:
    """
    Parameters
    ----------
    matrix : nptypes.NDArray
        Our universe
    expand_by : int, optional
        How much larger the empty space really is, by is 2x the size

    Returns
    -------
    list[Coordinate]
        List of coordinates of the galaxies in the expanded universe
    """

    # We need to be a little smarter about it, since it's perhaps not a good idea to do insertion 1M times
    # Instead of expanding the matrix, just get the coordinates directly
    galaxies = np.nonzero(matrix)
    coordinates_orig = np.rec.fromarrays([galaxies[0], galaxies[1]]).tolist()

    # find which lines/columns will be neededed to expand
    lines_i, cols_i = find_indices_to_expand(matrix)

    # doing -1 since we need to account for the galaxies already in there
    expansion_factor = expand_by - 1

    expanded_coords = []
    for x, y in coordinates_orig:
        new_x = x
        new_y = y
        # count how many expansions (X-coord shifts) we'll have to make
        lines = sum([1 if x > i else 0 for i in lines_i])
        if lines != 0:
            new_x = x + lines * expansion_factor

        # do the same for the columns (Y-Coord shifts)
        cols = sum([1 if y > i else 0 for i in cols_i])
        if cols != 0:
            new_y = y + cols * expansion_factor
        expanded_coords.append((new_x, new_y))
    return expanded_coords

def calculate_distances(coordinates: list[Coordinate]) -> list[int]:
    total_coords = len(coordinates)
    return [
        manhattan_distance(coordinates[i], coordinates[j])
        for i in range(total_coords)
        for j in range(i, total_coords)
        if coordinates[i] != coordinates[j]
    ]


def day_11(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    universe_matrix = []
    galaxy_count = 1
    with content as f:
        for line in f:
            line = line.strip()
            le_numbers = []
            for i in line:
                le_val = 0
                if i == "#":
                    le_val = galaxy_count
                    galaxy_count += 1
                le_numbers.append(le_val)
            universe_matrix.append(le_numbers)

    u_m = np.asarray(universe_matrix)
    coordinates_part1 = naive_find_expanded_coordinates(u_m)
    distances_part1 = calculate_distances(coordinates_part1)

    # part 2
    coordinates_part2 = smart_find_expanded_coordinates(u_m, expand_by=1000 * 1000)
    distances_part2 = calculate_distances(coordinates_part2)

    return sum(distances_part1), sum(distances_part2)
