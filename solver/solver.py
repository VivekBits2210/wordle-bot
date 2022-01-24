from util.log_gen import get_logger
from solver.random_strategy import RandomStrategy
from solver.random_candidate_strategy import RandomCandidateStrategy

logger = get_logger(__file__)


class Solver:
    def __init__(self, slow, wordle):
        self.slow = slow
        self.wordle = wordle

    def solve(self):
        while True:
            guess = RandomCandidateStrategy(self.wordle).get_guess()
            clues = self.wordle.play(guess)
            self.wordle.pretty_print_game_output()
            if self.wordle.is_game_complete():
                break
            else:
                if self.slow:
                    print("On slow mode, waiting for input: ", end="")
                    input()
