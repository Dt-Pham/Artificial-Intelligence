def min_value(gameState):
    """ Return the game state utility if the game is over,
    otherwise return the minimum value over all legal successors
    """
    if gameState.terminal_test():
        return gameState.utility(0)
    return min(max_value(gameState.result(a)) for a in gameState.actions())

def max_value(gameState):
    """ Return the game state utility if the game is over,
    otherwise return the maximum value over all legal successors
    """
    if gameState.terminal_test():
        return gameState.utility(0)
    return max(min_value(gameState.result(a)) for a in gameState.actions())
