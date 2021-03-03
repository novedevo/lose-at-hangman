from executionr import GameWonException
import csv
from typing import Dict, Tuple
from random import sample
import re


class Guessr:
    wordsFile = open("data/words.txt")
    orderedWordsFile = csv.reader(open("data/English_Word_Prevalences.csv"))
    alphabet = "abcdefghijklmnopqrstuvwxyz-".upper()
    ordered_alphabet = "ESIARNOTLCDUPMGHBYFKVWZXQJ-"

    next(wordsFile)
    next(wordsFile)

    next(orderedWordsFile)

    def __init__(self, blank_slate: str, smart: bool) -> None:
        self.words = []
        self.guesses = []
        self.last_guess = None
        self.information = blank_slate
        if smart:
            for row in Guessr.orderedWordsFile:
                self.words.append((row[0].upper(), float(row[1])))
        for word in Guessr.wordsFile:
            if re.match("^"+self.information+"$", word) and word != (entry[0] for entry in self.words):
                self.words.append((word.strip(), 0.01))
        self.filter_list(number_of_letters=len(self.information))

        if len(self.words) == 1:
            raise GameWonException(self.words[0][0])

    def new_information(self, information: str) -> None:
        if information.count(".") == 0:
            raise GameWonException(information)
        if information == self.information:
            self.filter_list(letter_not_in=self.last_guess)
        else:
            self.information = information
            self.words = [word for word in self.words if re.compile("^" + information + "$").match(
                word[0]) and (word[0].count(self.last_guess) == information.count(self.last_guess))]
        if len(self.words) == 1:
            raise GameWonException(self.words[0][0])

    def filter_list(self, number_of_letters: int = None, letter_not_in: str = None) -> None:
        if number_of_letters:
            self.words = list(filter(lambda word: len(
                word[0]) == number_of_letters, self.words))
        if letter_not_in:
            self.words = list(
                word for word in self.words if letter_not_in not in word[0])

    def make_random_guess(self) -> str:
        for letter in sample(Guessr.alphabet, len(Guessr.alphabet)):
            if letter not in self.guesses:
                self.guesses.append(letter)
                self.last_guess = letter
                return letter
        else:
            exit(-1)

    def make_ordered_guess(self) -> str:
        for letter in Guessr.ordered_alphabet:
            if letter not in self.guesses:
                self.guesses.append(letter)
                self.last_guess = letter
                return letter
        else:
            exit(-1)

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

    def get_letter_frequencies(self) -> Dict:
        freqs = {}
        alphabet = [
            letter for letter in Guessr.alphabet if letter not in self.guesses]

        for letter in alphabet:
            freqs[letter] = 0.0

        for word in self.words:
            for letter in word[0]:
                try:
                    freqs[letter] += word[1]
                except KeyError:
                    continue

        return freqs

    def print_words(self):
        for word in self.words:
            print(word)
