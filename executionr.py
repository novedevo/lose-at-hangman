# boring exception classes

class GameWonException(Exception):
    pass


class GameLostException(Exception):
    pass


# Default, headless executioner. Perfect in every way 🥰.
class Executionr:

    # constructor
    def __init__(self, word: str, guess_limit: int = 6) -> None:
        self.wrong_guesses = 0
        self.guess_limit = guess_limit
        self.word = word
        self.current_string = list("." * len(word))

    # checks the guess passed in as `letter` against the canonical word,
    # returns a newly constrained half-formed regex pattern as a string
    # e.g. word=apple, guess=e, returned regex is `....e`
    def check_answer(self, letter: str) -> str:

        # wrong guess
        if letter not in self.word:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.guess_limit:
                raise GameLostException()
            return "".join(self.current_string) # have to convert list to string

        # update the regex pattern
        for i in range(len(self.current_string)):
            if self.word[i] == letter:
                self.current_string[i] = letter

        # if the game is over
        if "".join(self.current_string) == self.word:
            raise GameWonException(self.word)

        return "".join(self.current_string)

# Little more than a wrapper for input(). Uses the same method signatures as Executionr to maintain polymorphism.
class PlayerExecutionr:
    def __init__(self):
        pass

    def check_answer(self, letter: str) -> str:
        return input("Please update the string, using \".\" for an empty character: ")
        # relies pretty heavily on the executioner player being perfect and good at typing
