from strategy import Strategy


class StrategyMinimaxMyopic(Strategy):
    ''' Interface for suggesting moves
    
    Uses myopic minimax algorithm that determines the best move only to
    a limited recursion depth, in this case 5
    '''
    
    def suggest_move(self, state):
        ''' (StrategyMinimax, GameState) -> Move 
        
        Use myopic implementation of minimax to return the move reaching the 
        best score
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
    
    def minimax(self, state, depth=5):
        '''(StrategyMinimax, GameState, int) -> float
        
        Return score for the given game state, that is, how favourable the 
        game is for the next_player
        
        Only expand game tree to a maximum depth of 5
        
        Return a float between -1.0 and 1.0
        '''
        
        if state.over:
            # if game is over, return outcome for next_player
            return state.outcome()
        elif depth == 0:
            # if maximum depth has been reached, return the rough_outcome
            return state.rough_outcome()
        else:
            # if game is not over, run through all possible_next_moves
            states = [state.apply_move(i) for i in 
                      state.possible_next_moves()]
            
            # for each new hypothetical state, find (-1) * score
            # multiplied by (-1) since minimax returns opponent's score
            scores = [(-1) * self.minimax(i, depth - 1) for i in states]
            
            # return the maximum of the scores for each move
            return max(scores)