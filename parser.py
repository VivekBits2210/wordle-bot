import argparse
from constants import *
from log_gen import get_logger
from wordutil import WordUtil
logger = get_logger(__file__)

def fetch_arguments_parser():
    parser = argparse.ArgumentParser(description="Wordle Bot Arena")
    parser.add_argument('-w',
                        '--word',
                        help='Word to solve',
                        default=None,
                        required=False)
    parser.add_argument('-n',
                        '--length',
                        help='Length of word',
                        type=int,
                        default=DEFAULT_WORD_LENGTH,
                        required=False)
    parser.add_argument('-g',
                        '--guesses',
                        help='Number of guesses allowed',
                        type=int,
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
    parser.add_argument('-D',
                        '--debug',
                        help="Debug mode",
                        action='store_true',
                        default=False,
                        required=False)
    return parser

class Parser:
    def __init__(self):
        self.parser = fetch_arguments_parser()
        self.args = None

    def parse(self):
        self.args = self.parser.parse_args()
        self._validate_args()
        return self.args
        
    def _validate_args(self):
        if self.args is None:
            self.args = self.parser.parse_args()
        
        logger.info("Validating arguments...")

        if self.args.word is None:
            self.args.word = WordUtil(self.args.length, self.args.difficulty).get_word()
        
        self.args.word = self.args.word.lower()
        if self.args.word not in WORDS:
            raise Exception(f'Word \"{self.args.word}\" is not in the dictionary')
        
        if self.args.length < 1 or self.args.length > MAX_WORD_LENGTH:
            raise Exception("Word length must be between 1 and {}".format(MAX_WORD_LENGTH))
        
        if self.args.word and len(self.args.word) != self.args.length:
            raise Exception('Word length must match the length of the word')
        
        if self.args.guesses < 1 or self.args.guesses > MAX_GUESSES:
            raise Exception('Number of guesses must be between 1 and {}'.format(MAX_GUESSES))
        
        if self.args.difficulty not in DIFFICULTY_CHOICES:
            raise Exception('Difficulty must be one of {}'.format(DIFFICULTY_CHOICES))

        logger.info(f"Valid Arguments: {vars(self.args)}")

    