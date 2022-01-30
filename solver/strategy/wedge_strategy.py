import random
import string
from solver.strategy.deedy_strategy import DeedyStrategy
from solver.strategy.random_candidate_strategy import RandomCandidateStrategy
from util.constants import WORDS
from util.wordutil import WordUtil


class WedgeStrategy:
    def __init__(self, game=None):
        self.game = game
        self.rcs = RandomCandidateStrategy(self.game)
        self.ds = DeedyStrategy(self.game)

    def set_game(self, game):
        self.game = game
        self.rcs.set_game(self.game)
        self.ds.set_game(self.game)

    def find_wedge(self):
        if len(self.rcs.candidates) <= 4:
            return random.choice(list(self.rcs.candidates))
        good_letters = set(self.rcs.confirmed_alphabet_mapping.keys()).union(self.rcs.confirmed_alphabets)
        alphabet_to_frequency_map = {}
        for candidate in self.rcs.candidates:
            for alphabet in candidate:
                if alphabet not in alphabet_to_frequency_map:
                    alphabet_to_frequency_map[alphabet] = 1
                else:
                    alphabet_to_frequency_map[alphabet] += 1
        
        # Pick 6 wedge letters
        num_wedges_threshold = 8
        polarizer_function = lambda dict_item: abs(dict_item[1]/len(self.rcs.candidates) - 0.5)
        wedge_alphabet_list = [item[0] for item in sorted(alphabet_to_frequency_map.items(), key=polarizer_function)][:num_wedges_threshold]

        # Find words with most number of wedge letters
        best_choice_frequency = 0
        rarity_to_words_map = {}
        for word in WordUtil().get_words_of_given_length(self.game.word_length):
            rarity_frequency = 0
            alphabet_seen_before = set()
            for alphabet in word:
                if alphabet in alphabet_seen_before:
                    continue
                alphabet_seen_before.add(alphabet)

            for alphabet in wedge_alphabet_list:
                if alphabet in word:
                    if alphabet in good_letters:
                        rarity_frequency+=1
                    else:
                        rarity_frequency+=2
                
            if rarity_frequency not in rarity_to_words_map:
                rarity_to_words_map[rarity_frequency] = [word]
            else:
                rarity_to_words_map[rarity_frequency].append(word)

            if rarity_frequency > best_choice_frequency:
                best_choice_frequency = rarity_frequency
            
        # Pick any word from the list of words that have the largest bounty of rare letters
        return random.choice(rarity_to_words_map[best_choice_frequency])

    def get_guess(self):
        self.rcs.parse_last_guess_and_clue()
        self.rcs.update_candidates()

        # Phase 1 & 3: Deedy strategy (moves 1-3)
        if len(self.game.guess_history) >= 5:
            return self.ds.get_guess()

        # Phase 2: Wedge strategy (moves 4 and 5)
        else:
            self.ds.set_rcs(self.rcs)
            return self.find_wedge()
