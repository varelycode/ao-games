#!/usr/bin/python

import sys
import json
import socket
import boards
import moves

# 2 - red; 1- yellow (us)
TEST_1 = [[0,0,0,0,0,0,0], [0,0,0,2,0,0,0], [0,0,1,1,0,0,0], [0,0,2,1,0,0,0], [0,0,2,2,1,0,0], [0,0,2,1,1,2,0]]


def get_move(player, board):
  # TODO determine valid moves
  # TODO determine best move

  return moves.get_best_move()

def prepare_response(move):
  response = '{}\n'.format(json.dumps(move))
  print('sending {!r}'.format(response))
  return response.encode(encoding='UTF-8') #return response as bytes-like

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337 # default port 1337, add optional port
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname() # default hostname at gethostname or add optional name

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
      obj = boards.Board()
      mask, current = obj.get_bit_board(TEST_1)
      print(player, maxTurnTime, board)
      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()

