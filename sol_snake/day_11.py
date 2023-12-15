from typing import TextIO

import numpy as np
import numpy.typing as nptypes


def expand_universe(universe : list ) -> nptypes.NDArray:
    u_m = np.asarray(universe)

    # lines that are fully 0s (aka, summing over columns will be 0)
    line_indexes = np.nonzero(u_m.sum(axis=1) == 0)[0] # we don't care about the type
    # columns that are fully 0s (aka, summing over lines will be 0)
    col_indexes = np.nonzero(u_m.sum(axis=0) == 0)[0] # we don't care about the type

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

    expanded = expand_universe(universe_matrix)
    galaxies = np.nonzero(expanded)
    coordinates = np.rec.fromarrays([galaxies[0], galaxies[1]]).tolist()

    lowest_distances = []

    for i in range(len(coordinates)):
        coords_a = coordinates[i]
        curr_elem = expanded[coords_a]
        #print("Start", coords_a, curr_elem)

        distances = [manhattan_distance(coords_a, coordinates[j]) for j in  range(i, len(coordinates)) if coords_a != coordinates[j]]
        #print(curr_elem, distances)
        lowest_distances.extend(distances)

    return sum(lowest_distances)
