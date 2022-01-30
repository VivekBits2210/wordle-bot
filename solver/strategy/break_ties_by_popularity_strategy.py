import random
from util.wordutil import WordUtil
from .random_candidate_strategy import RandomCandidateStrategy


class BreakTiesByPopularityStrategy:
    def __init__(self, game=None):
        self.game = game
        self.rcs = RandomCandidateStrategy()

    def set_game(self, game):
        self.game = game
        self.rcs.set_game(game)

    def get_score(self, candidate):
        return WordUtil().get_word_frequency(word=candidate)

    def get_max_score_candidate(self):
        max_score = -1
        max_score_candidate_list = []
        for candidate in self.rcs.candidates:
            current_score = self.get_score(candidate)
            if current_score > max_score:
                max_score = current_score
                max_score_candidate_list.append(candidate)
        return random.choice(max_score_candidate_list)

    def get_guess(self):
        self.rcs.parse_last_guess_and_clue()
        self.rcs.update_candidates()
        return self.get_max_score_candidate()
