# utils.py
import argparse
import random
from re import M
from constants import *
from wordfreq import word_frequency

def get_word_frequency(word):
    return word_frequency(word, 'en')

def validate_args(args):
    if not args.word:
        args.word = get_word(args.length, args.difficulty)
    args.word = args.word.lower()
    if args.word not in WORDS:
        raise Exception('Word must be in the dictionary or be specified')
    if args.length < 1 or args.length > MAX_WORD_LENGTH:
        raise Exception("Word length must be between 1 and {}".format(MAX_WORD_LENGTH))
    if args.word and len(args.word) != args.length:
        raise Exception('Word length must match the length of the word')
    if args.guesses < 1 or args.guesses > MAX_GUESSES:
        raise Exception('Number of guesses must be between 1 and {}'.format(MAX_GUESSES))
    if args.difficulty not in DIFFICULTY_CHOICES:
        raise Exception('Difficulty must be one of {}'.format(DIFFICULTY_CHOICES))

def get_word(length, difficulty):
    if length == 1:
        word = random.choice(list(WORDS))
    else:
        word = random.choice(list(filter(lambda x: len(x) == length, WORDS)))


def fetch_arguments_parser():
    parser = argparse.ArgumentParser(description="Wordle Bot Arena")
    parser.add_argument('-w',
                        '--word',
                        help='Word to solve',
                        default=None,
                        required=False)
    parser.add_argument('-n',
                        '--length',
                        type=int,
                        help='Length of word',
                        default=DEFAULT_WORD_LENGTH,
                        required=False)
    parser.add_argument('-g',
                        '--guesses',
                        help='Number of guesses allowed',
                        default=DEFAULT_NUM_GUESSES,
                        required=False)
    parser.add_argument('-s',
                        '--slow',
                        help='Wait for user input after every guess',
                        action='store_true',
                        default=False,
                        required=False)
    parser.add_argument('-d',
                        '--difficulty',
                        help='Difficulty level',
                        type=int,
                        choices=DIFFICULTY_CHOICES,
                        default=DEFAULT_DIFFICULTY,
                        required=False)
    return parser