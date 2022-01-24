import string
from util.constants import WORDS


class UserStrategy:
    def __init__(self, wordle):
        self.wordle = wordle
        qwertyKeyboard = 'qwertyuiopasdfghjklzxcvbnm'
        self.unused_letters = (list(qwertyKeyboard))

    def get_guess(self):
        guess = ""
        while True:
            print(f"Unused Letters: ",end='')
            for letter in self.unused_letters:
                print(f"{letter.upper()}", end=' ')
            guess = input("\nEnter guess: ").strip().lower()
            if len(self.wordle.word) != len(guess):
                print(f"Your guess '{guess}' is not of length {len(self.wordle.word)}!")
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
