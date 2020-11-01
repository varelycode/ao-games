import math
import functools
import boards
from copy import deepcopy

class Play:
    HEIGHT: int = 6
    WIDTH: int = 7
    move_table = {}
    #mask = '' # Bit mask containing positions of non-empty cells
    num_moves_played = 0 # Number of moves played since beginning of game
    column_ordering = [3, 2, 4, 1, 5, 0, 6] # Order to look at columns in, since columns closer to the center are involved in more 4-alignments

    def __init__(self):
        self.best_move = 3

    #def __mtdf():
    @functools.lru_cache
    def iterate(self, board) -> int:
        minimum = -1 * (self.WIDTH * self.HEIGHT - board.num_moves_played) // 2
        maximum = (self.WIDTH * self.HEIGHT + 1 - board.num_moves_played) // 2
        it = 0
        while minimum < maximum:
            it += 1
            print("Iteration ", it)
            print("Max: " + str(maximum) + ", Min: " + str(minimum))
            median = minimum + (maximum - minimum) // 2
            if (median <= 0) and (minimum // 2 < median):
                median = minimum // 2
            elif (median >= 0) and (maximum // 2 > median):
                median = maximum // 2

            iteration_score = self.score(board, median, median + 1)
            if iteration_score <= median:
                maximum = iteration_score
            else:
                minimum = iteration_score
        
        return self.best_move

    @functools.lru_cache
    def score(self, board, a, b) -> int:
        # Include function to get valid plays 
        # Include check here for if depth is 0 or if it's a game-terminating depth

        if board.num_moves_played == self.WIDTH * self.HEIGHT: # Case of a draw
            return 0
        
        for c in range(self.WIDTH):
            if board.is_column_free(c) and board.is_winning_move(c):
                self.best_move = c
                return ((self.WIDTH * self.HEIGHT + 1 - board.num_moves_played) // 2)

        maximum = (self.WIDTH * self.HEIGHT - 1 - board.num_moves_played) // 2
        if board.get_key() in self.move_table: # Check if we've seen this board position before
            move_value = self.move_table[board.get_key()]
            maximum = move_value + board.MIN_SCORE - 1
        
        if b > maximum:
            b = maximum
            if a >= b:
                return b

        for col_to_play in self.column_ordering:
            if board.is_column_free(col_to_play):
                #board.last_col_played = c
                temp_board = deepcopy(board)
                temp_board.play_column(col_to_play)
                temp_score = -1 * self.score(temp_board, -1 * b, -1 * a)
                if temp_score >= b:
                    return temp_score
                if temp_score > a:
                    a = temp_score
        self.move_table[board.get_key()] = a - board.MIN_SCORE + 1
        #print(a)
        return a
