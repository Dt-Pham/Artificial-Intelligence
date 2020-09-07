import random
import math
from sample_players import DataPlayer
from isolation import DebugState

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            alphabeta = AlphaBetaPruning(state, self.queue)
            alphabeta.best_action()
            # mcts = MCTSSearch(state, self.queue)
            # mcts.best_action()

class MCTSSearch:
    def __init__(self, state, queue):
        self.root = MCTSNode(state)
        self.queue = queue

    def best_action(self):
        for i in range(900):
            node = self._tree_policy()
            result = node.simulate()
            node.backpropagate(result)
            if i%10==0:
                self.queue.put(self.root.best_action())
        return self.root.best_action()

    def _tree_policy(self):
        node = self.root
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.best_child()
        return node

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.actions = []
        self._results = [0, 0]
        self._untried_actions = None
        self._visit_cnt = 0

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.actions()
        return self._untried_actions
    
    @property
    def value(self):
        wins = self._results[self.state.player()^1]
        loses = self._results[self.state.player()]
        return wins - loses
    
    @property
    def n(self):
        return self._visit_cnt

    def is_terminal(self):
        return self.state.terminal_test()

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c = 1.4):
        return max(self.children, key=lambda x: x.value/x.n + c*math.sqrt(math.log(self.n)/x.n))
    
    def best_action(self):
        if len(self.actions) == 0:
            return random.choice(self.state.actions())
        idx = max(list(range(len(self.actions))), key=lambda i: self.children[i].value/self.children[i].n)
        return self.actions[idx]

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.result(action)
        child_node = MCTSNode(next_state, self)
        self.children.append(child_node)
        self.actions.append(action)
        return child_node

    def simulate(self):
        current_state = self.state
        while not current_state.terminal_test():
            action = random.choice(current_state.actions())
            current_state = current_state.result(action)
        return 0 if current_state.utility(0) > 0 else 1

    def backpropagate(self, result):
        self._visit_cnt += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

class AlphaBetaPruning:
    def __init__(self, state, queue):
        self.state = state
        self.player_id = state.player()
        self.queue = queue

    def best_action(self):
        for depth in range(2, 100):
            alpha = float("-inf")
            beta = float("inf")
            best_score = float("-inf")
            best_move = None
            for action in self.state.actions():
                val = self.min_value(self.state.result(action), alpha, beta, depth - 1)
                alpha = max(val, alpha)
                if val > best_score:
                    best_score = val
                    best_move = action
            if best_move is None:
                best_move = self.state.actions()[0]
            self.queue.put(best_move)

    def min_value(self, state, alpha, beta, depth):
        if state.terminal_test(): return state.utility(self.player_id)
        if depth <= 0: return self.score(state)
        value = float("inf")
        for action in state.actions():
            value = min(value, self.max_value(state.result(action), alpha, beta, depth - 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def max_value(self, state, alpha, beta, depth):
        if state.terminal_test(): return state.utility(self.player_id)
        if depth <= 0: return self.score(state)
        value = float("-inf")
        for action in state.actions():
            value = max(value, self.min_value(state.result(action), alpha, beta, depth - 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value


    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
