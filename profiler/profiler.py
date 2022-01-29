import time
import random
from webbrowser import get
from solver.solver import Solver
from util.wordutil import WordUtil
from game.wordle import Wordle
from util.log_gen import get_logger
logger = get_logger(__file__)

class Profiler:
    def __init__(self, strategy, guess_range=range(5,8), length_range=range(4,10), difficulty_range=(1,9)):
        self.strategy = strategy
        self.guess_range = guess_range
        self.length_range = length_range
        self.difficulty_range = difficulty_range
    
    def get_profile(self):
        wu = WordUtil()
        profile = {}
        for length in self.length_range:
            words = wu.get_words_of_given_length(length=length)
            for difficulty in self.difficulty_range:
                words= wu.get_words_of_given_difficulty(word_subset=words, difficulty=difficulty)
                for guesses in self.guess_range:          
                    game_tuple = (length,difficulty,guesses)
                    profile[game_tuple] = 0.0
                    win_counter = 0
                    sampled_words = random.sample(list(words),100)
                    print("Length: {}, Difficulty: {}, Guesses: {}, Number of Words: {} ".format(length, difficulty, guesses, len(words)))
                    for word in sampled_words:
                        game = Wordle(word,guesses,subdue=True)
                        win_counter = win_counter+1 if self.profile_game(game) else win_counter
                            
                    profile[game_tuple] = 100*(win_counter/len(sampled_words))
                    print(f"WIN PERCENTAGE: {profile[game_tuple]}")

        return profile


    def profile_game(self, game):
        self.solver = Solver(game, self.strategy, subdue=True)
        self.solver.solve()
        return game.has_won()
        

                    
                     
