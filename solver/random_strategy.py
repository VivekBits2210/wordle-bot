from util.wordutil import WordUtil
import random


class RandomStrategy:
    def __init__(self, wordle):
        self.wordle = wordle

    def get_guess(self):
        return random.choice(
            list(WordUtil().get_words_of_given_length(length=len(self.wordle.word)))
        )
