import traceback
from game.wordle import Wordle
from profiler.profiler import Profiler
from util.parser import Parser
from util.log_gen import get_logger
from solver.solver import Solver

"""
Work left:
- Removing direct access to word by strategy
- Profiling on threads
- Even faster profiling
- Speed up candidate pruning -> generate regex on the fly?
- Add support for multiple words
- Test suite
- Other solver strategies
- Deep learning solver strategy
"""


def main():
    try:
        logger = get_logger(__file__)
        parser = Parser()
    except Exception as e:
        print(e)
        traceback.print_exc()
        quit(2)

    try:
        args = parser.parse()

        if args.profiler:  # Profile
            profiler = Profiler(args.strategy)
            print(profiler.get_profile())
        else:  # Solve
            if args.strategy == "USER":
                temp_dict = {key: vars(args)[key] for key in vars(args) if key != "word"}
                print(f"Conditions: {temp_dict}")
                game = Wordle(args.word, args.guesses, show_word=False)
            else:
                print(f"Conditions: {vars(args)}")
                game = Wordle(args.word, args.guesses)

            solver = Solver(game, args.strategy, slow=args.slow)
            solver.set_game(game)
            solver.solve()
    except Exception as e:
        logger.error(f"{repr(e)}")
        traceback.print_exc()
        if parser.args.debug:
            traceback.print_exc()


if __name__ == "__main__":
    main()
