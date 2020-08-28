import minimax_helpers
from gamestate import *

def main():
    g = GameState()
    inf = float("inf")
    actions = [((0, 0), inf), ((0, 1), -inf), ((0, 2), inf), ((1, 0), inf), ((1, 1), -inf)]

    for a, _ in actions:
        print(minimax_helpers.min_value(g.result(a)))

    if all(minimax_helpers.min_value(g.result(a)) == ev for a, ev in actions):
        print("Looks like everything works!")
    else:
        print("Uh oh! Not all the scores matched.")

if __name__ == "__main__":
    main()