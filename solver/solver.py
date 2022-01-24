from util.log_gen import get_logger
from solver.random_strategy import RandomStrategy

logger = get_logger(__file__)

class Solver:
    def __init__(self, length, guesses, slow, wordle):
        self.length = length
        self.guesses = guesses
        self.slow = slow
        self.wordle = wordle
        self.clue_history = []

    def solve(self):
        while(True):
            guess = RandomStrategy(self.length).get_guess()
            clues = self.wordle.get_clue_bits(guess)
            if clues is None:
                break
            self.clue_history.append(clues)
            self.wordle.pretty_print_guess()
            if self.slow:
                print("On slow mode, waiting for input: ",end='')
                input()
            