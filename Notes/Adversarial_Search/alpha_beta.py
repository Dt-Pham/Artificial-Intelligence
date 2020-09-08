def alpha_beta_search(gameState):
    """ Return the move aloong a branch of the game tree that
    has the best possible value. A move is a pair of coordinates
    in (row, column) order corresponding to a legal move for the searching player.
    """
    alpha = float("-inf")
    beta = float("inf")

    best_value = float("-inf")
    best_move = None
    for a in gameState.actions():
        value = min_value(gameState.result(a), alpha, beta)
        if best_value < value:
            best_value = value
            best_move = a
        alpha = max(alpha, best_value)
    return best_move

def min_value(gameState, alpha, beta):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if gameState.terminal_test(): return gameState.utility(0)

    v = float("inf")
    for a in gameState.actions():
        v = min(v, max_value(gameState.result(a), alpha, beta))
        if v <= alpha: return v
        beta = min(beta, v)
    return v

def max_value(gameState, alpha, beta):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal cihld nodes.
    """
    if gameState.terminal_test(): return gameState.utility(0)

    v = float("-inf")
    for a in gameState.actions():
        v = max(v, min_value(gameState.result(a), alpha, beta))
        if v >= beta: return v
        alpha = max(alpha, v)
    return v
