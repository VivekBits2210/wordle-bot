from solver.strategy.five_hit_strategy import FiveHitStrategy
from util.wordutil import WordUtil


class FiveHitWithPopularWordTieBreakStrategy:
    def __init__(self, wordle):
        self.wordle = wordle
        self.fhs = FiveHitStrategy(self.wordle)

    def get_guess(self):
        return self.fhs.get_guess(
            scoring_function=lambda word: WordUtil().get_word_frequency(word=word)
        )
