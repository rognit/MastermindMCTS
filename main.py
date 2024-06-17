import random
import statistics
from itertools import product

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm

from mcts import FeedbackNode

def redlog(message):
    print(f"\033[91m{message}\033[0m")
def bluelog(message):
    print(f"\033[94m{message}\033[0m")



def evaluate_guess(guess, secret_code):
    exact = sum([1 for i in range(len(secret_code)) if guess[i] == secret_code[i]])
    return exact, sum([min(guess.count(j), secret_code.count(j)) for j in set(guess)]) - exact


def select(node):
    guess_nodes = node.children
    if not guess_nodes:
        return node
    chosen_guess_node = max(guess_nodes, key=lambda guess_node: guess_node.score())

    if chosen_guess_node.children:
        feedback_nodes = chosen_guess_node.children

        probas = [node.score() for node in feedback_nodes]
        chosen_feedback_node = np.random.choice(feedback_nodes, p=probas)
        return select(chosen_feedback_node)

    return chosen_guess_node


def backpropagate(node, total_moves):
    while node is not None:
        node.update(total_moves)
        node = node.parent




def mcts_training(node, num_iterations, parameters):

    for i in range(num_iterations+1):
        if i % 10 == 0:
            bluelog(f"\nITERATION {i}/{num_iterations}")
        guess_node = select(node)
        if guess_node.is_terminal():
            total_moves = guess_node.moves

        else:
            guess_node.expand()
            total_moves = guess_node.simulate()
        backpropagate(guess_node, total_moves)
    return node

def show_f(node_f, depth=1):
    print(f"{'  ' * depth}{node_f} ({node_f.visits} visits, frequency:{node_f.frequency})")
    for child in node_f.children:
        show_g(child, depth + 1)

def show_g(node_g, depth=1):
    print(f"{'  ' * depth}{node_g} ({node_g.visits} visits, {node_g.total_moves} total_moves)")
    for child in node_g.children:
        show_f(child, depth + 1)

parameters = {
    "code_length": 2,
    "num_colors": 3
}
root = FeedbackNode(parameters)
mcts_training(root, 10, parameters)


print("\n\n\n")
#show_f(root)
print("\n\n\n")



def play_with_mcts(parameters, root, n):
    def game():
        secret_code = random.choices(range(1, parameters['num_colors'] + 1), k=parameters['code_length'])
        node = root
        while True:
            guess_node = max(node.children, key=lambda guess_node: guess_node.score())
            guess = guess_node.guess
            feedback = evaluate_guess(guess, secret_code)
            print(f"Node children: {guess}, guess: {guess}, feedback: {feedback}")


            if feedback == (parameters["code_length"], 0):
                return guess_node.moves
            if not guess_node.children:
                redlog("RETRAINING")
                mcts_training(guess_node, 100, parameters)

            for child in guess_node.children:
                if child.feedback == feedback:
                    node = child
                    break

    games = []
    for i in range(n):
        print(i)
        games.append(game())
    return games


games = play_with_mcts(parameters, root, 10)
print(statistics.mean(games))


def plot_strategy_performance(games):
    count, bins, ignored = plt.hist(games, bins=range(1, 13), align='left', rwidth=0.8, color='skyblue',
                                    edgecolor='black')

    mean = np.mean(games)
    std = np.std(games)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 300)
    p = norm.pdf(x, mean, std) * len(games) * (bins[1] - bins[0])

    plt.plot(x, p, 'k', linewidth=2)

    title = "Fit results: mean = %.2f,  std = %.2f" % (mean, std)
    plt.title(title)
    plt.xlabel('Attempts')
    plt.ylabel('Frequency')
    plt.show()


plot_strategy_performance(games)

