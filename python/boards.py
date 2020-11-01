class Board:


    spaces_available = 42
    COLS = 7
    ROWS = 6
    player_num = 1

    def is_full(self, board): # check if thing is full
        for row in board:
            if 0 in row:
                return False
        return True

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

    def is_draw(self, board, player_num) -> bool: #check if it is a draw
        if self.check_wins(board, player_num) == False and self.is_full(board):
            return True




    """ Functions for bit version """




    def is_full_bit(self, board):
        pass

    def is_column_free(self, mask: '', col: int) -> bool:
        mask_int = int(mask, 2)
        top_mask = self.get_top_mask(col)
        return ((mask_int & top_mask) == 0)

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << 5) << column * 7
        print(format(top_mask, 'b'))
        return top_mask

    def get_bit_opponent(self, mask, current) -> str:
        c = int(mask, 2) ^ int(current, 2)
        return format(c, 'b')

    def get_bit_board(board: [[]], player_num: int) -> str:
        opp = set()
        opp.add(2)
        opp.add(1)
        opp.remove(player_num)
        opposite = opp.pop()
        print(opp)
        # Input board: [[]] - Takes, player and board list contains current state of board
        # Output mask: '', player: ''Returns Mask and position of current player
        player = ''
        mask = ''
        mask_ls = []
        brd = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]
        print("brd: ", brd)
        for row in brd:  # iterate through cols
            for pos in row:  # access each item in cols
                print("pos", pos)
                if pos == 0:
                    mask += '0'
                    player += '0'
                if pos == opposite:
                    mask += '1'
                    player += '0'
                elif pos == player_num:
                    mask += '1'
                    player += '1'
        #res = len(player) == len(mask) # check if they are the same length
        return mask, 2, player, 2
