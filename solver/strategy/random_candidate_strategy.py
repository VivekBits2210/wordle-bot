import time
from copy import deepcopy
import random
from util.log_gen import get_logger
from util.wordutil import WordUtil

logger = get_logger(__file__)


class RandomCandidateStrategy:
    def __init__(self, game=None):
        self.game = game
        # for candidate in self.candidates:
        #     for alphabet in candidate:

    def set_game(self, game):
        self.game = game
        self.candidates = WordUtil().get_words_of_given_length(
            length=self.game.word_length
        )
        self.confirmed_alphabets = set()
        self.confirmed_absent_alphabets = set()
        self.confirmed_alphabet_mapping = {}
        self.alphabet_to_candidate_mapping = (
            {}
        )  # TODO: Find ways to decrease candidate_update_time


    def parse_last_guess_and_clue(self):
        try:
            last_word = self.game.guess_history[-1]
            last_clue = self.game.clue_bits_history[-1]
            if self.game.guess_history[-1] in self.candidates:
                self.candidates.remove(self.game.guess_history[-1])
        except IndexError:  # Game has begun, nothing to parse
            return

        for position in last_clue:
            if last_clue[position] == 0:
                self.confirmed_absent_alphabets.add(last_word[position])
            if last_clue[position] >= 1:
                self.confirmed_alphabets.add(last_word[position])
            if last_clue[position] == 2:
                self.confirmed_alphabet_mapping[position] = last_word[position]

    def update_candidates(self):
        new_candidates = deepcopy(self.candidates)
        for candidate in self.candidates:
            discard = False
            for index in range(len(candidate)):
                alphabet = candidate[index]
                if alphabet in self.confirmed_absent_alphabets:
                    discard = True
                    break

                if index in self.confirmed_alphabet_mapping:
                    if alphabet != self.confirmed_alphabet_mapping[index]:
                        discard = True
                        break

            if discard:
                new_candidates.remove(candidate)

        self.candidates = new_candidates

    def get_guess(self):
        self.parse_last_guess_and_clue()
        self.update_candidates()
        choice = random.choice(list(self.candidates))
        return choice
