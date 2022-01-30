import time
import random
import copy
from concurrent.futures import ThreadPoolExecutor
from solver.solver import Solver
from util.wordutil import WordUtil
from game.wordle import Wordle
from util.log_gen import get_logger
from util.constants import NUM_THREADS
counter = 0
logger = get_logger(__file__)


class Profiler:
    def __init__(
        self,
        strategy,
        guess_range=range(6, 7),
        length_range=range(5, 6)
    ):
        self.strategy = strategy
        self.guess_range = guess_range
        self.length_range = length_range
        self.length_to_word_map = {}
        wu = WordUtil()
        for length in self.length_range:
            self.length_to_word_map[length] = wu.get_words_of_given_length(length =length)

        #Construct maps
        self.profile = {}
        self.game_tuple_to_config_tuple_map = {}
        for length in self.length_range:
            words = self.length_to_word_map[length]
            for guesses in self.guess_range:
                game_tuple = (length, guesses)
                self.profile[game_tuple] = 0.0
                self.game_tuple_to_config_tuple_map[game_tuple] = []
                for chunk in self.chunks(words,int(len(words)/NUM_THREADS)):  
                    config_tuple = (guesses, chunk) 
                    self.game_tuple_to_config_tuple_map[game_tuple].append(config_tuple)

    def generate_profile(self):
        for game_tuple in self.profile:
            length = game_tuple[0]
            guesses = game_tuple[1]
            print(f"Profiling Length: {length}, Guesses: {guesses}")
            words = self.get_scrambled_words(self.length_to_word_map[length])
            win_counter = 0
            total_counter = 0
            total_attempts = 0
            start = time.process_time()
            for word in words:
                game = Wordle(word, guesses, subdue=True)
                is_win = self.profile_game(game)
                win_counter = (
                    win_counter + 1 if is_win else win_counter
                )
                total_counter += 1
                total_attempts += len(game.guess_history)
                if total_counter%20==0:
                    print(f'Total={total_counter}:\tFailed: {total_counter - win_counter}\tAccuracy:{(win_counter/total_counter)*100:.02f}%\tAvg Attempts: {total_attempts/total_counter:.02f}\tAvg Time: {(time.process_time() - start)/total_counter:.03f}s')
            print(f"WIN COUNTER: {win_counter}")


    def generate_profile_threaded(self):        
        print(f"{len(self.profile)}")    
        for game_tuple in self.profile:
            print(f"Profiling Length: {game_tuple[0]}, Guesses: {game_tuple[1]}")
            config_tuple_list = self.game_tuple_to_config_tuple_map[game_tuple]
            print(len(config_tuple_list))
            with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                results = executor.map(self.profile_word_set,config_tuple_list)
            num_words = len(self.length_to_word_map[game_tuple[0]])
            self.profile[game_tuple] = round(100*(sum(list(results))/num_words),2)
            print(f"Win Percentage: {self.profile[game_tuple]} %")

        return self.profile

    def profile_word_set(self,config_tuple):
        global counter
        counter = counter + 1
        print(f"Entered Profile word set : {counter}")
        guesses = config_tuple[0]
        words = config_tuple[1]
        win_counter = 0
        for word in words:
            game = Wordle(word, guesses, subdue=True)
            is_win = self.profile_game(game)
            win_counter = (
                win_counter + 1 if is_win else win_counter
            )
        print(f"WIN COUNTER: {win_counter}")
        return win_counter

    def profile_game(self, game):
        self.solver = Solver(None, self.strategy, subdue=True)
        self.solver.set_game(game)
        self.solver.solve()
        return game.has_won()
        
    def chunks(self, words, n):
        words = list(words)
        return [copy.deepcopy(words[i:i + n]) for i in range(0, len(words), n)]

    def get_scrambled_words(self, words):
        words = list(words)
        random.shuffle(words)
        words = set(words)
        return words

