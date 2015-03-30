from move import Move


class TippyMove(Move):
    ''' A move in the game of Tippy.
    
    pos: list -- list denoting the row and column of the move on the grid.
    '''
    
    def __init__(self, pos):
        ''' (TippyMove, list) -> NoneType
    
        Initialize a new TippyMove for inserting 'X' or 'O' on the grid.

        Assume: pos is a list with integer values 
        '''
        
        self.pos = [pos[0] - 1, pos[1] - 1]
        #user will enter number from 1 to n
        
    def __repr__(self):
        ''' (TippyMove) -> str
        
        Return the string representation of this TippyMove.
        
        >>> p = TippyMove([1, 1])
        >>> p 
        TippyMove([1, 1])
        '''
        return 'TippyMove([{}, {}])'.format(str(self.pos[0] + 1), 
                                            str(self.pos[1] + 1))
        
    def __str__(self):
        ''' (TippyMove) -> str
        
        Returns the string representation of this TippyMove that is readable.
        
        >>> p = TippyMove([1, 1])
        >>> print(p) 
        Row: 1  Column: 1
        '''
        return 'Row: {}  Column: {}'.format(self.pos[0] + 1, self.pos[1] + 1) 
    
    def __eq__(self, other):
        ''' (TippyMove, TippyMove) -> bool

        Return True iff this TippyMove is the same as other.

        >>> m1 = TippyMove([1, 2])
        >>> m2 = TippyMove([2, 1])
        >>> print(m1 == m2)
        False
        >>> m3 = TippyMove([1, 2])
        >>> print(m1 == m3)
        True
        '''
        return (isinstance(other, TippyMove) and 
                self.pos == other.pos)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()