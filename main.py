import numpy as np

from mcts import FeedbackNode


def evaluate_guess(guess, secret_code):
    exact = sum([1 for i in range(len(secret_code)) if guess[i] == secret_code[i]])
    return exact, sum([min(guess.count(j), secret_code.count(j)) for j in set(guess)]) - exact


def select(root):
    guess_nodes = root.children
    chosen_guess_node = max(guess_nodes, key=lambda guess_node: guess_node.score())

    if chosen_guess_node.children:
        feedback_nodes = chosen_guess_node.children
        frequencies = [node.frequency for node in feedback_nodes]
        total_frequency = np.sum(frequencies)
        normalized_probabilities = [freq / total_frequency for freq in frequencies]

        chosen_feedback_node = np.random.choice(feedback_nodes, p=normalized_probabilities)

        return chosen_feedback_node

    return chosen_guess_node

    while node.children:
        node = max(node.children, key=lambda child: child.ucb1())

    return node


def expand(guess_node):
    guess_node.expand()


def simulate(guess_node):
    return guess_node.simulate()  # (moves)


def backpropagate(node, total_moves):
    while node is not None:
        node.update(total_moves)
        node = node.parent


def best_child(feedback_node):
    return max(feedback_node.children, key=lambda child: child.visits) if feedback_node.children else None


def mcts_training(num_iterations):
    parameters = {
        "code_length": 2,
        "num_colors": 3
    }
    root = FeedbackNode(parameters)
    for _ in range(num_iterations):
        guess_node = select(root)
        expand(guess_node)
        total_moves = simulate(guess_node)
        backpropagate(guess_node, total_moves)


def main():
    mcts_training(10)


if __name__ == "__main__":
    main()
