import math
import functools
from copy import deepcopy

HEIGHT = 6
WIDTH = 7

class Play:
    mask = '' # Bit mask containing positions of non-empty cells
    num_moves_played = 0 # Number of moves played since beginning of game
    column_ordering = [] # Order to look at columns in, since columns closer to the center are involved in more 4-alignments

    # def __init__(self, other=None):
    #     for i in range(WIDTH): # Populate column ordering list, starting in center cols and moving outwards
    #         self.column_ordering[i] = (WIDTH / 2) + (1 - 2 * (i % 2)) * (i + 1) / 2

    def is_column_free(self, col: int) -> bool:
        mask_int = int(self.mask, 2)
        top_mask = self.get_top_mask(col)
        return ((mask_int & top_mask) == 0)

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << (HEIGHT - 1))  << (column * WIDTH)
        # print(format(top_mask, 'b'))
        return top_mask

    #def __mtdf():
    def check_wins(self, board, player_num) -> bool:
        #horizontal
        for i in range(ROW - 3):
            for j in range(COLS):
                if board[j][i] == player_num and board[j][i+1] == player_num and board[j][i+2] == player_num and board[j][i+3] == player_num:
                    return True
        #vertical
        for i in range(COLS - 3):
            for j in range(ROWS):
                if board[i][j] == player_num and board[i][j+1] == player_num and board[i][j+2] == player_num and board[i][j+3] == player_num:
                    return True
        # ascending diagnols
        for i in range(COLS - 3):
            for j in range(ROWS - 3):
                if board[j][i] == player_num and board[j + 1][i] == player_num and board[j+2][i] == player_num and board[j+3][i] == player_num:
                    return True
        # descending diagnols
        for i in range(COLS - 3):
            for j in range(ROWS - 3):
                if board[j][i] == player_num and board[j - 1][i + 1] == player_num and board[j - 2][i + 2] == player_num and board[j + 3][i + 3] == player_num:
                    return True
        return False

    def get_opp_num(self, player_num) -> int:
        opp = set()
        opp.add(2)
        opp.add(1)
        opp.remove(player_num) # remove the number that reps the player from set
        opposite = opp.pop()
        return opposite

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
