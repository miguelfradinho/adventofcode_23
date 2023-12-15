from typing import TextIO

import numpy as np
import numpy.typing as nptypes


def find_indices_to_expand(matrix : nptypes.NDArray):
    # lines that are fully 0s (aka, summing over columns will be 0)
    line_indexes = np.nonzero(matrix.sum(axis=1) == 0)[0] # we don't care about the type
    # columns that are fully 0s (aka, summing over lines will be 0)
    col_indexes = np.nonzero(matrix.sum(axis=0) == 0)[0] # we don't care about the type

    return line_indexes, col_indexes
def expand_universe(u_m :  nptypes.NDArray) -> nptypes.NDArray:
    line_indexes, col_indexes = find_indices_to_expand(u_m)
    # insert the lines as 0
    expanded_lines = np.insert(u_m, line_indexes, 0, axis=0)
    # insert the news colums at those indexes with 0
    return np.insert(expanded_lines, col_indexes, 0, axis=1)

def manhattan_distance(a, b):
    #print(a,b)
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

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
    expanded = expand_universe(u_m)
    galaxies = np.nonzero(expanded)
    coordinates = np.rec.fromarrays([galaxies[0], galaxies[1]]).tolist()

    lowest_distances = []

    for i in range(len(coordinates)):
        coords_a = coordinates[i]
        distances = [manhattan_distance(coords_a, coordinates[j]) for j in  range(i, len(coordinates)) if coords_a != coordinates[j]]
        lowest_distances.extend(distances)


    # part 2
    # We need to be a little smarter about it, since it's perhaps not a good idea to do insertion 1M times
    non_expanded_galaxies = galaxies = np.nonzero(u_m)
    lines_i, cols_i = find_indices_to_expand(u_m)
    non_expanded_coords = np.rec.fromarrays([non_expanded_galaxies[0], non_expanded_galaxies[1]]).tolist()

    # How large galaxies really are
    times_larger = 1000*1000
    # doing -1 since we need to account for the galaxy already in there
    expansion_factor = times_larger - 1
    new_coords = []
    for x,y in non_expanded_coords:
        new_x = x
        new_y = y
        # count how many empty lines were found for this x
        lines = sum([1 if x > i else 0 for i in lines_i])
        if lines != 0:
            new_x = x + lines * expansion_factor

        cols = sum([1 if y > i else 0 for i in cols_i])
        if cols != 0:
            new_y = y + cols * expansion_factor
        new_coords.append((new_x, new_y))

    lowest_distances_part2 = []
    for i in range(len(new_coords)):
        coords_a = new_coords[i]
        distances = [manhattan_distance(coords_a, new_coords[j]) for j in  range(i, len(new_coords)) if coords_a != new_coords[j]]
        lowest_distances_part2.extend(distances)

    return sum(lowest_distances), sum(lowest_distances_part2)
