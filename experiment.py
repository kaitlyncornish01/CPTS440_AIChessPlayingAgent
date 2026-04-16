import argparse
import csv
import time

import chess

from ai import alphabeta_with_stats, minimax_with_stats


ALGORITHMS = {
    "alphabeta": alphabeta_with_stats,
    "minimax": minimax_with_stats,
}

DEFAULT_DEPTHS = [1, 2, 3]
DEFAULT_RESULTS_FILE = "results.csv"


def play_game(algorithm_name, depth):
    board = chess.Board()
    move_count = 0
    total_nodes = 0
    search = ALGORITHMS[algorithm_name]

    start_time = time.time()

    while not board.is_game_over():
        maximizing_player = board.turn == chess.WHITE

        if algorithm_name == "alphabeta":
            _, move, nodes = search(
                board,
                depth,
                float("-inf"),
                float("inf"),
                maximizing_player,
            )
        else:
            _, move, nodes = search(board, depth, maximizing_player)

        if move is None:
            break

        total_nodes += nodes
        board.push(move)
        move_count += 1

    total_time = time.time() - start_time
    result = board.result() if board.is_game_over() else "unfinished"

    return {
        "algorithm": algorithm_name,
        "depth": depth,
        "moves": move_count,
        "result": result,
        "time_seconds": total_time,
        "nodes": total_nodes,
        "avg_time_per_move": total_time / move_count if move_count else 0.0,
        "avg_nodes_per_move": total_nodes / move_count if move_count else 0.0,
    }


def run_experiments(algorithms, depths, trials, output_file):
    fieldnames = [
        "algorithm",
        "trial",
        "depth",
        "moves",
        "result",
        "time_seconds",
        "nodes",
        "avg_time_per_move",
        "avg_nodes_per_move",
    ]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for algorithm_name in algorithms:
            for depth in depths:
                for trial in range(1, trials + 1):
                    print(
                        f"Running {algorithm_name} at depth {depth} "
                        f"(trial {trial}/{trials})..."
                    )

                    result = play_game(algorithm_name, depth)
                    result["trial"] = trial
                    writer.writerow(result)

                    print(
                        f"  Result: {result['result']}, "
                        f"moves={result['moves']}, "
                        f"time={result['time_seconds']:.4f}s, "
                        f"nodes={result['nodes']}"
                    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run self-play chess AI experiments and save metrics to CSV."
    )
    parser.add_argument(
        "--algorithms",
        nargs="+",
        choices=sorted(ALGORITHMS.keys()),
        default=["alphabeta"],
        help="Algorithms to benchmark.",
    )
    parser.add_argument(
        "--depths",
        nargs="+",
        type=int,
        default=DEFAULT_DEPTHS,
        help="Search depths to benchmark.",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=1,
        help="Number of self-play games to run for each algorithm/depth pair.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_RESULTS_FILE,
        help="CSV file used to store experiment results.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_experiments(args.algorithms, args.depths, args.trials, args.output)
