# constants.py
def load_dictionary(filename):
    with open(filename, 'r') as f:
        return set(f.read().split())

DEFAULT_WORD_LENGTH = 5
DEFAULT_NUM_GUESSES = 6
DIFFICULTY_CHOICES = [1,2,3]
DEFAULT_DIFFICULTY = 2
MAX_GUESSES = 50
MAX_WORD_LENGTH = 20
WORDS_FILE_PATH = './data/words.txt'
WORD_TO_DIFFICULTY_PICKLE_OBJECT_FILE_PATH = './data/word_to_difficulty.pkl'
WORDS = load_dictionary(WORDS_FILE_PATH)