import numpy as np
from solver.strategy.random_candidate_strategy import RandomCandidateStrategy


class ThreeHitStrategy:
    def __init__(self, game=None):
        self.game = game
        self.rcs = RandomCandidateStrategy(self.game)
        self.three_hit_candidates = {
            0: "lunch",
            1: "metro",
            2: "daisy",
        }

    def set_game(self, game):
        self.game = game
        self.rcs.set_game(self.game)

    def get_guess(self, *, scoring_function=lambda word: 1):
        self.rcs.parse_last_guess_and_clue()
        self.rcs.update_candidates()

        # If we have more than 5 guesses, a 5 letter word and haven't used up all our hit words, we can try a hit word
        if (
            self.game.total_guesses >= 6
            and self.game.word_length == 5
            and len(self.game.guess_history) in self.three_hit_candidates
        ):
            return self.three_hit_candidates[len(self.game.guess_history)]

        candidate_list = list(self.rcs.candidates)
        candidate = candidate_list[
            np.argmax([scoring_function(candidate) for candidate in candidate_list])
        ]
        return candidate
