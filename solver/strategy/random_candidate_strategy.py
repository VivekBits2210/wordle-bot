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
        self.length_to_alphabet_to_candidate_mapping = {}
        self.length_to_alphabet_and_position_to_candidate_mapping = {}
        
        for length in range(2,MAX_WORD_LENGTH):
            self.length_to_alphabet_to_candidate_mapping[length] = {}
            self.length_to_alphabet_and_position_to_candidate_mapping[length] = {}
            for candidate in self.length_to_candidates_map[length]:
                for position in range(len(candidate)):
                    alphabet = candidate[position]
                    if (alphabet,position) in self.length_to_alphabet_and_position_to_candidate_mapping[length]:
                        self.length_to_alphabet_and_position_to_candidate_mapping[length][(alphabet, position)].add(candidate)
                    else:
                        self.length_to_alphabet_and_position_to_candidate_mapping[length][(alphabet, position)] = set([candidate])

                    if alphabet in self.length_to_alphabet_to_candidate_mapping:
                        self.length_to_alphabet_to_candidate_mapping[length][alphabet].add(candidate)
                    else:
                        self.length_to_alphabet_to_candidate_mapping[length][alphabet] = set([candidate])
            

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
        new_candidates = deepcopy(self.candidates)
    
        for position in self.confirmed_alphabet_mapping:
            alphabet = self.confirmed_alphabet_mapping[position]
            new_candidates = new_candidates.intersection(self.length_to_alphabet_and_position_to_candidate_mapping[len(self.game.word)][(alphabet,position)])
            
        for alphabet in self.alphabet_to_candidate_mapping:
            if alphabet in self.confirmed_alphabets:
                new_candidates = new_candidates.intersection(self.length_to_alphabet_to_candidate_mapping[len(self.game.word)][alphabet])

        self.candidates = new_candidates

    def get_guess(self): 
        self.parse_last_guess_and_clue()
        self.update_candidates()
        choice = random.choice(list(self.candidates))
        return choice
