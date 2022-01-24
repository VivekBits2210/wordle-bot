from pyrsistent import b
from util.constants import WORDS
from util.wordutil import WordUtil
import random


class UserStrategy:
    def __init__(self, wordle):
        self.wordle = wordle

    def get_guess(self):
        guess = ""
        while True:
            guess = input("Enter guess: ").strip().lower()
            if len(self.wordle.word) != len(guess):
                print(f"Your guess '{guess}' is not of length {len(self.wordle.word)}!")
                continue
            if not guess.isalpha():
                print(f"Your guess '{guess}' is not a valid word")
                continue
            if guess not in WORDS:
                print(f"Your guess '{guess}' is not in the dictionary")
                continue
            break
        return guess