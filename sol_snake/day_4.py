from typing import TextIO

type ScratchCard = tuple[int, list[int], list[int]]


def score_card(winning: list[int], having: list[int]) -> tuple[int, int]:
    matches = len(set(winning) & set(having))
    if matches == 0:
        return (0, 0)
    points = 2 ** (matches - 1)
    return (matches, points)


def parse_input(line: str) -> ScratchCard:
    card_id, numbers_part = line.strip().split(":")
    number_card_id = int(card_id.split(" ")[-1])

    winning, having = numbers_part.split("|")
    winning_numbers = [int(i) for i in winning.split(" ") if i != ""]
    having_numbers = [int(i) for i in having.split(" ") if i != ""]
    return (number_card_id, winning_numbers, having_numbers)


def day_4(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    card_points: list[int] = [0]
    cards_list: list[ScratchCard] = []
    winning_numbers: list[int] = []
    numbers_we_have: list[int] = []

    # we'll need this for part 2
    card_matches: dict[int, int] = {}

    with content as f:
        for line in f:
            card_id, winning_numbers, numbers_we_have = parse_input(line)
            scratch_card = (card_id, winning_numbers, numbers_we_have)
            cards_list.append(scratch_card)
            matches, points = score_card(winning_numbers, numbers_we_have)
            card_points.append(points)
            # for part 2
            # saving how many matches we found for this card
            card_matches[card_id] = matches

    # Instead of iterating a second time over this dict, we could have also done it on the first for
    # with having some default logic for our first-key access
    # However, that'd be quite a bit less clear, so we opted this way
    card_counts = {c: 1 for c in card_matches.keys()}
    for card_id, matches in card_matches.items():
        # Number of copies (+ original) we ha
        current_copies = card_counts[card_id]
        # we need to add + 1 because we want to start at the next
        for i in range(card_id + 1, card_id + matches + 1):
            card_counts[i] += 1 * current_copies
    return sum(card_points), sum([i for i in card_counts.values()])
