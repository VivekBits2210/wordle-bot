from solver.strategy.five_hit_strategy import FiveHitStrategy
from util.wordutil import WordUtil


class FiveHitWithPopularWordTieBreakStrategy:
    def __init__(self, game=None):
        self.game = game
        self.fhs = FiveHitStrategy(self.game)

    def set_game(self,game):
        self.game = game

    def get_guess(self):
        return self.fhs.get_guess(
            scoring_function=lambda word: WordUtil().get_word_frequency(word=word)
        )
