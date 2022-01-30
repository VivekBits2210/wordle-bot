from util.constants import MAX_WORD_LENGTH
from util.wordutil import WordUtil
import random


class RandomStrategy:
    def __init__(self, game=None):
        self.game = game
        self.length_to_candidates_map = {}
        for length in range(2,MAX_WORD_LENGTH):
            self.length_to_candidates_map[length] = WordUtil().get_words_of_given_length(length)

    def set_game(self, game):
        self.game = game
        self.set_game(self.game)

    def get_guess(self):
        return random.choice(
            list(self.length_to_candidates_map[len(self.game.word)])
        )
