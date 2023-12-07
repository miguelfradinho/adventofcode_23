from enum import Enum
from typing import Self, TextIO

type Bid = int
type HandCards = list[int]
type Bet = tuple[HandCards, Bid]
type Hand = tuple[HandType, HandCards]


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

    @classmethod
    def calc_type(cls, hand: HandCards) -> Self:
        # we can be _really_ smart about it
        # There's definitely a generic way for len(hand) = x, but we're bound by the hand being size 5, so let's just assume that
        uniques = list(set(hand))
        n = len(uniques)
        first, last = uniques[0], uniques[-1]
        # edge cases, really cool
        if n == 1:
            return HandType.FiveKind
        elif n == 4:
            return HandType.Pair
        elif n == 5:
            return HandType.High
        # not so edgy
        elif n == 2:
            # In this case, the counts of first and last are either
            # four of a kind [4,1] or [1,4]
            # full house [2,3] or [2,3]
            # So, we could also multiply the counts instead of comparing to 4
            if hand.count(first) == 4 or hand.count(last) == 4:
                return HandType.FourKind
            return HandType.FullHouse
        # the 3 is the hardest because Three of a Kind and Two pair can shift, but we can still try our best
        elif n == 3:
            # here instead of comparing, it's literally just easier if we multiple so
            c_first = hand.count(first)
            c_last = hand.count(last)
            c_middle = hand.count(uniques[1])
            order_doesnt_matter = c_first * c_last * c_middle
            if order_doesnt_matter == 3:
                return HandType.ThreeKind
            elif order_doesnt_matter == 4:
                return HandType.TwoPair

        raise ValueError("Unimplemented, oops")

    def __str__(self) -> str:
        return self.name


# We could use Enum, but it'd be quite more verbose in terms of written code, so meh, if YAGNI...
symbol_cards = ["A", "K", "Q", "J", "T"]
symbol_values = [14, 13, 12, 11, 10]

name_to_card = {v: symbol_values[i] for i, v in enumerate(symbol_cards)}
card_to_name = {symbol_values[i]: v for i, v in enumerate(symbol_cards)}


def parse_input(line: str) -> tuple[list[int], Bid]:
    hand, bid = line.split(" ")
    bid = int(bid)
    hand = [int(i) if i.isnumeric() else name_to_card[i] for i in hand]
    return (hand, bid)


def hand_key(h: tuple[HandType, HandCards, Bid]) -> tuple[HandType, HandCards]:
    hand_type = h[0]
    cards = h[1]
    return (hand_type, cards)


def hand_as_string(h: HandCards) -> str:
    # Just helper method for debug
    return "".join([str(i) if i < 10 else card_to_name[i] for i in h])


def day_7(content: TextIO, is_example: bool = False) -> tuple[int, int]:
    hands_bids: list[Bet]
    with content as f:
        hands_bids = [parse_input(line) for line in f]

    hands_classified = [(HandType.calc_type(h), h, b) for h, b in hands_bids]

    # weakest hand gets rank 1, so
    hands_ranked = sorted(hands_classified, key=hand_key)

    winnings = []
    for i, (t, h, bid) in enumerate(hands_ranked):
        rank = i + 1
        print(rank, t, hand_as_string(h), bid)
        winnings.append(rank * bid)
    return sum(winnings), 0
