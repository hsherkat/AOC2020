"""
Advent of Code 2020: Day 22
https://adventofcode.com/2020/day/22
"""

from collections import deque
from itertools import count
from typing import Tuple, List, Iterable, Optional


class Game:
    def __init__(self, deck1: Iterable, deck2: Iterable):
        self.deck1 = deque(deck1)
        self.deck2 = deque(deck2)

    def play_round(self) -> Optional[Tuple[int, int]]:
        """Return cards played in round. If game ends this round, return None."""
        if not (self.deck1 and self.deck2):
            return None
        card1, card2 = self.deck1.popleft(), self.deck2.popleft()
        if card1 > card2:
            self.deck1.extend([card1, card2])
        else:
            self.deck2.extend([card2, card1])
        return (card1, card2)

    def play_game(self):
        """Play until one deck exhausted, return the other."""
        while self.play_round():
            pass
        return self.deck1 or self.deck2

    @staticmethod
    def from_str(s: str) -> "Game":
        p1, p2 = s.strip().split("\n\n")
        deck1 = [int(n.strip()) for n in p1.split("\n")[1:]]
        deck2 = [int(n.strip()) for n in p2.split("\n")[1:]]
        return Game(deck1, deck2)

    def winners_score(self) -> int:
        if self.deck1 and self.deck2:
            deck = self.play_game()
        else:
            deck = self.deck1 or self.deck2
        return sum(i * card for i, card in zip(count(1), reversed(deck)))


###


class GameRecursive:
    def __init__(self, deck1, deck2):
        self.deck1 = deque(deck1)
        self.deck2 = deque(deck2)
        self.winner = None
        self.past_decks = set()

    def pre_check(self) -> bool:
        """Is game over because of repeating previous state? Set winner.
        Update record of previous states.
        """
        record1 = ("1",) + tuple(self.deck1)
        record2 = ("2",) + tuple(self.deck2)
        if record1 + record2 in self.past_decks:
            self.winner = 1
            return True
        else:
            self.past_decks.add(record1 + record2)
            return False

    def post_check(self) -> bool:
        """Did the game end because of empty deck? Set winner."""
        if not (self.deck1 and self.deck2):
            self.winner = 1 if self.deck1 else 2
            return True
        return False

    def play_round(self) -> Optional[int]:
        if self.pre_check():
            return None

        card1, card2 = self.deck1.popleft(), self.deck2.popleft()
        if card1 <= len(self.deck1) and card2 <= len(self.deck2):
            sub_game = GameRecursive(list(self.deck1)[:card1], list(self.deck2)[:card2])
            round_winner = sub_game.play_game()
        else:
            round_winner = 1 if card1 > card2 else 2
        if round_winner == 1:
            self.deck1.extend([card1, card2])
        else:
            self.deck2.extend([card2, card1])

        if self.post_check():
            return None
        return round_winner

    def play_game(self) -> int:
        """Play until someone wins, set winner if not set already, and return winner."""
        while not self.winner:
            self.play_round()
        return self.winner

    def winners_score(self) -> int:
        if not self.winner:
            self.play_game()
        deck = self.deck1 if self.winner == 1 else self.deck2
        return sum(i * card for i, card in zip(count(1), reversed(deck)))

    @staticmethod
    def from_str(s: str) -> "GameRecursive":
        p1, p2 = s.strip().split("\n\n")
        deck1 = [int(n.strip()) for n in p1.split("\n")[1:]]
        deck2 = [int(n.strip()) for n in p2.split("\n")[1:]]
        return GameRecursive(deck1, deck2)


#####################


with open("input_22.txt") as f:
    raw_input = f.read()


if __name__ == "__main__":
    game = Game.from_str(raw_input)
    print(game.winners_score())
    game2 = GameRecursive.from_str(raw_input)
    print(game2.winners_score())
