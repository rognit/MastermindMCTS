import numpy as np
import random
from itertools import product


def redlog(message):
    print(f"\033[91m{message}\033[0m")


def evaluate_guess(guess, secret_code):
    exact = sum([1 for i in range(len(secret_code)) if guess[i] == secret_code[i]])
    return exact, sum([min(guess.count(j), secret_code.count(j)) for j in set(guess)]) - exact


class GuessNode:
    def __init__(self, parent, parameters, guess):
        self.parameters = parameters
        self.guess = guess

        self.children = []
        self.parent = parent

        self.possible_codes = parent.possible_codes.copy()
        self.history = parent.history.copy()
        self.moves = parent.moves + 1  # (node depth)

        self.total_moves = 0  # sum of moves of all children (for ucb1)
        self.visits = 0

    def expand(self):  # (add feedback children)
        if len(self.possible_codes) == 1:
            redlog("ERROR: extent of a terminal GuessNode")

        possible_feedbacks = {}

        for code in self.possible_codes:
            feedback = evaluate_guess(code, self.guess)

            if feedback not in possible_feedbacks:
                possible_feedbacks[feedback] = [code]
            else:
                possible_feedbacks[feedback].append(code)

        n = len(self.possible_codes)

        for feedback in possible_feedbacks:
            child = FeedbackNode(self.parameters, feedback=feedback, parent=self,
                                 frequency=len(possible_feedbacks[feedback]) / n)
            self.children.append(child)

    def update(self, n_moves):
        self.visits += 1
        self.total_moves += n_moves

    def score(self):  # (ucb1)
        if self.visits == 0:
            return float('inf')
        score = -self.total_moves / self.visits + np.sqrt(2 * np.log(self.parent.visits) / self.visits)
        return score

    def simulate(self):
        moves, possible_codes, guess = self.moves, self.possible_codes.copy(), self.guess
        secret_code = random.choice(self.possible_codes)
        while True:
            feedback = evaluate_guess(guess, secret_code)
            if feedback == (self.parameters["code_length"], 0):
                return moves
            new_possible_codes = []
            for code in possible_codes:
                if evaluate_guess(guess, code) == feedback:
                    new_possible_codes.append(code)
            possible_codes = new_possible_codes
            moves += 1
            guess = random.choice(possible_codes)

    def __str__(self):
        return f"GuessNode : {self.history} With guess: {self.guess}"

    def is_terminal(self):
        return len(self.possible_codes) == 1


class FeedbackNode:
    def __init__(self, parameters, feedback=None, parent=None, frequency=1.):
        self.parameters = parameters
        self.feedback = feedback
        self.frequency = frequency

        self.visits = 0

        if parent:
            self.moves = parent.moves
            self.guess = parent.guess
            self.history = parent.history.copy()
            self.history.append((parent.guess, feedback))
            self.possible_codes = [code for code in parent.possible_codes if
                                   evaluate_guess(self.guess, secret_code=code) == feedback]
        else:
            self.moves = 0
            self.guess = None
            self.history = []
            self.possible_codes = list(
                product(range(1, self.parameters["num_colors"] + 1), repeat=self.parameters["code_length"]))

        self.parent = parent
        self.children = []

        self.expand()

    def simulate(self):
        redlog("ERROR: FeedbackNode should not simulate")

    def expand(self):  # (add_guess_children)
        for code in self.possible_codes:
            child = GuessNode(self, self.parameters, code)
            self.children.append(child)

    def score(self):
        return self.frequency

    def update(self, moves):
        self.visits += 1

    def __str__(self):
        return f"FeedbackNode : {self.history}"

    def is_terminal(self):
        redlog("ERROR: GuessNode should have been caught first")
        return len(self.possible_codes) == 1
