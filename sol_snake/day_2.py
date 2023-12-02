from enum import Enum
from typing import Self, TextIO

SET_SEPARATOR = ";"
ITEM_SEPARATOR = ","
type GameId = int
type GameRecord = tuple[GameId, str]

class CubeType(str, Enum):
    Red = "red"
    Green = "green"
    Blue = "blue"


class CubeInfo:
    def __init__(self, cube_type: CubeType, number: int):
        self.cube_type = cube_type
        self.quantity = number

    def __eq__(self, other: Self) -> bool:
        return (self.cube_type == other.cube_type) and (self.quantity == other.quantity)

    def __gt__(self, other: Self) -> bool:
        return (self.cube_type == other.cube_type) and (self.quantity > other.quantity)

    def __lt__(self, other: Self) -> bool:
        return (self.cube_type == other.cube_type) and (self.quantity < other.quantity)


def parse_cube_info(cube_info: str) -> CubeInfo:
    number, color = cube_info.strip().split(" ")
    color_type: CubeType
    match color:
        case CubeType.Red:
            color_type = CubeType.Red
        case CubeType.Blue:
            color_type = CubeType.Blue
        case CubeType.Green:
            color_type = CubeType.Green
        case _:
            raise NotImplementedError(f"Unimplemented color: {color}")
    return CubeInfo(color_type, int(number))

def parse_game_record(line: str) -> GameRecord:
    id_info, game_info = line.strip().split(":")
    id_number = int(id_info.split(" ")[1])
    return (id_number, game_info.strip())


MaxRed = CubeInfo(CubeType.Red, 12)
MaxGreen = CubeInfo(CubeType.Green, 13)
MaxBlue = CubeInfo(CubeType.Blue, 14)

def get_limit(cube_type: CubeType) -> CubeInfo:
    match cube_type:
        case CubeType.Red:
            return MaxRed
        case CubeType.Blue:
            return MaxBlue
        case CubeType.Green:
            return MaxGreen
        case _:
            raise NotImplementedError(f"Unimplemented color: {cube_type}")

def all_cubes_within_limit(game_info : str) -> bool:
    for cube_set in game_info.split(SET_SEPARATOR):
        for cube_info in cube_set.strip().split(ITEM_SEPARATOR):
            cube = parse_cube_info(cube_info)
            limit = get_limit(cube.cube_type)
            if cube > limit:
                return False
    return True


def day_2(content: TextIO, is_example: bool = False) -> int:
    all_game_ids: list[GameId] = []
    valid_ids : list[GameId] = []

    for line in content:
        game_id, game_info = parse_game_record(line)
        all_game_ids.append(game_id)
        if all_cubes_within_limit(game_info):
            valid_ids.append(game_id)

    return sum(valid_ids)
