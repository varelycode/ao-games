import math
import functools
from copy import deepcopy

class Play:
    mask = '' # Bit mask containing positions of non-empty cells
    num_moves_played = 0 # Number of moves played since beginning of game
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

    @functools.lru_cache
    def __score(self) -> int:
        # Include function to get valid plays 
        # Include check here for if depth is 0 or if it's a game-terminating depth

        if self.num_moves_played == 42: # Case of a draw
            return 0
        
        for c in range(6):
            if self.is_column_free(c):  # and is winning move
                return (43 - self.num_moves_played) / 2

        score = -42

        for c in range(6):
            # make deep copy of current board
            # play by placing piece in column c
            # temp_score = __score(temp_board)
            """ if temp_score > score:
                score = temp_score """

        return score 
            



""" class Board:
    def __init__(self, other=None): """
