import string
from util.constants import WORDS


class UserStrategy:
    def __init__(self, game=None):
        self.game = game
        qwertyKeyboard = "qwertyuiopasdfghjklzxcvbnm"
        self.unused_letters = list(qwertyKeyboard)

    def set_game(self,game):
        self.game = game
        self.word_length = self.game.word_length

    def get_guess(self):
        guess = ""
        while True:
            print(f"Unused Letters: ", end="")
            for letter in self.unused_letters:
                print(f"{letter.upper()}", end=" ")
            guess = input("\nEnter guess: ").strip().lower()
            if self.word_length != len(guess):
                print(f"Your guess '{guess}' is not of length {len(self.word_length)}!")
                continue
            if not guess.isalpha():
                print(f"Your guess '{guess}' is not a valid word")
                continue
            if guess not in WORDS:
                print(f"Your guess '{guess}' is not in the dictionary")
                continue
            for letter in guess:
                if letter in self.unused_letters:
                    self.unused_letters.remove(letter)
            break
        return guess
