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
        next_move = board.get_non_losing_moves()
        if next_move == 0: # No non-losing move means opponent wins next turn
            return -1 * (self.WIDTH * self.HEIGHT - board.num_moves_played) // 2
        
        if (board.num_moves_played >= (self.WIDTH * self.HEIGHT - 2)): # Draw game
            return 0

        minimum = -1 * (self.WIDTH * self.HEIGHT - 2 - board.num_moves_played) // 2
        if a < minimum:
            a = minimum
            if a >= b:
                return a

        maximum = (self.WIDTH * self.HEIGHT - 1 - board.num_moves_played) // 2
        if board.get_key() in self.move_table: # Check if we've seen this board position before
            move_value = self.move_table[board.get_key()]
            maximum = move_value + board.MIN_SCORE - 1

        if b > maximum:
            b = maximum
            if a >= b:
                return b
        
        move_getter = MoveGetter()

        for i in range(self.WIDTH - 1, -1, -1):
            col = self.column_ordering[i]
            move = next_move & board.get_column_mask(col)
            if move != 0:
                move_getter.add_to_best_moves(move, board.get_num_winning_spots(move), col)

        next_move = None
        while True:
            next_move, next_move_col = move_getter.get_next_best_move()
            #if next_move <= 6:
                #print("Got next best move: ", str(next_move))
            #print("Best moves list size: ", str(move_getter.move_list_size))
            if next_move == 0:
                break   
            temp_board = deepcopy(board)
            temp_board.play(next_move)
            temp_score = -1 * self.score(temp_board, -1 * b, -1 * a)
            if temp_score >= b:
                self.best_move = next_move_col
                return temp_score
            if temp_score > a:
                a = temp_score
                self.best_move = next_move_col
        self.move_table[board.get_key()] = a - board.MIN_SCORE + 1
        return a

class MoveGetter:
    def __init__(self):
        self.move_list = []
        self.move_list_size = 0

    def add_to_best_moves(self, move, score, col):
        self.move_list.append((move, score, col))
        self.move_list_size += 1
        if self.move_list_size > 1:
            self.move_list.sort(key = lambda x: x[1], reverse=True)

    def get_next_best_move(self):
        if(self.move_list_size > 0):
            best_move_tuple = self.move_list.pop(0)
            self.move_list_size -= 1
            return (best_move_tuple[0], best_move_tuple[2])
        else:
            return (0, 0)