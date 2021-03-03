class GameWonException(Exception):
    pass


class GameLostException(Exception):
    pass


class Executionr:
    def __init__(self, word: str, guess_limit: int = 6) -> None:
        self.wrong_guesses = 0
        self.guess_limit = guess_limit
        self.word = word
        self.current_string = list("." for _ in word)

    def check_answer(self, letter: str) -> str:
        if letter not in self.word:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.guess_limit:
                raise GameLostException()
            return "".join(self.current_string)

        for i in range(len(self.current_string)):
            if self.word[i] == letter:
                self.current_string[i] = letter

        if "".join(self.current_string) == self.word:
            raise GameWonException(self.word)
        return "".join(self.current_string)


class PlayerExecutionr:
    def __init__(self):
        pass

    def check_answer(self, letter: str) -> str:
        return input("Please update the string, using \".\" as the empty character: ")
