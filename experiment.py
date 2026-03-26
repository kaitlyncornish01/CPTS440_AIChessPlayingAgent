import time
import chess
import csv
from ai import alphabeta_with_stats


def play_game(depth):
    board = chess.Board()
    move_count = 0
    total_nodes = 0

    start_time = time.time()

    while not board.is_game_over():
        score, move, nodes = alphabeta_with_stats(
            board,
            depth,
            float("-inf"),
            float("inf"),
            board.turn == chess.WHITE
        )

        if move is None:
            break

        total_nodes += nodes
        board.push(move)
        move_count += 1

    end_time = time.time()
    total_time = end_time - start_time

    result = board.result() if board.is_game_over() else "unfinished"

    return {
        "depth": depth,
        "moves": move_count,
        "result": result,
        "time_seconds": total_time,
        "nodes": total_nodes
    }

def run_experiments():
    depths = [1, 2, 3]

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Depth", "Moves", "Result", "Time", "Nodes"])

        for depth in depths:
            print(f"Testing depth {depth}...")
            result = play_game(depth)

            writer.writerow([
                result["depth"],
                result["moves"],
                result["result"],
                result["time_seconds"],
                result["nodes"]
            ])

            print(result)

if __name__ == "__main__":
    run_experiments()