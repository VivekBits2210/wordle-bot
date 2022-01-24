from util.log_gen import get_logger
from util.constants import StrategyEnum
from solver.random_strategy import RandomStrategy
from solver.random_candidate_strategy import RandomCandidateStrategy
from solver.deedy_strategy import DeedyStrategy

logger = get_logger(__file__)
strategy_enum_to_strategy_mapper = {
        StrategyEnum.RAND: RandomStrategy,
        StrategyEnum.RAND_CAND: RandomCandidateStrategy,
        StrategyEnum.DEEDY: DeedyStrategy
}

class Solver:
    def __init__(self, slow, strategy, wordle):
        self.slow = slow
        self.wordle = wordle
        self.strategy_enum = StrategyEnum.from_str(strategy)
        self.strategy = strategy_enum_to_strategy_mapper[self.strategy_enum](self.wordle)

    def solve(self):
        print(f"Strategy: {self.strategy_enum.name}\n")
        while True:
            guess = self.strategy.get_guess()
            self.wordle.play(guess)
            self.wordle.pretty_print_game_output()
            
            if self.wordle.is_game_complete():
                break
            
            if self.slow:
                print("On slow mode, waiting for input: ", end="")
                input()
