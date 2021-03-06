from enum import Enum


class StrategyEnum(Enum):
    RAND = 1
    RAND_CAND = 2
    DEEDY = 3
    USER = 4
    FIVE_HIT = 5
    THREE_HIT = 6
    TIES_POP = 7
    FIVE_HIT_TIES_POP = 8
    WEDGE = 9

    def from_str(label):
        if label == "RAND":
            return StrategyEnum.RAND
        if label == "RAND_CAND":
            return StrategyEnum.RAND_CAND
        if label == "DEEDY":
            return StrategyEnum.DEEDY
        if label == "USER":
            return StrategyEnum.USER
        if label == "FIVE_HIT":
            return StrategyEnum.FIVE_HIT
        if label == "TIES_POP":
            return StrategyEnum.TIES_POP
        if label == "FIVE_HIT_TIES_POP":
            return StrategyEnum.FIVE_HIT_TIES_POP
        if label == "THREE_HIT":
            return StrategyEnum.THREE_HIT
        if label == "WEDGE":
            return StrategyEnum.WEDGE
        raise NotImplementedError


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
NUM_THREADS = 1000
WORDS_FILE_PATH = "./data/words.txt"
WORDS = load_text_file(WORDS_FILE_PATH)
DIFFICULTY_TO_WORD_MAP_PICKLE_FILE_PATH = "./data/difficulty_to_word.pkl"
DIFFICULTY_TO_FREQUENCY_PICKLE_FILE_PATH = "./data/difficulty_to_frequency.pkl"
CLUE_BIT_TO_EMOJI_MAP = {
    0: "⬛",
    1: "🟨",
    2: "🟩",
}
STRATEGY_CHOICES = [e.name for e in StrategyEnum]
EXPLORATION_WEIGHT = 0.5