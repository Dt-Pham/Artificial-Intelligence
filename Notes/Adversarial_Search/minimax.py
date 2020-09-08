player_id = 0

def my_moves(gameState):
    return len(gameState.actions())

def minimax_decision(gameState, depth):
    return max(gameState.actions(), key = lambda a: min_value(gameState.result(a), depth-1))

def min_value(gameState, depth):
    """ Return the game state utility if the game is over,
    otherwise return the minimum value over all legal successors
    """
    if gameState.terminal_test(): return gameState.utility(0)
    if depth == 0: return my_moves(gameState)
    return min(max_value(gameState.result(a), depth-1) for a in gameState.actions())

def max_value(gameState, depth):
    """ Return the game state utility if the game is over,
    otherwise return the maximum value over all legal successors
    """
    if gameState.terminal_test(): return gameState.utility(0)
    if depth == 0: return my_moves(gameState)
    return max(min_value(gameState.result(a), depth-1) for a in gameState.actions())
