from ast import Continue
from importlib.machinery import WindowsRegistryFinder
import time
import random
from webbrowser import get
from solver.solver import Solver
from util.wordutil import WordUtil
from game.wordle import Wordle
from util.log_gen import get_logger

logger = get_logger(__file__)


class Profiler:
    def __init__(
        self,
        strategy,
        guess_range=range(4, 8),
        length_range=range(6,7),
        difficulty_range=range(1, 9),
    ):
        self.strategy = strategy
        self.solver = Solver(None, self.strategy, subdue=True)
        self.guess_range = guess_range
        self.length_range = length_range
        self.difficulty_range = difficulty_range

    def get_profile(self):
        wu = WordUtil()
        profile = {}
        for length in self.length_range:
            for difficulty in self.difficulty_range:
                words = wu.get_words_of_given_difficulty(
                    difficulty=difficulty, length =length
                )
                if len(words) == 0:
                    continue
                for guesses in self.guess_range:
                    game_tuple = (length, difficulty, guesses)
                    profile[game_tuple] = 0.0
                    win_counter = 0
                    print(
                        f"Length: {length}, Difficulty: {difficulty}, Guesses: {guesses}, Number of Words: {len(words)}, ",
                        end=''
                    )
                    
                    for word in words:
                        game = Wordle(word, guesses, subdue=True)
                        is_win = self.profile_game(game)
                        win_counter = (
                            win_counter + 1 if is_win else win_counter
                        )

                    profile[game_tuple] = 100 * (win_counter / len(words))
                    profile[game_tuple] = round(profile[game_tuple],2)
                    print(f"Win Percentage: {profile[game_tuple]} %")

        return profile

    def profile_game(self, game):
        self.solver.set_game(game)
        self.solver.solve()
        return game.has_won()
