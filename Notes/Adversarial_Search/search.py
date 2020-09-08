from minimax import minimax_decision

def get_action(gameState, depth_limit):
    best_move = None
    for depth in range(1, depth_limit+1):
        best_move = minimax_decision(gameState, depth)
    return best_move