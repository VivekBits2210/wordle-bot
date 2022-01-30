"""
ALGO
- Find all candidates that fit the criteria.
- Amongst the valid candidates, compute a distribution of letters at each position.
- Find a guessable word from all valid guesses which optimizes sum(P(letter at pos i)) + 0.5 * sum(P letter not at pos i) amongst the candidate set. Break ties effectively.
- Repeat until there is only 1 candidate possible and guess it.
"""
import random
from util.wordutil import WordUtil
from .random_candidate_strategy import RandomCandidateStrategy


class DeedyStrategy:
    def __init__(self, game=None):
        self.game = game
        self.rcs = RandomCandidateStrategy()
        self.pos_to_dist_map = {}


    def set_game(self,game):
        self.game = game
        self.rcs.set_game(self.game)
        for pos in range(len(self.game.word_length)):
            self.pos_to_dist_map[pos] = {}

    def get_score(self, candidate):
        score = 0.0
        for pos in range(len(candidate)):
            score += self.pos_to_dist_map[pos][candidate[pos]]
        return score

    def calculate_frequency_distribution_per_position(self):
        for candidate in self.rcs.candidates:
            for pos in range(len(candidate)):
                char = candidate[pos]
                if char not in self.pos_to_dist_map[pos]:
                    self.pos_to_dist_map[pos][char] = 1
                else:
                    self.pos_to_dist_map[pos][char] += 1

        temp_pos_to_dict_map = {}
        for pos in self.pos_to_dist_map:
            distr_map = self.pos_to_dist_map[pos]
            denom = sum(distr_map.values())
            temp_distr_map = {}
            for char in distr_map:
                temp_distr_map[char] = 100 * (float(distr_map[char]) / float(denom))
            distr_map = temp_distr_map
            temp_pos_to_dict_map[pos] = distr_map
        self.pos_to_dist_map = temp_pos_to_dict_map

    def get_max_score_candidate(self):
        self.calculate_frequency_distribution_per_position()
        max_score = -1
        max_score_candidate = None
        for candidate in self.rcs.candidates:
            current_score = self.get_score(candidate)
            if current_score > max_score:
                max_score = current_score
                max_score_candidate = candidate
        return max_score_candidate

    def get_guess(self):
        self.rcs.parse_last_guess_and_clue()
        self.rcs.update_candidates()
        return self.get_max_score_candidate()
