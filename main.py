import traceback
from util.parser import Parser
from util.log_gen import get_logger
from solver.solver import Solver

def main():
    try:
        logger = get_logger(__file__)
        parser = Parser()
        args = parser.parse()
        solver = Solver(args.word,args.guesses)
        solver.solve()
    except Exception as e:
        logger.error(e)
        if parser.args.debug:
            traceback.print_exc()

if __name__ == '__main__':
    main()
