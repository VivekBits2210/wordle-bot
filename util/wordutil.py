import os
import pickle
import random
from wordfreq import zipf_frequency, word_frequency
from util.constants import WORD_TO_DIFFICULTY_PICKLE_OBJECT_FILE_PATH, WORDS
from util.log_gen import get_logger
logger = get_logger(__file__)
        
class WordUtil:
    def __init__(self, *, length=None, difficulty=None):
        self.length = length
        self.difficulty = difficulty
        self.word = None
    
    def get_word(self):
        specific_words = self.get_words_of_given_difficulty()
        if self.length != 0:
            specific_words = self.get_words_of_given_length(words=specific_words)
            if len(specific_words) == 0:
                raise Exception(f"No words of length {self.length} and difficulty {self.difficulty}")
            
        self.word = random.choice(list(specific_words))
        return self.word

    def get_words_of_given_difficulty(self,difficulty=None):
        if difficulty is None:
            difficulty = self.difficulty

        difficulty_to_words_map = {}

        try:
            if os.path.exists(WORD_TO_DIFFICULTY_PICKLE_OBJECT_FILE_PATH):
                with open(WORD_TO_DIFFICULTY_PICKLE_OBJECT_FILE_PATH, 'rb') as f:
                    difficulty_to_words_map = pickle.load(f)
                return difficulty_to_words_map[difficulty]
        except KeyError:
            logger.error(f"Pickle file {WORD_TO_DIFFICULTY_PICKLE_OBJECT_FILE_PATH} has invalid structure")            
        except pickle.PicklingError:
            logger.error(f"Failed to load pickle file {WORD_TO_DIFFICULTY_PICKLE_OBJECT_FILE_PATH}, probably corrupted.")

        for word in WORDS:
            self.word = word
            difficulty = self.get_word_difficulty()
            if difficulty not in difficulty_to_words_map:
                difficulty_to_words_map[difficulty] = set(word)
            else:
                difficulty_to_words_map[difficulty].add(word)
                
        with open(WORD_TO_DIFFICULTY_PICKLE_OBJECT_FILE_PATH, 'wb') as f:
            pickle.dump(difficulty_to_words_map, f)

        return difficulty_to_words_map[difficulty]

    def get_words_of_given_length(self,length=None,*,words=WORDS):
        if length is None:
            length = self.length
        
        specific_words = set(filter(lambda x: len(x) == length, words))
        if len(specific_words)==0:
            raise Exception(f"No words of length {length} found with given constraints")
        
        return specific_words

    # TODO: Make number of difficulty levels pluggable
    def get_word_difficulty(self,word=None):
        if word is None:
            word = self.word

        frequency = self.get_word_frequency(word, kind='zipf')
        if frequency == 0:
            return None
        elif frequency > 2.63:
            return 1
        elif frequency > 1.7:
            return 2
        elif frequency > 0:
            return 3
        else:
            raise Exception(f"Word {word} has very low frequency: {frequency}")

    def get_word_frequency(self, word=None, *, kind):
        if word is None:
            word = self.word

        if kind == 'zipf':
            return zipf_frequency(word, 'en')
        elif kind == 'general':
            return word_frequency(word, 'en')
        else:
            raise Exception(f"Invalid kind: {kind}")

    

    