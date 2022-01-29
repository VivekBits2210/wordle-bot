import time
from copy import deepcopy
import random
from util.constants import MAX_WORD_LENGTH
from util.log_gen import get_logger
from util.wordutil import WordUtil

logger = get_logger(__file__)


class RandomCandidateStrategy:
    def __init__(self, game=None):
        self.game = game
        self.length_to_candidates_map = {}
        for length in range(2,MAX_WORD_LENGTH):
            self.length_to_candidates_map[length] = WordUtil().get_words_of_given_length(length)

        self.candidates = None
        self.confirmed_alphabets = set()
        self.confirmed_absent_alphabets = set()
        self.confirmed_alphabet_mapping = {}
        self.alphabet_to_candidate_mapping = {}
        self.alphabet_and_position_to_candidate_mapping = {}

        for candidate in self.candidates:
            for position in range(len(candidate)):
                alphabet = candidate[position]
                if (alphabet,position) in self.alphabet_and_position_to_candidate_mapping:
                    self.alphabet_and_position_to_candidate_mapping[(alphabet, position)].add(candidate)
                else:
                    self.alphabet_and_position_to_candidate_mapping[(alphabet, position)] = set([candidate])

                if alphabet in self.alphabet_to_candidate_mapping:
                    self.alphabet_to_candidate_mapping[alphabet].add(candidate)
                else:
                    self.alphabet_to_candidate_mapping[alphabet] = set([candidate])
        

    def set_game(self, game):
        self.game = game
        self.confirmed_alphabets = set()
        self.confirmed_absent_alphabets = set()
        self.confirmed_alphabet_mapping = {}
        self.alphabet_to_candidate_mapping = {}
        self.candidates = self.length_to_candidates_map[len(self.game.word)]

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
        new_candidates = set()
    
        for position in self.confirmed_alphabet_mapping:
            alphabet = self.confirmed_alphabet_mapping[position]
            self.alphabet_to_candidate_mapping
            
        for alphabet in self.alphabet_to_candidate_mapping:
            if alphabet not in self.confirmed_absent_alphabets:
                new_candidates.add(self.alphabet_to_candidate_mapping[alphabet])
            


        for candidate in self.candidates:
            discard = False
            for index in range(len(candidate)):
                alphabet = candidate[index]
                
                    discard = True
                    break

                

            if discard:
                new_candidates.remove(candidate)

        self.candidates = new_candidates

    def get_guess(self):
        print(self.game.word)
        print(self.game.word in self.candidates)
        print(len(self.candidates))
        self.parse_last_guess_and_clue()
        self.update_candidates()
        choice = random.choice(list(self.candidates))
        return choice
