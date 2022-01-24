from util.log_gen import get_logger
from solver.random_strategy import RandomStrategy

logger = get_logger(__file__)


class Solver:
    def __init__(self, slow, wordle):
        self.slow = slow
        self.wordle = wordle

    def solve(self):
        while True:
            guess = RandomStrategy(self.wordle).get_guess()
            clues = self.wordle.get_clue_bits(guess)
            if clues is None:
                break
            self.wordle.pretty_print_guess()
            if self.slow:
                print("On slow mode, waiting for input: ", end="")
                input()
