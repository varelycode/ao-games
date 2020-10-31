class Board:

    def is_column_free(self, mask: '', col: int) -> bool:
        mask_int = int(mask, 2)
        top_mask = self.get_top_mask(col)
        return ((mask_int & top_mask) == 0)

    def get_top_mask(self, column: int) -> int:
        top_mask = (1 << 5) << column * 7
        print(format(top_mask, 'b'))
        return top_mask

    # def win_condition(self, ):

    def get_bit_board(self, board: [[]], player_num: int) -> str:
        #Input board: [[]] - Takes, player and board list contains current state of board
        #Output mask: '', player: ''Returns Mask and position of current player
        player = ''
        mask = ''
        brd = list(zip(*board)) #get cols
        print("brd: ", brd)
        for row in brd: #iterate through cols
            for i, pos in enumerate(row): #access each item in cols
                if  == 0:
                    mask += '0'
                    player += '0'
                else:
                    mask += '1'

                if pos == player_num:
                    player += '1'
                else:
                    player += '0'
        print("mask: ", mask)
        print("player: ", player)
        print(self.is_column_free(mask, 0))

        print("row", row)
        print("In class board")

        return mask, player

    # def get_opponent(self, mask, current) -> str:
    #
    #     return mask xor


