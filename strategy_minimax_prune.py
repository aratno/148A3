from strategy import Strategy


class StrategyMinimaxPrune(Strategy):
    ''' Interface to suggest moves in a game
    
    Uses pruning minimax algorithm that only expands the game tree as far
    as needed to find the best move
    '''
    
    def suggest_move(self, state):
        ''' (StrategyMinimax, GameState) -> Move 
        
        Use minimax to return the move reaching the best score
        Override Strategy.suggest_move
        '''
        
        move = None
        
        for i in state.possible_next_moves():  # iterate through options
            x = state.apply_move(i)
            score = self.minimax(x, state.LOSE, state.WIN, False)
            
            if score == state.WIN:
            # if winning move is available, stop searching
                return i
            elif score == state.DRAW:
            # elif draw is available, reset move
                move = i
        
        # if all moves are losses, return first available move
        return move if move else state.possible_next_moves()[0]
    
    def minimax(self, state, cur_min=-1, opp_min=1, cur=True):
        ''' (StrategyMinimaxPrune, GameState, int, int, bool) -> float
        
        Return score for the given game state, that is, how favourable the 
        game is for the next_player
        
        If a winning strategy is available, return 1
        Elif a tying strategy is available, return 0
        Else return -1
        
        cur_min: int  -- worst guaranteed score for next_player (maximizer)
        opp_min: int  -- worst guaranteed score for opponent (minimizer)
        
        cur: bool  -- whether the options are for next_player or opponent
        '''
        
        if state.over:  # if over, return outcome for next_player
            return state.outcome() if cur else (-1) * state.outcome()
        elif cur:  # options for next_player
            score = -1  # begin at worst achievable score
            for i in state.possible_next_moves():
                # iterate through moves, reset cur_min and score
                x = state.apply_move(i)
                score = max(score, self.minimax(x, cur_min, opp_min, False))
                cur_min = max(score, cur_min)
                
                # if cur_min is better than opp_min, stop searching
                if cur_min >= opp_min:
                    break
            return score
        else:  # options for opponent
            score = 1  # begin at worst achievable score (for opp)
            for i in state.possible_next_moves():
                # iterate through moves, reset opp_min and score
                x = state.apply_move(i)
                score = min(score, self.minimax(x, cur_min, opp_min, True))
                opp_min = min(score, opp_min)
                
                # if opp_min is worse than cur_min, stop searching
                if opp_min <= cur_min:
                    break 
            return score