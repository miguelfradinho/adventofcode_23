from collections import deque
from typing import TextIO

from utils import parse_ints


def difference(a : tuple[int,int]) -> int:
    return a[1]-a[0]


def build_differences(history : list[int]) -> deque[list[int]]:
    # so we don't modify it
    start_history = [i for i in history]
    report = deque()
    report.append(start_history)
    to_check = [start_history]
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

def extrapolate_left(report : deque[list[int]]) -> int:
    # turn the report into deques so we can use append left
    report_but_deques = [deque(i) for i in report]
    # le switcheroo to make the iteration easy
    report_but_deques.reverse()
    # initialize
    last_val = 0
    for i in range(len(report_but_deques)):
        curr_line = report_but_deques[i]
        next_val = curr_line[0]
        predicted = next_val - last_val
        curr_line.appendleft(predicted)
        last_val = predicted

    report_but_deques.reverse()
    predicted_value = report_but_deques[0][0]
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

    predictions_left = []
    for history in histories:
        report = build_differences(history)
        predict_left = extrapolate_left(report)
        predictions_left.append(predict_left)

    return sum(predictions), sum(predictions_left)
