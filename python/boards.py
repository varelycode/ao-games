from copy import deepcopy

class Board:
    HEIGHT = 6
    WIDTH = 7

    def __init__(self, board, player_num):
        self.player_num = player_num
        self.num_moves_played = 0
        self.player_bitboard, self.mask_bitboard = self.get_bit_board_alt(board)

    def is_column_free(self, col: int) -> bool:
        mask_int = int(self.mask_bitboard, 2)
        top_mask = (1 << (self.HEIGHT - 1)) << col * (self.HEIGHT + 1)
        return ((mask_int & top_mask) == 0)

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << 5) << column * 7
        #print(format(top_mask, 'b'))
        return top_mask

    def is_winning_move(self, col: int) -> bool:
        p = deepcopy(self.player_bitboard)
        col_mask = (1 << self.HEIGHT-1) << col * (self.HEIGHT+1)
        bottom_mask = 1 << (col * WIDTH)
        p = p | (self.mask_bitboard + bottom_mask) & col_mask
        return (self.connect4_check(p))

    def connect4_check(self, player_mask) -> bool:
        # 4 across
        temp_mask = player_mask & (player_mask >> (HEIGHT + 1))
        if (temp_mask & (temp_mask >> (2 * (HEIGHT + 1)))):
            return True
        
        # 4 diagonal (1)
        temp_mask = player_mask & (player_mask >> HEIGHT)
        if (temp_mask & (temp_mask >> (2 * HEIGHT))):
            return True

        # 4 diagonal (2)
        temp_mask = player_mask & (player_mask >> (HEIGHT + 2))
        if (temp_mask & (temp_mask >> (2 * (HEIGHT + 2)))):
            return True
        
        # 4 vertical
        temp_mask = player_mask & (player_mask >> 1)
        if (temp_mask & (temp_mask >> 2)):
            return True
        
        return False

    def play_column(self, col: int):
        self.player_bitboard = self.player_bitboard ^ self.mask_bitboard
        self.mask_bitboard = self.mask_bitboard | (self.mask_bitboard + (1 << (col * WIDTH)))
        self.num_moves_played += 1
    # def win_condition(self, ):

    def get_bit_board_alt(self, board) -> str:
        player_bitboard = ''
        mask_bitboard = ''
        for col in range(6, -1, -1):
            mask_bitboard += '0'
            player_bitboard += '0'
            for row in range(6):
                this_cell = board[row][col]
                if this_cell == 0:
                    mask_bitboard += '0'
                    player_bitboard += '0'
                else:
                    mask_bitboard += '1'
                    if this_cell == self.player_num:
                        player_bitboard += '1'
                    else:
                        player_bitboard += '0'
        return player_bitboard, mask_bitboard

    def get_bit_board(self, board: [[]], player_num: int) -> str:
        #Input board: [[]] - Takes, player and board list contains current state of board
        #Output mask: '', player: ''Returns Mask and position of current player
        player = ''
        mask = ''
        brd = list(zip(*board)) #get cols
        print("brd: ", brd)
        for row in brd: #iterate through cols
            print(row)
            for pos in row: #access each item in cols
                if pos == 0:
                    mask += '0'
                    player += '0'
                else:
                    mask += '1'

                if pos == player_num:
                    player += '1'
                else:
                    player += '0'
                
                mask += '0'
                player += '0'
        """ print("mask:")
        for i in range(6, -1, -1):
            for j in range(7):
                print(mask[i + (j * 7)], end='')
            print('\n', end='') """
        print('\n', end='')
        print("player: ", player)
        print(self.is_column_free(mask, 0))

        print("row", row)
        print("In class board")

        return mask, player

    # def get_opponent(self, mask, current) -> str:
    #
    #     return mask xor


