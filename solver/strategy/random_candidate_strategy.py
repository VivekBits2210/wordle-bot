from copy import deepcopy
import random
from util.wordutil import WordUtil


class RandomCandidateStrategy:
    def __init__(self, wordle):
        self.wordle = wordle
        self.candidates = WordUtil().get_words_of_given_length(
            length=len(self.wordle.word)
        )
        self.confirmed_alphabets = set()
        self.confirmed_alphabet_mapping = {}

    def parse_last_guess_and_clue(self):
        try:
            last_word = self.wordle.guess_history[-1]
            last_clue = self.wordle.clue_bits_history[-1]
            self.candidates.remove(self.wordle.guess_history[-1])
        except IndexError:  # Game has begun, nothing to parse
            return

        for position in last_clue:
            if last_clue[position] >= 1:
                self.confirmed_alphabets.add(last_word[position])
            if last_clue[position] == 2:
                self.confirmed_alphabet_mapping[position] = last_word[position]

    def update_candidates(self):
        self.parse_last_guess_and_clue()
        new_candidates = deepcopy(self.candidates)
        for candidate in self.candidates:
            continue_in_outer_loop = False
            for alphabet in self.confirmed_alphabets:
                if alphabet not in candidate:
                    new_candidates.remove(candidate)
                    continue_in_outer_loop = True
                    break

            if continue_in_outer_loop:
                continue

            for position in self.confirmed_alphabet_mapping:
                if candidate[position] != self.confirmed_alphabet_mapping[position]:
                    new_candidates.remove(candidate)
                    break
        self.candidates = new_candidates

    def get_guess(self):
        self.update_candidates()
        return random.choice(list(self.candidates))
