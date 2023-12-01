import os
import typing
from os import path

FILES_FOLDER : str = "data"

def get_file(file_name : str, ext : str ="txt"):
    file_with_ext = f"{file_name}.{ext}"
    #print(os.getcwd())
    #print(os.path.abspath(os.path.dirname(__file__)))

    path_to_file = path.join(os.getcwd(), FILES_FOLDER, file_with_ext)
    return open(path_to_file, "r", encoding="utf-8")

def get_exercise_file(day: int) -> typing.TextIO:
    exercise_format = f"{day}_input"
    return get_file(exercise_format)


def get_example_file(day: int, part: int = 1) -> typing.TextIO:
    part_prefix = ""
    if part > 1:
        part_prefix = f"_{part}"

    example_format = f"{day}_example{part_prefix}"
    return get_file(example_format)