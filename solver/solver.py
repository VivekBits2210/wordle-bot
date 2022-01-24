'''
ALGO
- Find all candidates that fit the criteria.
- Amongst the valid candidates, compute a distribution of letters at each position.
- Find a guessable word from all valid guesses which optimizes sum(P(letter at pos i)) + 0.5 * sum(P letter not at pos i) amongst the candidate set. Break ties effectively.
- Repeat until there is only 1 candidate possible and guess it.
'''

from util.log_gen import get_logger
logger = get_logger(__file__)

class Solver:
    def __init__(self, word, guesses):
        self.word = word
        self.guesses = guesses
    
    def solve(self):
        logger.info("Solving for word: {}".format(self.word))

