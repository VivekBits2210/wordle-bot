import argparse
import traceback
from parser import Parser
from solver import Solver
from log_gen import get_logger

def main():
    try:
        parser = Parser()
        args = parser.parse()
        solver = Solver(**vars(args))
        solver.solve()
    except Exception as e:
        logger.error(e)
        if parser.args.debug:
            traceback.print_exc()

if __name__ == '__main__':
    logger = get_logger(__file__)
    main()
