from copy import deepcopy

class Board:
    HEIGHT: int = 6
    WIDTH: int = 7
    MIN_SCORE = -1 * (WIDTH * HEIGHT) // 2 + 3;
    MAX_SCORE = (WIDTH * HEIGHT +1 ) // 2 - 3;

    def __init__(self, board, player_num):
        self.player_num = player_num
        self.bottom_mask = self.get_bottom_row_mask(self.WIDTH, self.HEIGHT)
        self.board_mask = self.bottom_mask * ((1 << self.HEIGHT) - 1)
        self.num_moves_played = 0

        # player_bitboard is the bitboard of the player's pieces
        # mask bitboard is the bitboard of all non-empty spaces
        self.player_bitboard, self.mask_bitboard = self.get_bit_board(board)

    def is_column_free(self, col: int) -> bool:
        top_mask = self.get_top_mask(col)
        return ((self.mask_bitboard & top_mask) == 0)

    def get_key(self): # Get unique transposition table key for this board position
        return self.player_bitboard + self.mask_bitboard

    def get_non_losing_moves(self) -> int:
        possible_moves = self.get_possible_moves_mask()
        opponent_wins = self.get_opponent_winning_pos()
        forced = possible_moves & opponent_wins
        if forced:
            if (forced & (forced - 1)):
                return 0
            else:
                possible_moves = forced
        return possible_moves & ~(opponent_wins >> 1)
    
    def get_possible_moves_mask(self) -> int:
        return (self.mask_bitboard + self.bottom_mask) & self.board_mask
    
    def get_player_winning_pos(self) -> int:
        return self.get_winning_moves_mask(self.player_bitboard, self.mask_bitboard)

    def get_opponent_winning_pos(self) -> int:
        return self.get_winning_moves_mask(self.player_bitboard ^ self.mask_bitboard, self.mask_bitboard)

    def get_column_mask(self, col: int) -> int:
        return ((1 << self.HEIGHT) - 1) << (col * (self.HEIGHT + 1))

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << (self.HEIGHT - 1)) << column * (self.HEIGHT + 1)
        return top_mask

    def is_winning_move(self, col: int) -> bool:
        win_positions = self.get_player_winning_pos()
        possible_moves = self.get_possible_moves_mask()
        col_mask = self.get_column_mask(col)
        return win_positions & possible_moves & col_mask

    def connect4_check(self, player_mask) -> bool:
        # 4 across
        temp_mask = player_mask & (player_mask >> (self.HEIGHT + 1))
        if (temp_mask & (temp_mask >> (2 * (self.HEIGHT + 1)))):
            return True
        
        # 4 diagonal (1)
        temp_mask = player_mask & (player_mask >> self.HEIGHT)
        if (temp_mask & (temp_mask >> (2 * self.HEIGHT))):
            return True

        # 4 diagonal (2)
        temp_mask = player_mask & (player_mask >> (self.HEIGHT + 2))
        if (temp_mask & (temp_mask >> (2 * (self.HEIGHT + 2)))):
            return True
        
        # 4 vertical
        temp_mask = player_mask & (player_mask >> 1)
        if (temp_mask & (temp_mask >> 2)):
            return True
        
        return False

    def play(self, move: int):
        self.player_bitboard ^= self.mask_bitboard
        self.mask_bitboard |= move
        self.num_moves_played += 1

    def play_column(self, col: int):
        self.play((self.mask_bitboard + self.get_bottom_mask_w_col(col)) & self.get_column_mask(col))
    
    # Get mask that's just all 1s in the bottom row
    def get_bottom_row_mask(self, w: int, h: int) -> int:
        if w == 0:
            return 0
        else:
            return self.get_bottom_row_mask(w - 1, h) | 1 << (w - 1) * (h + 1)

    def get_bottom_mask_w_col(self, col: int) -> int:
        return (1 << (col * (self.HEIGHT + 1)))

    # Get the number of winning spots from the mask of winning spots
    def get_num_winning_spots(self, move: int) -> int:
        temp_bitstring = self.get_winning_moves_mask(self.player_bitboard | move, self.mask_bitboard)
        return bin(temp_bitstring).count('1') # Count set bits

    # Use bit-shift ugliness to get a string corresponding to all the free cells making a winning move
    def get_winning_moves_mask(self, player_mask: int, filled_positions_mask: int) -> int:
        # Vertical winning moves
        m1 = (player_mask << 1) & (player_mask << 2) & (player_mask << 3)
        # Horizontal
        m2 = (player_mask << (self.HEIGHT + 1)) & (player_mask << 2 * (self.HEIGHT + 1))
        m1 |= m2 & (player_mask << 3 * (self.HEIGHT + 1))
        m1 |= m2 & (player_mask >> (self.HEIGHT + 1))
        m2 = (player_mask >> (self.HEIGHT + 1)) & (player_mask >> 2*(self.HEIGHT + 1))
        m1 |= m2 & (player_mask << (self.HEIGHT + 1));
        m1 |= m2 & (player_mask >> 3 * (self.HEIGHT + 1))
        # Diag case 1
        m2 = (player_mask << self.HEIGHT) & (player_mask << (2 * self.HEIGHT))
        m1 |= m2 & (player_mask << (3 * self.HEIGHT))
        m1 |= m2 & (player_mask >> self.HEIGHT)
        m2 = (player_mask >> self.HEIGHT) & (player_mask >> (2 * self.HEIGHT))
        m1 |= m2 & (player_mask << self.HEIGHT)
        m1 |= m2 & (player_mask >> (3 * self.HEIGHT))
        # Diag case 2
        m2 = (player_mask << (self.HEIGHT + 2)) & (player_mask << 2 * (self.HEIGHT + 2))
        m1 |= m2 & (player_mask << 3 * (self.HEIGHT + 2))
        m1 |= m2 & (player_mask >> (self.HEIGHT + 2))
        m2 = (player_mask >> (self.HEIGHT + 2)) & (player_mask >> 2 * (self.HEIGHT + 2))
        m1 |= m2 & (player_mask << (self.HEIGHT + 2))
        m1 |= m2 & (player_mask >> 3*(self.HEIGHT + 2))
    
        return m1 & (self.board_mask ^ filled_positions_mask)

    def get_bit_board(self, board) -> str:
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
        return int(player_bitboard, 2), int(mask_bitboard, 2)

