def load_text_file(filename):
    with open(filename, "r") as f:
        return set(f.read().split())


DEFAULT_WORD_LENGTH = 5
DEFAULT_NUM_GUESSES = 6
DIFFICULTY_CHOICES = list(
    range(1, 10)
)  # NOTE: To effectively change this, delete both pickle files under data as well
MAX_DIFFICULTY_CHOICES_INTERNAL = 10
DEFAULT_DIFFICULTY = 2
MAX_GUESSES = 50
MAX_WORD_LENGTH = 20
WORDS_FILE_PATH = "./data/words.txt"
WORDS = load_text_file(WORDS_FILE_PATH)
DIFFICULTY_TO_WORD_MAP_PICKLE_FILE_PATH = "./data/difficulty_to_word.pkl"
DIFFICULTY_TO_FREQUENCY_PICKLE_FILE_PATH = "./data/difficulty_to_frequency.pkl"
CLUE_BIT_TO_EMOJI_MAP = {
    0: "⬛",
    1: "🟨",
    2: "🟩",
}
