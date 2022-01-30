import time
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
        length_range=range(6, 7)
    ):
        self.strategy = strategy
        self.solver = Solver(None, self.strategy, subdue=True) #Subdue is set to True to stop the game from printing stuff while profiling
        self.guess_range = guess_range
        self.length_range = length_range

    def get_profile(self):
        wu = WordUtil()
        profile = {}
        for length in self.length_range:
            t1 = time.process_time()
            words = wu.get_words_of_given_length(length =length)
            if len(words) == 0:
                continue
            for guesses in self.guess_range:
                game_tuple = (length, guesses)
                profile[game_tuple] = 0.0
                win_counter = 0
                print(
                    f"Length: {length}, Guesses: {guesses}, Number of Words: {len(words)} ")
                t1 = time.process_time()
                for word in words:
                    game = Wordle(word, guesses, subdue=True)
                    is_win = self.profile_game(game)
                    win_counter = (
                        win_counter + 1 if is_win else win_counter
                    )
                t2 = time.process_time()
                print(f"Time to guess the words: {t2-t1}")
                profile[game_tuple] = 100 * (win_counter / len(words))
                profile[game_tuple] = round(profile[game_tuple],2)
                print(f"Win Percentage: {profile[game_tuple]} %")

        return profile

    def profile_game(self, game):
        self.solver.set_game(game)
        self.solver.solve()
        return game.has_won()
