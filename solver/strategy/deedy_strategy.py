"""
ALGO
- Find all candidates that fit the criteria.
- Amongst the valid candidates, compute a distribution of letters at each position.
- Find a guessable word from all valid guesses which optimizes sum(P(letter at pos i)) + 0.5 * sum(P letter not at pos i) amongst the candidate set. Break ties effectively.
- Repeat until there is only 1 candidate possible and guess it.
"""
from collections import defaultdict
import random
import string
from util.constants import EXPLORATION_WEIGHT
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
        self.pos_to_dist_map = {}
        for pos in range(self.game.word_length):
            self.pos_to_dist_map[pos] = {}

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


    def calculate_exploration_benefit_of_alphabets(self):
        self.alphabet_to_exploration_benefit_map = {}
        for candidate in self.rcs.candidates:
            for alphabet in string.ascii_lowercase:
                if alphabet in candidate:
                    if alphabet not in self.alphabet_to_exploration_benefit_map:
                        self.alphabet_to_exploration_benefit_map[alphabet] = 1
                    else:
                        self.alphabet_to_exploration_benefit_map[alphabet] += 1

        MULTIPLIER = 100
        for alphabet in self.alphabet_to_exploration_benefit_map:
            self.alphabet_to_exploration_benefit_map[alphabet] = (MULTIPLIER*self.alphabet_to_exploration_benefit_map[alphabet])/len(self.rcs.candidates)
            if self.alphabet_to_exploration_benefit_map[alphabet]>int(MULTIPLIER/2):
                self.alphabet_to_exploration_benefit_map[alphabet]-= int(MULTIPLIER/2)

        #     # self.alphabet_to_exploration_benefit_map[alphabet] = 100*(1 - abs(self.alphabet_to_exploration_benefit_map[alphabet] - 0.5))

    def get_max_score_candidate(self):
        self.calculate_frequency_distribution_per_position()
        self.calculate_exploration_benefit_of_alphabets()
        max_score = -1
        max_score_candidate = None
        for candidate in self.rcs.candidates:
            current_score = self.get_score(candidate)
            if current_score > max_score:
                max_score = current_score
                max_score_candidate = candidate
        return max_score_candidate

    def get_score(self, candidate):
        global EXPLORATION_WEIGHT
        if self.game.num_guesses/self.game.total_guesses > 0.7:
            EXPLORATION_WEIGHT /= 10
        score = 0.0
        alphabets_accounted_for = set()
        for position in range(len(candidate)):
            alphabet = candidate[position]
            exploitation_score =  self.pos_to_dist_map[position][candidate[position]]
            if alphabet not in alphabets_accounted_for:
                exploration_score = self.alphabet_to_exploration_benefit_map[alphabet]  
                score = score + exploitation_score + exploration_score*EXPLORATION_WEIGHT
            alphabets_accounted_for.add(alphabet)
            # print(f"SCORES - {exploitation_score} {exploration_score}")
        return score

    def get_guess(self):
        self.rcs.parse_last_guess_and_clue()
        self.rcs.update_candidates()
        return self.get_max_score_candidate()

# Deedy's code

# DEFAULT_N = 5
# DEFAULT_MAX_GUESSES = 6
# # Game settings
# DEFAULT_GAME_CONFIG = {
#     'max_guesses': str(DEFAULT_MAX_GUESSES)
# }
# NON_POS_WEIGHT = 0.5
# DEFAULT_SOLVER_SETTINGS = {
# 	# This now on by default. The setting was retired becuse it's inefficient and adding tech debt.
# 	# Not needed to implement unless we want to test for this specifically
# 	# 'use_conditional': True,
# 	# "HARD mode" - every subsequent guess must be in the candidate set
# 	'non_strict': True,
# 	# Use positional character distribution instead of global character distribution amongst the 
# 	# remaining word candidates.
# 	'use_pos': True,
# 	'max_guesses': str(DEFAULT_MAX_GUESSES)
# }

# # tile
# NOTHING = 0
# GUESS_WRONG_SPOT = 1
# GUESS_RIGHT_SPOT = 2
# # Code from deedy repo, wtf is going on here?
# def guess_next_word(
# 	word_set,
# 	clues,
# 	solver_settings=DEFAULT_SOLVER_SETTINGS,
# 	debug=1
# ):

#     N = get_n_from_word_set(word_set) # gets the length
#     MAX_GUESSES = int(solver_settings['max_guesses']) # gets max guesses
#     word_right_place, in_word_wrong_place, not_in_word = parse_clues(clues, debug=debug) # gets past clues
#     prev_guesses = set([w for w, _ in clues]) # gets past guesses
#     if len(clues) and clues[-1][1] == [GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT, GUESS_RIGHT_SPOT]: # if last guess was correct
#         return None, [], 0

#     cands = [w for w in word_set \
#             if not w in prev_guesses and is_guessable_word(w, word_right_place, in_word_wrong_place, not_in_word)]
#     # filter candidates

#     guess_left = MAX_GUESSES - len(clues)
#     if len(cands) == 1 or guess_left == 1:  #if there's 1 or we're fucked, go yolo
#         return cands[0], cands, len(cands)

#     new_musts = [set() for x in range(N)]
#     for ix in range(N):
#         for c in cands:
#             new_musts[ix].add(c[ix])
#     for ix, cond in enumerate(new_musts): 
#         if len(cond) == 1:
#             letter = list(cond)[0]
#             word_right_place[letter].add(ix)
#     places_known = set([x for setx in word_right_place.values() for x in setx])
#     unknown_places = set([ix for ix in range(N) if not ix in places_known])

#     # Assemble character frequencies of remaining candidates
#     conditional_unknown_freq = defaultdict(int)
#     conditional_pos_freq = [defaultdict(int) for i in range(N)]
#     total_unknown_freq = 0
#     for c in cands:
#         for i, l in enumerate(c):
#             if not i in unknown_places:
#                 continue
#             if l in not_in_word: # and not i in word_right_place[l]:# and not l in in_word_wrong_place:
#                 continue
#             conditional_unknown_freq[l] += 1
#             conditional_pos_freq[i][l] += 1
#             total_unknown_freq += 1

#     if not solver_settings['use_pos']:
#         def sort_maximal_nonpos(word):
#             # Sort by the number of times a character in a word appears
#             # globally in any unknown place in the remaining candidate set
#             return -sum([conditional_unknown_freq[c] for c in set(word)])
#         sortfn = sort_maximal_nonpos
#     else:
#         def sort_maximal_position_with_nonpos(word, sort=True):
#             # Sort by the number of times a character in a word appears
#             # in the right position of any unknown place in the word and weigh
#             # it with appearances in the wrong place by NON_POS_WEIGHT
#             score = [0]*26
#             nonpos_score = [0]*26
#             for i, c in enumerate(word):
#                 # += does well also but performs worse for duplicate letters
#                 score[ord(c)-ord('a')] = conditional_pos_freq[i][c]
#                 nonpos_score[ord(c)-ord('a')] = conditional_unknown_freq[c] - conditional_pos_freq[i][c]
#             sortscore = -(sum(score) + NON_POS_WEIGHT * sum(nonpos_score))
#             if sort:
#                 return sortscore
#             return ([(chr(i + ord('a')), v) for i, v in enumerate(score) if v],
#                     [(chr(i+ ord('a')), v) for i, v in enumerate(nonpos_score) if v], sortscore)
#         sortfn = sort_maximal_position_with_nonpos

#     explorable = word_set if solver_settings['non_strict'] else cands
#     explore_cands = sorted(explorable, key=sortfn)
#     max_val = sortfn(explore_cands[0])
#     explore_cands = [x for x in explore_cands if sortfn(x) == max_val]

#     if len(explore_cands) > 0:
#         # Break ties by boosting words with known letter guesses because
#         # they can appear in the word again and need to be explicitly checked for
#         # because simply guessing them in the wrong place will always return 🟨 
#         # because it exists in the word twice
#         def boost_letters_in_right_place(word):
#             score = 0
#             for i, c in enumerate(word):
#                 if c in new_musts[i] and len(new_musts[i]) > 1:
#                     if c in word_right_place:
#                         score += 1
#             return -score
#         explore_cands = sorted(explore_cands, key=boost_letters_in_right_place)
#         max_val2 = boost_letters_in_right_place(explore_cands[0])
#         explore_cands = [x for x in explore_cands if boost_letters_in_right_place(x) == max_val2]

#     if debug >= 2:
#         print('Inferred conditions ', [''.join(m) for m in new_musts])
#         cond_probs = [(x, y) for x, y in conditional_unknown_freq.items() if y]
#         print(f'Conditional ({len(cond_probs)}):{cond_probs}\nCands ({len(cands)}): {cands[:100]}...\n')
#         print(f'Explore cands ({len(explore_cands)}): {[(c, sortfn(c), boost_letters_in_right_place(c)) for c in explore_cands[:10]]}')

#     chosen_cs = [cand for cand in explore_cands if cand not in prev_guesses]
#     chosen = chosen_cs[0]	
#     return chosen, cands[:5], len(cands)
        
