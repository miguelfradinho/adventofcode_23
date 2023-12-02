import math
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


def check_limits_and_calc_power(game_info: str) -> tuple[bool, int]:
    maximums = {
        CubeType.Blue: 0,
        CubeType.Green: 0,
        CubeType.Red: 0,
    }
    any_exceeds_limit = False
    for cube_set in game_info.split(SET_SEPARATOR):
        for cube_info in cube_set.strip().split(ITEM_SEPARATOR):
            cube = parse_cube_info(cube_info)

            current_max = maximums.get(cube.cube_type, 0)
            if cube.quantity > current_max:
                maximums[cube.cube_type] = cube.quantity
            if not any_exceeds_limit:
                limit = get_limit(cube.cube_type)
                if cube > limit:
                    any_exceeds_limit = True

    cube_set_power = math.prod(maximums.values())
    return (any_exceeds_limit, cube_set_power)


def day_2(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    all_game_ids: list[GameId] = []

    valid_ids: list[GameId] = []
    powers: list[int] = []

    for line in content:
        game_id, game_info = parse_game_record(line)
        all_game_ids.append(game_id)
        any_exceed_limit, cube_set_power = check_limits_and_calc_power(game_info)
        powers.append(cube_set_power)
        if any_exceed_limit:
            valid_ids.append(game_id)

    return sum(valid_ids), sum(powers)
