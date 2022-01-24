from util.wordutil import WordUtil
import random
class RandomStrategy:
    def __init__(self,length):
        self.length = length

    def get_guess(self):
        return random.choice(list(WordUtil().get_words_of_given_length(length=self.length)))