# main.py
import argparse
from utils import fetch_arguments_parser, validate_args
from solver import Solver

def main():
    parser = fetch_arguments_parser()
    args = parser.parse_args()
    validate_args(args)
    solver = Solver(**vars(args))
    solver.solve()    

if __name__ == '__main__':
    main()
