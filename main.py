import chess
from ai import alphabeta

board = chess.Board()

while not board.is_game_over():
    print(board)
    print("\n")

    _, move = alphabeta(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=board.turn)

    board.push(move)

print("Game over!")
print(board.result())