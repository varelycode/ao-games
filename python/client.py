#!/usr/bin/python

import sys
import json
import socket
import boards
import moves
import math
from gameplay import *
from boards import *


def get_move(player, board):
  # TODO determine valid moves
  # TODO determine best move
  if(board.num_moves_played < 0):
    return player.column_ordering[board.num_moves_played]
  else:
    print("Using minimax now")
    return player.iterate(board)
    #return player.best_move

def prepare_response(move):
  movedict = {"column": move}
  response = '{}\n'.format(json.dumps(movedict))
  print('sending {!r}'.format(response))
  return response.encode(encoding='UTF-8') #return response as bytes-like

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337 # default port 1337, add optional port
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname() # default hostname at gethostname or add optional name

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  first_turn = True
  board_obj = None
  player_obj = Play()
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      if first_turn:
        board_obj = Board(board, player)
        first_turn = False
      else:
        board_obj.player_bitboard, board_obj.mask_bitboard = board_obj.get_bit_board_alt(board)
  
      """ mask, current = board_obj.get_bit_board_alt([[0,0,0,0,0,0,0],
                                             [0,0,0,2,0,0,0],
                                             [0,0,1,1,0,0,0],
                                             [0,0,2,1,0,0,0],
                                             [0,0,2,2,1,0,0],
                                             [0,0,2,1,1,2,0]], player) """
      print(player, maxTurnTime, board)
      move = get_move(player_obj, board_obj)
      board_obj.play_column(move)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()

