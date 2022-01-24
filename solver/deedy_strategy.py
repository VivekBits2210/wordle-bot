'''
ALGO
- Find all candidates that fit the criteria.
- Amongst the valid candidates, compute a distribution of letters at each position.
- Find a guessable word from all valid guesses which optimizes sum(P(letter at pos i)) + 0.5 * sum(P letter not at pos i) amongst the candidate set. Break ties effectively.
- Repeat until there is only 1 candidate possible and guess it.
'''
from util.wordutil import WordUtil
import random
class RandomStrategy:
    def __init__(self,length):
        self.length = length

    def get_guess(self):
        return random.choice(list(WordUtil().get_words_of_given_length(length=self.length)))