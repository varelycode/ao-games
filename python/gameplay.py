import math
import functools
from copy import deepcopy

HEIGHT = 6
WIDTH = 7
ROWS = 6
COLS = 7

class Play:
    mask = '' # Bit mask containing positions of non-empty cells
    num_moves_played = 0 # Number of moves played since beginning of game
    column_ordering = [] # Order to look at columns in, since columns closer to the center are involved in more 4-alignments

    def is_column_free(self, col: int) -> bool:
        mask_int = int(self.mask, 2)
        top_mask = self.get_top_mask(col)
        return ((mask_int & top_mask) == 0)

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << (HEIGHT - 1))  << (column * WIDTH)
        # print(format(top_mask, 'b'))
        return top_mask

    def check_wins(self, board, player_num) -> bool:
        #horizontal
        for i in range(COLS - 3):
            for j in range(ROWS):
                if board[j][i] == player_num and board[j][i+1] == player_num and board[j][i+2] == player_num and board[j][i+3] == player_num:
                    return True
        #vertical
        for i in range(COLS):
            for j in range(ROWS - 3):
                if board[j][i] == player_num and board[j + 1][i] == player_num and board[j + 1][i] == player_num and board[j + 1][i] == player_num:
                    return True
        # ascending diagnols
        for i in range(COLS - 3):
            for j in range(ROWS - 3):
                if board[j][i] == player_num and board[j + 1][i + 1] == player_num and board[j + 2][i + 1] == player_num and board[j + 3][i + 1] == player_num:
                    return True
        # descending diagnols
        for i in range(COLS - 3):
            for j in range(ROWS - 3):
                if board[j][i] == player_num and board[j - 1][i + 1] == player_num and board[j - 2][i + 2] == player_num and board[j - 3][i + 3] == player_num:
                    return True
        return False

    def get_opp_num(self, player_num) -> int:
        opp = set()
        opp.add(2)
        opp.add(1)
        opp.discard(player_num) #remove the number that reps the player from set
        opposite = opp.pop()
        return opposite
