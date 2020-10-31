import math

class Play:
    mask = '' # Bit mask containing positions of non-empty cells
    #def __init__(self, other=None):
    
    def is_column_free(self, col: int) -> bool:
        mask_int = int(self.mask, 2)
        top_mask = self.get_top_mask(col)
        return ((mask_int & top_mask) == 0)

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << 5)  << column * 7
        # print(format(top_mask, 'b'))
        return top_mask

    #def __mtdf():

    """ def __minimax_ab(self, board, depth, a, b, maxPlayer):
        # Include function to get valid plays 
        # Include check here for if depth is 0 or if it's a game-terminating depth
    
        if maxPlayer: # This is the case for the maximizing player

        else: # This is the case for the minimizing player """



""" class Board:
    def __init__(self, other=None): """
