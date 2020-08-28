import numpy as np
import copy

directions = np.array([[1,0], [-1,0], [0,1], [0,-1], [1,-1], [-1,1], [1,1], [-1,-1]])

class GameState:
    """ A state of Isolation game

    Attributes:
    ----------
        width (int): width of the board
        height (int): height of the board
        board (np.array): a 2D array where True mean a cell is opened and False otherwise
    """
    def __init__(self):
        self.width = 3
        self.height = 2
        self.board = np.ones((self.height, self.width), dtype=np.bool)
        self.board[-1,-1] = False

        # player to make next move
        self._player = 0
        # current position of players on the board. (represent by list of tuples)
        self._player_position = [None, None]
        
    def actions(self):
        """ Return a list of legal actions for the active player 
        
        You are free to choose any convention to represent actions,
        but one option is to represent actions by the (row, column)
        of the endpoint for the token. For example, if your token is
        in (0, 0), and your opponent is in (1, 0) then the legal
        actions could be encoded as (0, 1) and (0, 2).
        """
        return self.liberties(self._player_position[self._player])
    
    def player(self):
        """ Return the id of the active player 
        
        Hint: return 0 for the first player, and 1 for the second player
        """
        return self._player
    
    def result(self, action):
        """ Return a new state that results from applying the given
        action in the current state
        
        Hint: Check out the deepcopy module--do NOT modify the
        objects internal state in place
        """
        new_state = copy.deepcopy(self)
        new_state._player_position[self._player] = action
        new_state._player = 1 - self._player
        new_state.board[action] = False
        return new_state
    
    def terminal_test(self):
        """ return True if the current state is terminal,
        and False otherwise
        
        Hint: an Isolation state is terminal if _either_
        player has no remaining liberties (even if the
        player is not active in the current state)
        """
        return len(self.liberties(self._player_position[0])) == 0 or \
               len(self.liberties(self._player_position[1])) == 0

    def utility(self, player_id):
        if not self.terminal_test():
            return 0

        is_ended = len(self.liberties(self._player_position[self._player])) == 0
        if is_ended:
            return float("-inf") if player_id == self._player else float("inf")
        else:
            return float("inf") if player_id == self._player else float("-inf")

    def liberties(self, loc):
        """ Return a list of all open cells in the
        neighborhood of the specified location.  The list 
        should include all open spaces in a straight line
        along any row, column or diagonal from the current
        position. (Tokens CANNOT move through obstacles
        or blocked squares in queens Isolation.)
        
        Note: if loc is None, then return all empty cells
        on the board
        """
        if loc is None:
            return list(zip(self.board.nonzero()[0], self.board.nonzero()[1]))

        ans = []
        for direction in directions:
            cur = np.array(loc) + direction
            while self._valid_cell(cur):
                ans.append(tuple(cur))
                cur += direction
        return ans
    
    def _valid_cell(self, loc):
        return 0 <= loc[0] < self.height and 0 <= loc[1] < self.width and self.board[tuple(loc)]

