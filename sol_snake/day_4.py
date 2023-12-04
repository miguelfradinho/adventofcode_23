from typing import TextIO

type ScratchCard = tuple[int, list[int], list[int]]


def score_card(winning : list[int], having : list[int]) -> int:
    matching = len(set(winning) & set(having))
    if matching == 0:
        return 0
    return 2**(matching-1)

def parse_input(line: str) -> ScratchCard:
    card_id, numbers_part = line.strip().split(":")
    number_card_id = int(card_id.split(" ")[-1])

    winning, having = numbers_part.split("|")
    winning_numbers = [int(i) for i in winning.split(" ") if i != ""]
    having_numbers = [int(i) for i in having.split(" ") if i != ""]
    return (number_card_id, winning_numbers, having_numbers)

def day_4(content: TextIO, is_example: bool = False) -> tuple[int, int]:

    card_points : list[int] = [0]
    part_2_stuff : list[int] = [0]

    cards_list : list[ScratchCard] = []
    winning_numbers : list[int] = []
    numbers_we_have : list[int] = []

    with content as f:
        for line in f:
            card_id, winning_numbers, numbers_we_have = parse_input(line)
            scratch_card = (card_id, winning_numbers, numbers_we_have)
            cards_list.append(scratch_card)

            points_for_card = score_card(winning_numbers, numbers_we_have)
            card_points.append(points_for_card)

    return sum(card_points), sum(part_2_stuff)