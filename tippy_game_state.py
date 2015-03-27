from game_state import GameState
from tippy_move import TippyMove
from math import sqrt
from random import randint
from copy import deepcopy


class TippyGameState(GameState):
    ''' The state of the Tippy game
    
    current_state: list   --- n x n array of current board
    '''
    
    PLAYER = {'p1': 'X', 'p2': 'O'}
    
    def __init__(self, p, interactive=False,
                 current_state=[[' ' for i in range(3)] for i in range(3)]):
        ''' (TippyGameState, str, list) -> Nonetype
        
        Initialize TippyGameState self with current_state as the n x n grid.
        
        Assume:   p in {'p1','p2'}
                  current_state is a square list of lists
                  len(current_state) > 2 so the game can be won
        '''
        
        if interactive:
            size = int(input('Enter the size of your grid: '))
            while size < 3:
                size = int(input('Size must be at least 3. Try again: '))
            current_state = [[' ' for i in range(size)] for i in range(size)]
            
        GameState.__init__(self, p)
        self.current_state = current_state
        self.over = (self.winner('p1') or self.winner('p2') or not 
                     self.possible_next_moves())
        self.instructions = ('Enter the row number and then the column ' 
                             'number of the location where you wish to '
                             'make your move. The objective is to make '
                             'a tippy.')
        
    def __repr__(self):
        ''' (TippyGameState) -> str
        
        Return a string representation of TippyGameState self that evaluates 
        to  an equivalent TippyGameState.
        
        >>> t = TippyGameState('p1')
        >>> t
        TippyGameState('p1', [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']])
        '''
        
        return 'TippyGameState({}, {})'.format(repr(self.next_player),
                                               repr(self.current_state))
    
    def __str__(self):
        ''' (TippyGameState) -> str
        
        Return a convenient string representation of TippyGameState self.
        
        >>> t = TippyGameState('p1')
        >>> print(t)
        Current board:
         | | 
        -----
         | | 
        -----
         | | 
        <BLANKLINE>
        Next to play: p1
        '''
        
        size = len(self.current_state)  # assign variable to shorten lines
        grid = ''
        for i in range(size):  # iterate through rows
            for j in range(size):  # print row with vertical bars
                grid += self.current_state[i][j]
                if j != size - 1:
                    grid += '|'
            
            grid += '\n'
            if i != size - 1: 
                for k in range(2 * size - 1):  # print line in between rows
                    grid += '-'
                grid += '\n'
                
        return 'Current board:\n{}\nNext to play: {}'.format(
            grid, self.next_player)
    
    def __eq__(self, other):
        ''' (TippyGameState, TippyGameState) -> bool

        Return True iff this TippyGameState is the equivalent to other.

        >>> s1 = TippyGameState('p1')
        >>> s2 = TippyGameState('p1')
        >>> s1 == s2
        True
        '''
        
        return (isinstance(other, TippyGameState) and
                self.current_state == other.current_state and
                self.next_player == other.next_player)
    
    def apply_move(self, move):
        ''' (TippyGameState, TippyMove) -> TippyGameState

        Return the new TippyGameState reached by applying move to self.
        
        >>> s1 = TippyGameState('p1')
        >>> s2 = s1.apply_move(TippyMove([1, 1]))
        >>> print(s2)
        Current board:
        X| | 
        -----
         | | 
        -----
         | | 
        <BLANKLINE>
        Next to play: p2
        '''
        
        if move in self.possible_next_moves():
            new_state = deepcopy(self.current_state)
            if self.next_player == 'p1':
                new_state[move.pos[0]][move.pos[1]] = 'X'                
            else:
                new_state[move.pos[0]][move.pos[1]] = 'O'
            return TippyGameState(self.opponent(), False, new_state)
        else:
            return None
            
    def get_move(self):
        ''' (TippyGameState) -> TippyMove

        Prompt user and return move.
        '''
        
        move = []
        #first row or column taken as 1, then corrected in TippyMove
        size = len(self.current_state)
        
        move.append(int(input('Enter the row (1 to {}): '.format(size))))
        move.append(int(input('Enter the column (1 to {}): '.format(size))))
        
        return TippyMove(move)
    
    def possible_next_moves(self):
        ''' (TippyGameState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal from the 
        present state.
        
        >>> s1 = TippyGameState('p1')
        >>> s2 = s1.apply_move(TippyMove([1,1]))
        >>> s2.possible_next_moves()
        [TippyMove([1, 2]), TippyMove([1, 3]), TippyMove([2, 1]), TippyMove([2, 2]), TippyMove([2, 3]), TippyMove([3, 1]), TippyMove([3, 2]), TippyMove([3, 3])]
        '''
        
        moves = []
        if not (self.winner('p1') or self.winner('p2')):
            for i in range(len(self.current_state)):
                for j in range(len(self.current_state)):
                    if self.current_state[i][j] == ' ':
                        moves.append(TippyMove([i + 1, j + 1]))
                        # the TippyMove representation starts at 1
        
        return moves
    
    def winner(self, player):
        ''' (TippyGameState, str) -> bool
        
        Return True iff a tippy has been formed in self and player has won.
        
        >>> s1 = TippyGameState('p1')
        >>> s2 = s1.apply_move(TippyMove([1,1]))
        >>> s2.winner('p1')
        False
        
        Precondition: player is either 'p1' or 'p2'
        '''
        
        win = False
        
        i = 0        
        while not win and i < len(self.current_state):
            #iterate through rows
            j = 0
            while not win and j < len(self.current_state):
                #iterate through columns
                win = find_tippy(self.current_state,
                                 TippyGameState.PLAYER[player], [i, j])
                #determine if tippy has been formed at this position
                j += 1
            i += 1
        return win
    
    def rough_outcome(self):
        ''' (TippyGamestate) -> float
        
        Return an estimate in interval [LOSE,WIN] of best outcome next_player
        can obtain from state self, by finding how many moves result in wins
        and losses. If game is over, return 0.0.
        
        >>> s1 = TippyGameState('p1')
        >>> s2 = s1.apply_move(TippyMove([1,1]))
        >>> s2.rough_outcome()
        0.0
        '''
        
        new_states = [self.apply_move(i) for i in self.possible_next_moves()]
        #run through all options (for next_player) and produce new states
        win_outcome = [i.winner(self.next_player) for i in new_states]
        #determine which of these are winning states (for next_player)
        
        opp = TippyGameState(self.opponent(), False, self.current_state)
        #create new state with the opponent next to play
        new_opp = [opp.apply_move(i) for i in opp.possible_next_moves()]
        #run through all options (for opponent) and produce new states
        opp_outcome = [i.winner(opp.next_player) for i in new_opp]
        #determine which of these are losing states (for next_player)
        
        wins = float(len([i for i in win_outcome if i]))
        losses = float(len([i for i in opp_outcome if i]))
        
        try:
            num = 2 * wins / (wins + losses) - 1
            #scale value into [LOSE, WIN]
        except ZeroDivisionError:
            num = 0.0
        
        return num  


def find_tippy(state, sym, pos):
    ''' (list, str, list) -> bool
    
    Return True if a tippy made up of letter sym has been formed in state
    starting at position pos.
    Helper function for TippyGameState.winner().
    
    >>> s1 = TippyGameState('p1')
    >>> temp = deepcopy(s1.current_state)
    >>> temp[0][0] = 'X'
    >>> temp[0][1] = 'X'
    >>> temp[1][1] = 'X'
    >>> temp[1][2] = 'X'
    >>> find_tippy(temp, 'X', [0, 0])
    True
    
    Precondition: sym is either 'X' or 'O'
    '''
    
    x, y = pos[0], pos[1]
    
    tippy = False
    
    #because we are iterating from the top left to the bottom right,
    #there are only four tippy configurations we need to check
    
    if state[x][y] == sym:
        try:  # search for right-rightdown-rightrightdown tippy
            if all([state[x][y + 1] == sym,
                    state[x + 1][y + 1] == sym,
                    state[x + 1][y + 2] == sym]):
                tippy = True
        except IndexError:
            pass
        
        try:  # search for right-down-leftdown tippy       
            if all([state[x][y + 1] == sym,
                    state[x + 1][y] == sym,
                    state[x + 1][y - 1] == sym]):
                tippy = True
        except IndexError:
            pass
        
        try:  # search for down-rightdown-rightdowndown tippy
            if all([state[x + 1][y] == sym,
                    state[x + 1][y + 1] == sym,
                    state[x + 2][y + 1] == sym]):
                tippy = True
        except IndexError:
            pass
        
        try:  # search for down-leftdown-leftdowndown tippy
            if all([state[x + 1][y] == sym,
                    state[x + 1][y - 1] == sym,
                    state[x + 2][y - 1] == sym]):
                tippy = True
        except IndexError:
            pass
    
    return tippy

if __name__ == '__main__':
    import doctest
    doctest.testmod()