import math
import boards
import gameplay
from copy import deepcopy
import numpy as np

TOTAL_SPACES = 7 * 6
spaces_available = 42
score = 0
ROWS = 6
COLS = 7

def get_best_move(board, player_num):
    best_move = 0
    best_score = -math.inf

    for i in range((len(board) - 1)):  #cols
        row = find_row_pos(board, i) # find next avail. position given a col
        if row >= 0:
            if board[row][i] == 0:
                new_board = deepcopy(board)
                new_board[row][i] = player_num
                score = min_max(new_board, 5, player_num, True)
                if score > best_score:
                    best_score = score
                    best_move = i

    return {'column': best_move}

def free_row(row) -> bool:
    for space in row:
        if space != 1 or space != 2:
            return True
    return False

def find_row_pos(board, col) -> int:
    end = 5
    while end >= 0:
        if board[end][col] == 0:
            return end
        end -= 1
    return -1 # no available spaces


def check_top_row(top_row) -> []:
    valid_cols = []
    for i, item in enumerate(top_row):
        if item == 0:
            valid_cols.append(i)
    return valid_cols

def valid_moves(board) -> []:
    # Check the top row. If top row not full, can still insert piece there
    valid_cols = check_top_row(board[0])
    return valid_cols

def terminal_node(board, player_num) -> bool:
    p = gameplay.Play()
    opp = p.get_opp_num(player_num)
    b = boards.Board()
    is_full = b.is_full(board)
    if p.check_wins(board, player_num):
        return True
    elif p.check_wins(board, opp):
        return True
    elif is_full:
        return True
    return False


def potential_win(connect, player_num) -> bool:
    count = 0
    for i, item in enumerate(connect):
        if item == 0:
            connect[i] = player_num
            count += 1
        if item == 1:
            count += 1
    if count == 4:
        return True
    return False

def column(board, i):
    return [row[i] for row in board]

def diag_check(board, r, c) -> []:
    l = np.array(board)
    major = np.diagonal(board, offset=(c - r))

    minor = np.diagonal(np.rot90(l), offset=-l.shape[1] + (c + r) + 1)
    return major, minor
def diag_count(major: [], minor: [], player_num) -> int:
    use_major = True
    use_minor = True
    minor_count = -1
    major_count = -1
    count = 0
    p = gameplay.Play()
    opp = p.get_opp_num(player_num)
    if len(major) != 4:
        use_major = False
    if len(minor) != 4:
        use_minor = False
    if use_major:
        for i, item in enumerate(major):
            if item == 0 or item == player_num:
                count += 1
            elif item == opp:
                if count > major_count:
                    major_count = count
                count = 0
    count = 0
    if use_minor:
        for i, item in enumerate(minor):
            if item == 0 or item == player_num:
                count += 1
            elif item == opp:
                if count > minor_count:
                    minor_count = count
                count = 0

    return major_count, minor_count




def score(board, player_num) -> bool:
    """
    This function takes the score of a board. This is called at depth = 0
    """
    # horizontal
    count = 0
    h_max_count = 0
    for i in range(ROWS):
        for j in range(COLS):
            if potential_win(board[i]): # make sure its possible to win before u keep track of count
                if board[i][j] == player_num:
                    count += 1
                    if count > h_max_count:
                        h_max_count = count
                else:
                    count = 0
    # vertical
    v_max_count = 0
    for i in range(COLS):
        winnable = potential_win(column(board, i), player_num) #ensure this column is winnable
        for j in range(ROWS):
            if winnable:
                if board[j][i] == player_num:
                    count += 1
                    if count > v_max_count:
                        v_max_count = count
                else:
                    count = 0

    max_major = 0 #diagnol from bottom right to top left
    max_minor = 0 #diagnol from bottom left to right
    end = ROWS - 1
    for i in range(COLS):
        for j in range(ROWS):
            major, minor = diag_check(board, r, c)
            major_count, minor_count = diag_count(major, minor, player_num)
            if major_count > max_major:
                max_major = major_count
            if minor_count > max_minor:
                max_minor   = minor_count
            end -= 1




def child_board(board: [[]], player_num: int, move: int) -> [[]]:
    end = len(board) - 1
    new_board = deepcopy(board)
    for i, row in enumerate(board):
        #start at the end of the board, we know what col we are placing it in
        if board[end][move] == 0:
            new_board[end][move] = player_num
        end -= 1
    return new_board


def min_max(board, depth, player_num, maximizing_player):
    ##Notes: nonleaf nodes get value from  descendant lead node (at the bottom)
    ## Leaf nodes return heuristic value
    """
    Input:
        board : [[]] - current state of board
        depth: int - current depth of the tree
        player_num: int - ai player first or 2nd
        maximixing_player: bool - which player the heuristic value applies to
    Output:
        score: int - value of the winner
    """
    p = gameplay.Play()
    opp = p.get_opp_num(player_num)
    stop_node = terminal_node(board, player_num)
    if depth == 0:
        return score(board, player_num)
    if stop_node == True:
        if p.check_wins(board, player_num): #player wins
            return -math.inf
        elif p.check_wins(board, opp): #opponent wins
            return math.inf
        else: #draw
            return 0
    if maximizing_player:
        score = -math.inf
        for move in valid_moves(board):
            score = max(score, min_max(child_board(board, player_num, move), player_num, depth + 1, False))
        return score
    elif maximizing_player == False: #if minimizing player
        score = math.inf
        for move in valid_moves(board):
            score = min(score, min_max(child_board(board, opp, move), opp, depth - 1, True))
        return score