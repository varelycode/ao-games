import math
import functools
from copy import deepcopy

HEIGHT = 6
WIDTH = 7

class Play:
    mask = '' # Bit mask containing positions of non-empty cells
    num_moves_played = 0 # Number of moves played since beginning of game
    column_ordering = [] # Order to look at columns in, since columns closer to the center are involved in more 4-alignments

    def __init__(self, other=None):
        for i in range(WIDTH): # Populate column ordering list, starting in center cols and moving outwards
            self.column_ordering[i] = (WIDTH / 2) + (1 - 2 * (i % 2)) * (i + 1) / 2

    def is_column_free(self, col: int) -> bool:
        mask_int = int(self.mask, 2)
        top_mask = self.get_top_mask(col)
        return ((mask_int & top_mask) == 0)

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << (HEIGHT - 1))  << (column * WIDTH)
        # print(format(top_mask, 'b'))
        return top_mask

    #def __mtdf():

    @functools.lru_cache
    def __score(self) -> int:
        # Include function to get valid plays 
        # Include check here for if depth is 0 or if it's a game-terminating depth

        if self.num_moves_played == WIDTH * HEIGHT: # Case of a draw
            return 0
        
        for c in range(WIDTH):
            if self.is_column_free(c):  # and is winning move
                return ((WIDTH * HEIGHT + 1) - self.num_moves_played) / 2

        score = -1 * WIDTH * HEIGHT

        for c in range(WIDTH):
            col_to_play = self.column_ordering[c]
            # make deep copy of current board
            # play by placing piece in column c
            # temp_score = __score(temp_board)
            """ if temp_score > score:
                score = temp_score """

        return score 
            



""" class Board:
    def __init__(self, other=None): """
