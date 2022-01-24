from log_gen import get_logger
logger = get_logger(__file__)

class Solver:
    def __init__(self, word, length, guesses, slow, difficulty, debug):
        self.word = word
        self.length = length
        self.guesses = guesses
        self.slow = slow
        self.difficulty = difficulty
        self.debug = debug
    
    def solve(self):
        logger.info("Solving for word: {}".format(self.word))