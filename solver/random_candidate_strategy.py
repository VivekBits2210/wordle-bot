from util.wordutil import WordUtil
import random


class RandomCandidateStrategy:
    def __init__(self, wordle):
        self.wordle = wordle
        self.candidates = WordUtil().get_words_of_given_length(
            length=len(self.wordle.word)
        )
        self.confirmed_alphabets = set()
        self.confirmed_alphabet_mapping = {}

    def parse_last_guess_and_clue(self):
        last_word = self.wordle.guess_history[-1]
        last_clue = self.wordle.clue_bits_history
        for position in last_clue:
            if last_clue[position] >= 1:
                self.confirmed_alphabets.add(last_word[position])
            if last_clue[position] == 2:
                self.confirmed_alphabet_mapping[position] = last_word[position]

    def get_candidates(self):
        self.parse_last_guess_and_clue()

    """
    [w1,w2,...]
    [{},{},...]
    candidates = {WORDS_right_length} (global set)
    for <word> in candidates:
        for k in range(alpha_present):
            if alpha_present[k] not in word:
                candidates.remove(<word>)
        for i in range(std_length):
            if word[i]!=ans[i]:
                candidates.remove(<word>)
    """

    def get_guess(self):
        return random.choice(
            list(WordUtil().get_words_of_given_length(length=self.length))
        )
