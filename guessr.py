from executionr import GameWonException
import csv
from typing import Dict
from random import sample
import re

# Really good at guessing in hangman.
# Contains multiple guessing methods


class Guessr:

    # statements placed here are run once when the class is defined, but never again
    # making them perfect for file preparation
    wordsFile = open("data/words.txt")
    orderedWordsFile = csv.reader(open("data/English_Word_Prevalences.csv"))
    alphabet = "abcdefghijklmnopqrstuvwxyz-".upper()
    ordered_alphabet = "ESIARNOTLCDUPMGHBYFKVWZXQJ-"

    # first two lines are garbage
    next(wordsFile)
    next(wordsFile)

    # first line is garbage
    next(orderedWordsFile)

    # constructor
    def __init__(self, blank_slate: str) -> None:
        self.words = []
        self.guesses = []
        self.last_guess = None
        self.information = blank_slate

        # load in the weighted words
        for row in Guessr.orderedWordsFile:
            self.words.append((row[0].upper(), float(row[1])))

        # load in the backup list of words from words.txt
        for word in Guessr.wordsFile:
            # hacky regex
            if re.match("^"+self.information+"$", word) and word != (entry[0] for entry in self.words):
                # low weight to deprioritize the massive list of backups compared to the weighted list of common words
                self.words.append((word.strip(), 0.01))

        # immediately restrict the list to the words with the correct length
        self.filter_list(number_of_letters=len(self.information))

        # instawin
        if len(self.words) == 1:
            raise GameWonException(self.words[0][0])

    # incorporate a new regex into the restrictions
    def new_information(self, information: str) -> None:

        # win condition for human executioners, if you're passed a completed string already
        if information.count(".") == 0:
            raise GameWonException(information)

        # last guess was incorrect :(
        if information == self.information:
            self.filter_list(letter_not_in=self.last_guess)

        # filter the new list
        else:
            self.information = information
            self.words = [
                word for word in self.words if

                # regex match the new constraints
                re.compile("^" + information + "$").match(word[0]) and

                # no additional characters of the previous guess in the wrong places
                (word[0].count(self.last_guess) ==
                 information.count(self.last_guess))
            ]

        # win!
        if len(self.words) == 1:
            raise GameWonException(self.words[0][0])

    # used for initial mass filtration
    def filter_list(self, number_of_letters: int = None, letter_not_in: str = None) -> None:
        if number_of_letters:
            self.words = [word for word in self.words if len(word[0]) == number_of_letters]
        if letter_not_in:
            self.words = [word for word in self.words if letter_not_in not in word[0]]

    # terrible method. use for control purposes only
    def make_random_guess(self) -> str:
        for letter in sample(Guessr.alphabet, len(Guessr.alphabet)):
            if letter not in self.guesses:
                self.guesses.append(letter)
                self.last_guess = letter
                return letter
        else:
            exit(-1)

    # not much better, but close to how humans play for the first few letters
    def make_ordered_guess(self) -> str:
        for letter in Guessr.ordered_alphabet:
            if letter not in self.guesses:
                self.guesses.append(letter)
                self.last_guess = letter
                return letter
        else:
            exit(-1)

    # where the magic happens
    def make_strategic_guess(self) -> str:
        freqs = self.get_letter_frequencies()

        if len(freqs) == 0:
            exit(-1)

        number_of_possibilities = len(self.words)

        letter = min((key for key in freqs), key=lambda i: abs(
            freqs[i] - number_of_possibilities))
        self.last_guess = letter
        self.guesses.append(letter)
        print(letter)
        return letter

    # calculates how often letters appear in the words remaining
    def get_letter_frequencies(self) -> Dict:
        freqs = {}
        alphabet = [
            letter for letter in Guessr.alphabet if letter not in self.guesses]

        for letter in alphabet:
            freqs[letter] = 0.0

        for word in self.words:
            for letter in set(word[0]):
                try:
                    freqs[letter] += word[1]
                except KeyError:
                    continue

        return freqs

    def print_words(self):
        for word in self.words:
            print(word)
