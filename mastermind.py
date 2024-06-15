import random


class Mastermind:
    def __init__(self, code_length=4, num_colors=6):
        self.code_length = code_length
        self.num_colors = num_colors
        self.secret_code = [random.randint(1, num_colors) for _ in range(code_length)]
        self.history = []

    def evaluate_guess(self, guess):
        exact = sum([1 for i in range(self.code_length) if guess[i] == self.secret_code[i]])
        return exact, sum([min(guess.count(j), self.secret_code.count(j)) for j in set(guess)]) - exact

    def is_solved(self, guess):
        exact, _ = self.evaluate_guess(guess)
        return exact == self.code_length

    def make_guess(self, guess):
        self.history.append(guess)
        return self.evaluate_guess(guess)
