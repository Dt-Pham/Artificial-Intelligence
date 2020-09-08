import random
from collections import defaultdict

from gamestate import GameState
NUM_ROUNDS = 10

def build_table(num_rounds=NUM_ROUNDS):
    win_count = defaultdict(int)
    book = {}
    depth_limit = 1
    gameState = GameState()
    update(gameState, depth_limit, win_count)

    for state in win_count:
        book[state.hashable] = max(state.actions(), key=lambda a : 0 if state.result(a) not in win_count else win_count[state.result(a)])
    return book

def update(gameState, depth, win_count):
    if depth==0:
        for _ in range(NUM_ROUNDS):
            win_count[gameState] += simulate(gameState)
        return win_count[gameState]
    
    for a in gameState.actions():
        win_count[gameState] += update(gameState.result(a), depth-1, win_count)

def simulate(gameState):
    while not gameState.terminal_test():
        gameState = gameState.result(random.choice(gameState.actions()))
    if gameState.utility(0) > 0:
        return 1
    return 0
