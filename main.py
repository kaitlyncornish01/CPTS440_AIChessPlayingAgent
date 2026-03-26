import chess
from ai import alphabeta

board = chess.Board()

depth = int(input("Enter AI search depth (for example 1, 2, or 3): "))

print("\nYou are White.")
print("Enter moves in UCI format, like e2e4 or g1f3.\n")

while not board.is_game_over():
    print(board)
    print()

    if board.turn == chess.WHITE:
        user_move = input("Your move: ").strip()

        try:
            move = chess.Move.from_uci(user_move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move. Try again.\n")
        except ValueError:
            print("Invalid format. Use UCI format like e2e4.\n")

    else:
        print("AI is thinking...")
        _, move = alphabeta(
            board,
            depth=depth,
            alpha=float("-inf"),
            beta=float("inf"),
            maximizing_player=False
        )

        if move is None:
            break

        print(f"AI move: {move}\n")
        board.push(move)

print(board)
print("\nGame over!")
print("Result:", board.result())