from strategy import Strategy


class StrategyMinimaxMemoize(Strategy):
    ''' Interface for suggesting moves
    
    Uses memoizing minimax algorithm that stores scores of GameStates in a
    dictionary to avoid redunancies in expanding the game tree
    
    DATA: dict  -- dictionary storing scores of GameStates
    '''
    
    DATA = {}
    
    def __init__(self, interactive=False):
        ''' (StrategyMinimaxMemoize, bool) -> None
        
        Initialize a minimax memoize strategy
        '''
        
        # empty the dictionary to avoid overlap of memory between games
        StrategyMinimaxMemoize.DATA = {}
    
    def suggest_move(self, state):
        ''' (StrategyMinimaxMemoize, GameState) -> Move 
        
        Use minimax to return the move reaching the best score
        Override Strategy.suggest_move
        '''
        
        # make a list of options
        moves = state.possible_next_moves()
        
        # find opponent's score for each option, multiply by (-1)
        scores = [(-1) * self.minimax(state.apply_move(i)) 
                  for i in state.possible_next_moves()]
        
        # find the maximum score available
        score = max(scores)
        
        return moves[scores.index(score)]
    
    def minimax(self, state):
        ''' (StrategyMinimax, GameState) -> float
        
        Return score for the given game state, that is, how favourable the 
        game is for the next_player
        
        If a winning strategy is available, return 1
        Elif a tying strategy is available, return 0
        Else return -1
        
        While game tree is traversed, store scores for GameStates in DATA 
        '''
        
        if repr(state) in StrategyMinimaxMemoize.DATA:
            # if game is known, return value from dictionary
            return StrategyMinimaxMemoize.DATA[repr(state)]            
        elif state.over:
            # if game is over, return outcome, assign value to dictionary
            StrategyMinimaxMemoize.DATA[repr(state)] = state.outcome()
            return state.outcome()
        else:
            # if game is not over, run through all possible_next_moves
            states = [state.apply_move(i) 
                      for i in state.possible_next_moves()]
            
            # for each new hypothetical state, find (-1) * score
            # multiplied by (-1) since miminax returns opponent's score
            scores = [(-1) * self.minimax(i) for i in states]
            
            # return the maximum of the scores for each move
            # assign this value to dictionary
            StrategyMinimaxMemoize.DATA[repr(state)] = max(scores)
            return max(scores)