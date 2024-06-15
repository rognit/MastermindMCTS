import numpy as np
import random
from mastermind import Mastermind


class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, child_state):
        child = MCTSNode(child_state, self)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def ucb1(self):
        return self.wins / self.visits + np.sqrt(2 * np.log(self.parent.visits) / self.visits)


class MCTS:
    def __init__(self, game):
        self.game = game
        self.possible_codes = self._generate_all_possible_codes()

    def _generate_all_possible_codes(self):
        from itertools import product
        return list(product(range(1, self.game.num_colors + 1), repeat=self.game.code_length))

    def search(self, num_iterations):
        root = MCTSNode(self.game.history)
        for _ in range(num_iterations):
            node = self._select(root)
            if not self.game.is_solved(node.state[-1]):
                node = self._expand(node)
            reward = self._simulate(node.state)
            self._backpropagate(node, reward)
        return self._best_child(root)

    def _select(self, node):
        while node.children:
            node = max(node.children, key=lambda child: child.ucb1())
        return node

    def _expand(self, node):
        possible_moves = self._get_possible_moves(node.state)
        for move in possible_moves:
            new_state = node.state + [move]
            node.add_child(new_state)
        return random.choice(node.children)

    def _simulate(self, state):
        game_copy = Mastermind(self.game.code_length, self.game.num_colors)
        game_copy.secret_code = self.game.secret_code
        game_copy.history = state[:]

        possible_codes = self.possible_codes[:]
        initial_possibilities = len(possible_codes)

        while not game_copy.is_solved(state[-1]):
            guess = self._make_random_move()
            exact, partial = game_copy.make_guess(guess)
            possible_codes = [code for code in possible_codes if
                              self._is_consistent_with_feedback(code, guess, exact, partial)]
            state.append(guess)

        final_possibilities = len(possible_codes)
        reward = initial_possibilities - final_possibilities
        return reward

    def _is_consistent_with_feedback(self, code, guess, exact, partial):
        game_copy = Mastermind(self.game.code_length, self.game.num_colors)
        game_copy.secret_code = code
        guess_exact, guess_partial = game_copy.evaluate_guess(guess)
        return guess_exact == exact and guess_partial == partial

    def _backpropagate(self, node, reward):
        while node is not None:
            node.update(reward)
            node = node.parent

    def _best_child(self, node):
        return max(node.children, key=lambda child: child.visits)

    def _get_possible_moves(self, state):
        return self.possible_codes

    def _make_random_move(self):
        return random.choice(self.possible_codes)
