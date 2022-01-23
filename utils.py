# utils.py
import argparse
import random
import pandas as pd
from re import M
from constants import *
from wordfreq import zipf_frequency

def get_word_difficulty(word):
    global frequency_list
    frequency = zipf_frequency(word, 'en')
    if frequency == 0:
        return None
    elif frequency > 2.63:
        return 1
    elif frequency > 1.7:
        return 2
    else:
        return 3

def get_difficulty_to_words_map(difficulty=None):
    difficulty_to_words_map = {}
    
    for word in WORDS:
        difficulty = get_word_difficulty(word)
        if difficulty is None:
            continue
        elif difficulty not in difficulty_to_words_map:
            difficulty_to_words_map[difficulty] = set(word)
        else:
            difficulty_to_words_map[difficulty].add(word)
    
    return difficulty_to_words_map if difficulty is None else difficulty_to_words_map[difficulty]

def get_word(length, difficulty):
    specific_words = get_difficulty_to_words_map(difficulty=difficulty)
    if length == 1:
        word = random.choice(list(specific_words))
        return word
    else:
        specific_words = list(filter(lambda x: len(x) == length, specific_words))
        return random.choice(specific_words)

def validate_args(args):
    print("Validating arguments...")
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