from enum import Enum
from typing import Self, TextIO

type Bid = int
type HandCards = list[int]
type Bet = tuple[HandCards, Bid]
type Hand = tuple[HandType, HandCards]


class Card:
    symbol: str
    value: int

    def __lt__(self, other: Self):
        return self.value < other.value

    def __eq__(self, other: Self):
        return self.value == other.value

    def __gt__(self, other: Self):
        return self.value < other.value


class HandType(int, Enum):
    # It's easier if we define as ints because
    # c o m p a r i s o n s
    FiveKind = 7  # AAAAA
    FourKind = 6  # AA8AA
    FullHouse = 5  # 23332
    ThreeKind = 4  # TTT98
    TwoPair = 3  # 23432
    Pair = 2  # A23A4
    High = 1  # 23456

    def __str__(self) -> str:
        return self.name


def find_uniques(l: list[int]) -> tuple[int, int]:
    # Okay so, in order to identify the hands we need to basically see how many occurrences we have of the cards
    # A simple way to do that is to just create a bitmap where our criteria is being unique
    # That, together with the number of different chars/numbers in the list, allows to create unique criteria
    uniques_chars = set(l)
    unique_bits = [1 if l.count(i) == 1 else 0 for i in uniques_chars]
    return len(uniques_chars), sum(unique_bits)


def calc_type(hand: HandCards) -> HandType:
    # We're assuming Jokers are 0, but really just needs to be a value that doesn't count so
    jokers = hand.count(0)

    unique, bit_sum = find_uniques(hand)
    if unique == bit_sum:
        # ABCDJ - 5 unique, 1 joker
        # 11111 = 5
        if jokers == 1:
            return HandType.Pair
        # ABCDE - 5 unique
        # 11111 = 5
        return HandType.High
    # here we don't need to check the sum
    elif unique == 4:
        # AABCD - 4 unique
        # 00111 = 3
        if jokers == 0:
            return HandType.Pair
        # we're favoring highest hand type, so consider the rest
        # AABCJ - 4 unique, 1 joker
        # 00111 = 3
        # AJBCJ - 4 unique, 2 joker
        # 10110 = 3
        else:
            return HandType.ThreeKind
    elif unique == 3:
        if bit_sum == 1:
            # AABBC = 3 unique
            # 00001 = 1
            if jokers == 0:
                return HandType.TwoPair
            # AABBJ - 3 unique, 1 joker
            elif jokers == 1:
                return HandType.FullHouse
            # AABJJ - 3 unique, 2 joker
            # 00100 = 1
            else:
                return HandType.FourKind
        elif bit_sum == 2:
            # AAABC - 3 unique
            # 00011 = 2
            if jokers == 0:
                return HandType.ThreeKind
            # AAABJ - 3 unique, 1 joker
            # 00011 = 2
            # AJJBJ - 3 unique, 3 joker
            # 10010 = 2
            else:
                return HandType.FourKind
        else:
            raise ValueError("Impossible to reach here?")
    elif unique == 2:
        # To remain 2 unique, jokers need to replace one or the other, so
        # AAAJJ - 2 unique, 2 jokers
        # JJJBB - 2 unique, 3 jokers
        if jokers > 0:
            return HandType.FiveKind
        # AAABB - 2 unique
        # 00000 = 0
        elif bit_sum == 0:
            return HandType.FullHouse
        # AAAAB - 2 unique
        # 00001 = 1
        else:
            return HandType.FourKind
    elif unique == 1:
        # AAAAA - 1 unique
        # 00000 = 0
        # JJJJJ - 1 unique
        # 00000 = 0
        return HandType.FiveKind
    raise ValueError("Unimplemented, oops")


# We could use Enum, but meh, if YAGNI and it works ok this way, not necessary
symbol_cards = ["A", "K", "Q", "J", "T"]
symbol_values = [14, 13, 12, 11, 10]

name_to_card = {v: symbol_values[i] for i, v in enumerate(symbol_cards)}
card_to_name = {symbol_values[i]: v for i, v in enumerate(symbol_cards)}
# adding the joker so we can still debug
card_to_name[0] = "J"


def hand_as_string(h: HandCards) -> str:
    # Just helper method for debug
    return "".join([str(i) if 1 < i < 10 else card_to_name[i] for i in h])


def hand_key(h: tuple[HandType, HandCards, Bid]) -> tuple[HandType, HandCards]:
    hand_type = h[0]
    cards = h[1]
    return (hand_type, cards)


def parse_input(line: str, *, with_jokers=False) -> tuple[list[int], Bid]:
    hand, bid = line.split(" ")
    bid = int(bid)
    hand = [int(i) if i.isnumeric() else name_to_card[i] for i in hand]
    if with_jokers:
        # best way to make sure it gets priority is we just subtract it
        hand = [i if i != 11 else i - 11 for i in hand]
    return (hand, bid)


def day_7(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    hand_bids: list[Bet]
    hand_bids_2: list[Bet]
    with content as f:
        all_lines = f.readlines()
        hand_bids = [parse_input(line) for line in all_lines]
        hand_bids_2 = [parse_input(line, with_jokers=True) for line in all_lines]

    hands_classified = [(calc_type(h), h, b) for h, b in hand_bids]

    # weakest hand gets rank 1, so
    hands_ranked = sorted(hands_classified, key=hand_key)
    winnings = []
    for i, (t, h, bid) in enumerate(hands_ranked):
        rank = i + 1
        winnings.append(rank * bid)

    # Part 2
    hands_classified_2 = [(calc_type(h), h, b) for h, b in hand_bids_2]
    hands_ranked_2 = sorted(hands_classified_2, key=hand_key)
    winnings_2 = []
    for i, (t, h, bid) in enumerate(hands_ranked_2):
        rank = i + 1
        winnings_2.append(rank * bid)

    return sum(winnings), sum(winnings_2)
