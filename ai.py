import chess
from evaluate import evaluate


def minimax(board, depth, maximizing_player):
    score, move, _ = minimax_with_stats(board, depth, maximizing_player)
    return score, move


def alphabeta(board, depth, alpha, beta, maximizing_player):
    score, move, _ = alphabeta_with_stats(board, depth, alpha, beta, maximizing_player)
    return score, move


def minimax_with_stats(board, depth, maximizing_player):
    nodes = 1  # count this position

    if depth == 0 or board.is_game_over():
        return evaluate(board), None, nodes

    legal_moves = list(board.legal_moves)
    best_move = None

    if maximizing_player:
        max_eval = float("-inf")
        for move in legal_moves:
            board.push(move)
            eval_score, _, child_nodes = minimax_with_stats(board, depth - 1, False)
            board.pop()

            nodes += child_nodes

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

        return max_eval, best_move, nodes

    else:
        min_eval = float("inf")
        for move in legal_moves:
            board.push(move)
            eval_score, _, child_nodes = minimax_with_stats(board, depth - 1, True)
            board.pop()

            nodes += child_nodes

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

        return min_eval, best_move, nodes


def alphabeta_with_stats(board, depth, alpha, beta, maximizing_player):
    nodes = 1  # count this position

    if depth == 0 or board.is_game_over():
        return evaluate(board), None, nodes

    legal_moves = list(board.legal_moves)
    best_move = None

    if maximizing_player:
        max_eval = float("-inf")
        for move in legal_moves:
            board.push(move)
            eval_score, _, child_nodes = alphabeta_with_stats(
                board, depth - 1, alpha, beta, False
            )
            board.pop()

            nodes += child_nodes

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval, best_move, nodes

    else:
        min_eval = float("inf")
        for move in legal_moves:
            board.push(move)
            eval_score, _, child_nodes = alphabeta_with_stats(
                board, depth - 1, alpha, beta, True
            )
            board.pop()

            nodes += child_nodes

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval, best_move, nodes