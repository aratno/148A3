from strategy import Strategy

class StrategyMinimaxMemoize(Strategy):
    ''' minimax strategy '''
    
    states_data = {}
    
    def __init__(self, interactive=False):
        ''' (StrategyMinimaxMemoize) -> None
        
        Initialize a minimax memoize strategy
        '''
        
        StrategyMinimaxMemoize.states_data = {}
    
    def suggest_move(self, state):
        ''' (StrategyMinimaxMemoize, GameState) -> Move 
        
        Use minimax to return the move reaching the best score
        Override Strategy.suggest_move
        '''
        
        return self.minimax(state)[1]
    
    def minimax(self, state):
        ''' (StrategyMinimaxMemoize, GameState) -> (int, Move)
        
        Suggest a move using result method
        Return the best score and the move that achieves it
        '''
        
        # make a list of options
        moves = state.possible_next_moves()
        
        # find opponent's score for each option, multiply by (-1)
        scores = [(-1)*self.result(state.apply_move(i)) 
                  for i in state.possible_next_moves()]
        
        # find the maximum score available
        score = max(scores)
        
        return (score, moves[scores.index(score)])
    
    def result(self, state):
        ''' (StrategyMinimax, GameState) -> int
        
        Return score for the given game state – how favourable the game is
        for the next_player
        
        If a winning strategy is available, return 1
        Elif a tying strategy is available, return 0
        Else return -1
        '''
        
        if repr(state) in StrategyMinimaxMemoize.states_data:
            # if game is known, return value from dictionary
            return StrategyMinimaxMemoize.states_data[repr(state)]            
        elif state.over:
            # if game is over, return outcome, assign value to dictionary
            StrategyMinimaxMemoize.states_data[repr(state)] = state.outcome()
            return state.outcome()
        else:
            # if game is not over, run through all possible_next_moves
            states = [state.apply_move(i) 
                      for i in state.possible_next_moves()]
            
            # for each new hypothetical state, find (-1)*result
            # multiplied by (-1) since result is opponent's score
            scores = [(-1)*self.result(i) for i in states]
            
            # return the maximum of the scores for each result
            # assign this value to dictionary
            StrategyMinimaxMemoize.states_data[repr(state)] = max(scores)
            return max(scores)