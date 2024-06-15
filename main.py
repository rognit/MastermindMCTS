from mastermind import Mastermind
from mcts import MCTS


def main():
    game = Mastermind()
    mcts = MCTS(game)
    best_move_node = mcts.search(100)
    best_move = best_move_node.state[-1]
    print("Best move:", best_move)


if __name__ == "__main__":
    main()
