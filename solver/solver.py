'''
ALGO
- Find all candidates that fit the criteria.
- Amongst the valid candidates, compute a distribution of letters at each position.
- Find a guessable word from all valid guesses which optimizes sum(P(letter at pos i)) + 0.5 * sum(P letter not at pos i) amongst the candidate set. Break ties effectively.
- Repeat until there is only 1 candidate possible and guess it.
'''
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
            