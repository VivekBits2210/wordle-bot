import time
from util.log_gen import get_logger
from util.constants import StrategyEnum
from solver.strategy.random_strategy import RandomStrategy
from solver.strategy.random_candidate_strategy import RandomCandidateStrategy
from solver.strategy.deedy_strategy import DeedyStrategy
from solver.strategy.user_strategy import UserStrategy
from solver.strategy.five_hit_strategy import FiveHitStrategy
from solver.strategy.five_hit_popular_break_strategy import (
    FiveHitWithPopularWordTieBreakStrategy,
)
from solver.strategy.break_ties_by_popularity_strategy import (
    BreakTiesByPopularityStrategy,
)

logger = get_logger(__file__)
strategy_enum_to_strategy_mapper = {
    StrategyEnum.RAND: RandomStrategy,
    StrategyEnum.RAND_CAND: RandomCandidateStrategy,
    StrategyEnum.DEEDY: DeedyStrategy,
    StrategyEnum.USER: UserStrategy,
    StrategyEnum.FIVE_HIT: FiveHitStrategy,
    StrategyEnum.FIVE_HIT_TIES_POP: FiveHitWithPopularWordTieBreakStrategy,
    StrategyEnum.TIES_POP: BreakTiesByPopularityStrategy,
}


class Solver:
    def __init__(self, game, strategy, *, subdue=False, slow=False):
        self.slow = slow
        self.subdue = subdue
        self.game = game
        self.strategy_enum = StrategyEnum.from_str(strategy)
        self.strategy = strategy_enum_to_strategy_mapper[self.strategy_enum]()

    def set_game(self, game):
        self.game = game
        self.strategy.set_game(game)

    def solve(self):
        if not self.subdue:
            print(f"Strategy: {self.strategy_enum.name}\n")
        while True:
            guess = self.strategy.get_guess()
            self.game.play(guess)
            self.game.pretty_print_game_output()
            if self.game.is_game_complete():
                break

            if self.slow:
                print("On slow mode, waiting for input: ", end="")
                input()
