import chess

CHECKMATE_SCORE = 100000

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]


def evaluate(board):
    # Terminal states
    if board.is_checkmate():
        # If it is checkmate and it is White's turn, White has no legal move and lost.
        # So return a very bad score for White.
        if board.turn == chess.WHITE:
            return -CHECKMATE_SCORE
        else:
            return CHECKMATE_SCORE

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Material
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    # Mobility
    white_mobility = _count_legal_moves_for_color(board, chess.WHITE)
    black_mobility = _count_legal_moves_for_color(board, chess.BLACK)
    score += 5 * (white_mobility - black_mobility)

    # Center control / occupation
    score += 20 * _center_occupation_score(board)

    return score


def _count_legal_moves_for_color(board, color):
    if board.turn == color:
        return board.legal_moves.count()

    temp_board = board.copy()
    temp_board.turn = color
    return temp_board.legal_moves.count()


def _center_occupation_score(board):
    score = 0

    for square in CENTER_SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                score += 1
            else:
                score -= 1

    return score