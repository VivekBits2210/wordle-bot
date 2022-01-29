import random
from wordfreq import zipf_frequency, word_frequency
from util.constants import *
from util.log_gen import get_logger
from util.pickleutil import pull_pickle_file, push_pickle_file

logger = get_logger(__file__)


class WordUtil:
    def __init__(self, *, length=None, difficulty=None):
        self.length = length
        self.difficulty = difficulty
        self.word = None
        self.difficulty_to_frequency_interval_map = None

    def get_word(self):
        specific_words = self.get_words_of_given_difficulty()
        if self.length != 0:
            specific_words = self.get_words_of_given_length(words=specific_words)
            if len(specific_words) == 0:
                raise Exception(
                    f"No words of length {self.length} and difficulty {self.difficulty}"
                )

        self.word = random.choice(list(specific_words))
        return self.word

    def get_words_of_given_difficulty(self, difficulty=None, *, force_create=False):
        if difficulty is None:
            difficulty = self.difficulty
        difficulty_to_words_map = {}

        if not force_create:
            difficulty_to_words_map = pull_pickle_file(
                DIFFICULTY_TO_WORD_MAP_PICKLE_FILE_PATH
            )
            if difficulty_to_words_map is not None:
                return difficulty_to_words_map[difficulty]

        # Create difficulty to words map if not exist (or if force_create)
        difficulty_to_words_map = self.create_word_to_difficulty_map()
        push_pickle_file(
            DIFFICULTY_TO_WORD_MAP_PICKLE_FILE_PATH, difficulty_to_words_map
        )

        return difficulty_to_words_map[difficulty]

    def get_words_of_given_length(self, length=None, *, words=WORDS):
        if length is None:
            length = self.length

        specific_words = set(filter(lambda x: len(x) == length, words))
        if len(specific_words) == 0:
            raise Exception(f"No words of length {length} found with given constraints")

        return specific_words

    # TODO: Make number of difficulty levels pluggable
    def get_word_difficulty(self, word=None):
        if word is None:
            word = self.word
        frequency = self.get_word_frequency(word, kind="zipf")
        num_difficulty_levels = len(DIFFICULTY_CHOICES)

        if self.difficulty_to_frequency_interval_map:
            return self.get_difficulty_from_frequency_interval_map(frequency)
        else:
            # Difficulty to frequency contains data in the form ({<Num Difficulty>:{<Difficulty Level>:<Frequency Interval>,..},..})
            difficulty_to_frequency_interval_data = pull_pickle_file(
                DIFFICULTY_TO_FREQUENCY_PICKLE_FILE_PATH
            )
            if difficulty_to_frequency_interval_data is not None:
                self.difficulty_to_frequency_interval_map = (
                    difficulty_to_frequency_interval_data[num_difficulty_levels]
                )
                return self.get_difficulty_from_frequency_interval_map(frequency)

            # Create difficulty to frequency map if not exist
            difficulty_to_frequency_interval_data = (
                self.create_difficulty_to_frequency_interval_data()
            )
            self.difficulty_to_frequency_interval_map = (
                difficulty_to_frequency_interval_data[num_difficulty_levels]
            )
            push_pickle_file(
                DIFFICULTY_TO_FREQUENCY_PICKLE_FILE_PATH,
                difficulty_to_frequency_interval_data,
            )
            self.get_words_of_given_difficulty(1, force_create=True)

            return self.get_difficulty_from_frequency_interval_map(frequency)

    def get_word_frequency(self, word=None, *, kind="zipf"):
        if word is None:
            word = self.word

        if kind == "zipf":
            return zipf_frequency(word, "en")
        elif kind == "general":
            return word_frequency(word, "en")
        else:
            raise Exception(f"Invalid kind: {kind}")

    def get_difficulty_from_frequency_interval_map(self, frequency):
        for difficulty in self.difficulty_to_frequency_interval_map:
            if frequency in self.difficulty_to_frequency_interval_map[difficulty]:
                return difficulty
        raise Exception(f"Word is too rare.")

    def create_word_to_difficulty_map(self, *, words=WORDS):
        difficulty_to_words_map = {}
        for word in words:
            self.word = word
            difficulty = self.get_word_difficulty()

            # Ignore words with very high difficulty
            if difficulty is None:
                continue

            if difficulty not in difficulty_to_words_map:
                difficulty_to_words_map[difficulty] = set(word)
            else:
                difficulty_to_words_map[difficulty].add(word)
        return difficulty_to_words_map

    def create_difficulty_to_frequency_interval_data(self):
        import pandas as pd

        # data to be pushed
        data = {}

        frequency_series = pd.Series(
            [self.get_word_frequency(word, kind="zipf") for word in WORDS]
        )
        dataframe = pd.DataFrame(frequency_series, columns=["frequency"])
        dataframe = dataframe[dataframe.frequency > 0]
        for num_choices in range(2, MAX_DIFFICULTY_CHOICES_INTERNAL + 1):
            intervals = pd.qcut(dataframe.frequency, num_choices).cat.categories
            difficulty_codes = reversed(
                range(1, num_choices + 1)
            )  # Reversed as least frequent is most difficult
            difficulty_to_frequency_interval_map = dict(
                zip(difficulty_codes, intervals)
            )
            data[num_choices] = difficulty_to_frequency_interval_map
        return data
