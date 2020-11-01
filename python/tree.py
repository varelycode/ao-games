class Tree:
	def __init__(self): 
		board = [[0,0,0,0,0,0,0], [0,0,0,2,0,0,0], [0,0,1,1,0,0,0], [0,0,2,1,0,0,0], [0,0,2,2,1,0,0], [0,0,2,1,1,2,0]]
	def get_move(board, player_num):
		best_move = {0}
		for i in range((len(board) - 1): #iterate through rows
			for j in range((len(board[i])): #iterate through columns
				if board[i][j] == 0:
					board[i][j] = player_num
					score = minimax(board)
					if score > best_score:
						best_score = score
						best_move = {j}
