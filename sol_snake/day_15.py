from typing import TextIO


def hash_algo(s) -> int:
    hashed_val = 0
    for c in s:
        # Determine the ASCII code for the current character of the string.
        ascii = ord(c)

        # Increase the current value by the ASCII code you just determined.
        hashed_val += ascii
        # Set the current value to itself multiplied by 17.
        hashed_val *= 17
        # Set the current value to the remainder of dividing itself by 256.
        hashed_val = hashed_val % 256
    return hashed_val
def day_15(content: TextIO, is_example: bool = False) -> tuple[int, int]:

    hashes = []
    with content as f:
        for line in f.read().strip().split(","):
            hashed = hash_algo(line)
            hashes.append(hashed)

    return sum(hashes), 0
