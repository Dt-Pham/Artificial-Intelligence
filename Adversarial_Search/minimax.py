from minimax_helpers import *

def minimax_decision(gameState, depth):
  return max(gameState.actions(), key a: min_value(gameState.result(a), depth))