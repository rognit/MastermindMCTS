import itertools
import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

COLORS = ['brown', 'red', 'orange', 'yellow', 'blue', 'green', 'white', 'black']
NB_PINS = 7
MAX_SAME_COLOR = 3


def generate_secret_code():
    return random.sample(COLORS * MAX_SAME_COLOR, NB_PINS)


def generate_random_guess():
    return random.choices(COLORS, k=NB_PINS)


def evaluate_proposal(guess, secret_code):
    exact = sum([1 for i in range(len(secret_code)) if guess[i] == secret_code[i]])
    return exact, sum([min(guess.count(j), secret_code.count(j)) for j in set(guess)]) - exact


def update_possible_codes(possible_codes, last_proposal, black_pins, white_pins):
    return [code for code in possible_codes if evaluate_proposal(last_proposal, code) == (black_pins, white_pins)]


def partie(strat, log=True):
    secret_code = generate_secret_code()

    # We create all possible combinations (8^5 = 32768) without the MAX_SAME_COLOR constraint, then filter according
    # to this constraint.
    all_combinations = list(itertools.product(COLORS, repeat=NB_PINS))
    possible_codes = [combo for combo in all_combinations if
                      all(combo.count(color) <= MAX_SAME_COLOR for color in COLORS)]

    attempts = 0
    while True:
        attempts += 1

        proposal = strat(possible_codes)

        black_pins, white_pins = evaluate_proposal(proposal, secret_code)

        if log:
            print(f"\nOnly {len(possible_codes)} possible codes left.")
            print(f"Attempt {attempts}: {proposal}")
            print(f"Result : {black_pins} black pins, {white_pins} white pins.")

        if black_pins == NB_PINS:
            if log:
                print("The bot has found the secret code!")
            break

        possible_codes = update_possible_codes(possible_codes, proposal, black_pins, white_pins)
    return attempts


def strategy0(possible_codes):
    return random.choice(possible_codes)


def strategy1(possible_codes):
    # We will choose the proposal that will eliminate the most possible codes
    max_elimination = 0
    best_proposal = None
    for proposal in possible_codes:
        elimination = 0
        for code in possible_codes:
            if evaluate_proposal(proposal, code) == (0, 0):
                elimination += 1
        if elimination > max_elimination:
            max_elimination = elimination
            best_proposal = proposal
    return best_proposal


def evaluate(strat, n_games):
    attempts_list = []
    for i in range(n_games):
        if i % 1 == 0:
            print(f"{round(100 * i / n_games)} % (Game {i})")
        attempts = partie(strat, log=False)
        attempts_list.append(attempts)
    return attempts_list


def plot_strategy_performance(strat, n_games=10):

    attempts = evaluate(strat, n_games)

    count, bins, ignored = plt.hist(attempts, bins=range(1, 13), align='left', rwidth=0.8, color='skyblue', edgecolor='black')

    mean = np.mean(attempts)
    std = np.std(attempts)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 300)
    p = norm.pdf(x, mean, std) * len(attempts) * (bins[1] - bins[0])

    plt.plot(x, p, 'k', linewidth=2)

    title = "Fit results: mean = %.2f,  std = %.2f" % (mean, std)
    plt.title(title)
    plt.xlabel('Attempts')
    plt.ylabel('Frequency')
    plt.show()


plot_strategy_performance(strategy0, n_games=3)


def help():
    all_combinations = list(itertools.product(COLORS, repeat=NB_PINS))
    possible_codes = [combo for combo in all_combinations if
                      all(combo.count(color) <= MAX_SAME_COLOR for color in COLORS)]

    while True:
        if len(possible_codes) < 10:
            print(possible_codes)
        proposal = random.choice(possible_codes)
        print(proposal)
        black_pins = int(input("black : "))
        white_pins = int(input("white : "))
        possible_codes = update_possible_codes(possible_codes, proposal, black_pins, white_pins)
        print(len(possible_codes))
        print('')


#help()