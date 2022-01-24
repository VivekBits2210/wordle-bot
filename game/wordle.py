from util.constants import CLUE_BIT_TO_EMOJI_MAP
from util.log_gen import get_logger
logger = get_logger(__file__)

class Wordle:
    def __init__(self, word, num_guesses):
        self.word = word
        self.total_guesses = num_guesses
        self.num_guesses = num_guesses
        self.guess_history = []
        self.clue_bits_history = []
        print(f"Started Wordle game for word {self.word} with {self.num_guesses} guesses remaining...\n")

    # 0 -> nothing, 1 -> out of place, 2 -> accurate
    def get_clue_bits(self,word_guess):
        if self.num_guesses <= 0:
            self.print_result()            
            return None

        self.num_guesses-=1
        self.guess_history.append(word_guess)
        
        clue_bits = {}
        for i in range(len(self.word)):
            if word_guess[i] == self.word[i]:
                clue_bits[i] = 2
            elif word_guess[i] in self.word:
                clue_bits[i] = 1
            else:
                clue_bits[i] = 0
        self.clue_bits_history.append(clue_bits)

        if self.has_won():
            self.print_result()
            self.num_guesses = 0 # Prevent further play

        return clue_bits

    def convert_clues_to_emoji(self,clue_bits=None):
        emoji_string = ""

        if clue_bits is None:
            clue_bits = self.clue_bits_history[-1]

        for position in clue_bits:
            emoji_string += CLUE_BIT_TO_EMOJI_MAP[clue_bits[position]]

        return emoji_string
    
    def has_won(self):
        return (self.word in self.guess_history)
    
    def has_lost(self):
        return not self.has_won() and self.num_guesses <= 0

    def print_result(self):
        if self.has_won():
            print(f"Player has won using {self.total_guesses - self.num_guesses} out of {self.total_guesses} guesses!", end='\n\n')
        else:
            print(f"Player lost, the word is '{self.word}'!", end='\n\n')

    def pretty_print_guess(self):
        print(f"Guess ({self.total_guesses - self.num_guesses}/{self.total_guesses}):-",end="\n\n")
        print(f"  {'  '.join(self.guess_history[-1].upper())}")
        print(f" {' '.join(self.convert_clues_to_emoji(self.clue_bits_history[-1]))}",end="\n\n")            
    