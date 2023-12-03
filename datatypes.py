from enum import Enum

type Coordinate = tuple[int, int]

class Direction(Enum):
    Up = 1
    DiagonalRightUp = 5
    Right = 2
    DiagonalRightDown = 6
    Down = 3
    DiagonalLeftDown = 7
    Left = 4
    DiagonalLeftUp = 8