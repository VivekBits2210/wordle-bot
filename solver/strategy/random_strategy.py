from util.wordutil import WordUtil
import random


class RandomStrategy:
    def __init__(self, game=None):
        self.game = game

    def set_game(self, game):
        self.game = game

    def get_guess(self):
        return random.choice(
            list(WordUtil().get_words_of_given_length(length=len(self.game.word)))
        )
