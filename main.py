import argparse
from parser import Parser
from solver import Solver

def main():
    parser = Parser()
    args = parser.parse()
    solver = Solver(**vars(args))
    solver.solve()

if __name__ == '__main__':
    main()
