from collections import deque
from typing import TextIO

from utils import parse_ints


def difference(a : tuple[int,int]) -> int:
    return a[1]-a[0]


def build_differences(history : list[int]) -> deque[list[int]]:
    report = deque()
    report.append(history)
    to_check = [history]
    while to_check != []:
        curr = to_check.pop()
        diff = list(map(difference, zip(curr[:-1], curr[1:])))
        if any([i for i in diff if i != 0]):
            to_check.append(diff)
        report.append(diff)

    return report

def extrapolate(report : deque[list[int]]) -> int:
    # le switcheroo to make the iteration easy
    report.reverse()
    # initialize
    last_val = 0
    for i in range(len(report)):
        curr_line = report[i]
        next_val = curr_line[-1]
        predicted = next_val + last_val
        curr_line.append(predicted)
        last_val = predicted

    report.reverse()
    predicted_value = report[0][-1]
    return predicted_value


def day_9(content: TextIO, is_example: bool = False) -> tuple[int, int]:

    histories = []
    with content as f:
        histories = [parse_ints(line.strip()) for line in f]

    predictions = []
    for history in histories:
        report = build_differences(history)
        predict = extrapolate(report)
        predictions.append(predict)

    #print(predictions)
    return sum(predictions)
