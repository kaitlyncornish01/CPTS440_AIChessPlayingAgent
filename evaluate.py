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

MATERIAL_WEIGHT = 1.0
POSITION_WEIGHT = 0.35
MOBILITY_WEIGHT = 4
CENTER_ATTACK_WEIGHT = 10
CENTER_OCCUPATION_WEIGHT = 18
DOUBLED_PAWN_PENALTY = 12
ISOLATED_PAWN_PENALTY = 10
BISHOP_PAIR_BONUS = 30
CASTLED_BONUS = 35

CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]
FILES = list(range(8))

PAWN_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]

ROOK_TABLE = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]

QUEEN_TABLE = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
]

KING_MIDDLEGAME_TABLE = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
]

KING_ENDGAME_TABLE = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50,
]

PIECE_SQUARE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
}


def evaluate(board):
    if board.is_checkmate():
        return -CHECKMATE_SCORE if board.turn == chess.WHITE else CHECKMATE_SCORE

    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.can_claim_threefold_repetition()
        or board.can_claim_fifty_moves()
    ):
        return 0

    score = 0.0
    score += MATERIAL_WEIGHT * _material_score(board)
    score += POSITION_WEIGHT * _piece_square_score(board)
    score += MOBILITY_WEIGHT * _mobility_score(board)
    score += CENTER_ATTACK_WEIGHT * _center_attack_score(board)
    score += CENTER_OCCUPATION_WEIGHT * _center_occupation_score(board)
    score += _pawn_structure_score(board)
    score += _bishop_pair_score(board)
    score += _king_safety_score(board)

    return int(score)


def _material_score(board):
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score


def _piece_square_score(board):
    score = 0
    endgame = _is_endgame(board)

    for piece_type, table in PIECE_SQUARE_TABLES.items():
        for square in board.pieces(piece_type, chess.WHITE):
            score += table[square]
        for square in board.pieces(piece_type, chess.BLACK):
            score -= table[chess.square_mirror(square)]

    king_table = KING_ENDGAME_TABLE if endgame else KING_MIDDLEGAME_TABLE
    for square in board.pieces(chess.KING, chess.WHITE):
        score += king_table[square]
    for square in board.pieces(chess.KING, chess.BLACK):
        score -= king_table[chess.square_mirror(square)]

    return score


def _mobility_score(board):
    white_mobility = _count_legal_moves_for_color(board, chess.WHITE)
    black_mobility = _count_legal_moves_for_color(board, chess.BLACK)
    return white_mobility - black_mobility


def _center_attack_score(board):
    score = 0
    for square in CENTER_SQUARES:
        score += len(board.attackers(chess.WHITE, square))
        score -= len(board.attackers(chess.BLACK, square))
    return score


def _center_occupation_score(board):
    score = 0
    for square in CENTER_SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            score += 1 if piece.color == chess.WHITE else -1
    return score


def _pawn_structure_score(board):
    white_files = _pawn_counts_by_file(board, chess.WHITE)
    black_files = _pawn_counts_by_file(board, chess.BLACK)

    white_penalty = _doubled_pawn_penalty(white_files) + _isolated_pawn_penalty(white_files)
    black_penalty = _doubled_pawn_penalty(black_files) + _isolated_pawn_penalty(black_files)

    return black_penalty - white_penalty


def _bishop_pair_score(board):
    score = 0
    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += BISHOP_PAIR_BONUS
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= BISHOP_PAIR_BONUS
    return score


def _king_safety_score(board):
    score = 0
    if board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
        score += 10
    if board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
        score -= 10

    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)

    if white_king_square in {chess.G1, chess.C1}:
        score += CASTLED_BONUS
    if black_king_square in {chess.G8, chess.C8}:
        score -= CASTLED_BONUS

    return score


def _count_legal_moves_for_color(board, color):
    if board.turn == color:
        return board.legal_moves.count()

    temp_board = board.copy(stack=False)
    temp_board.turn = color
    return temp_board.legal_moves.count()


def _pawn_counts_by_file(board, color):
    counts = {file_index: 0 for file_index in FILES}
    for square in board.pieces(chess.PAWN, color):
        counts[chess.square_file(square)] += 1
    return counts


def _doubled_pawn_penalty(file_counts):
    penalty = 0
    for count in file_counts.values():
        if count > 1:
            penalty += (count - 1) * DOUBLED_PAWN_PENALTY
    return penalty


def _isolated_pawn_penalty(file_counts):
    penalty = 0
    for file_index, count in file_counts.items():
        if count == 0:
            continue

        left_has_pawn = file_counts.get(file_index - 1, 0) > 0
        right_has_pawn = file_counts.get(file_index + 1, 0) > 0
        if not left_has_pawn and not right_has_pawn:
            penalty += count * ISOLATED_PAWN_PENALTY
    return penalty


def _is_endgame(board):
    white_queens = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queens = len(board.pieces(chess.QUEEN, chess.BLACK))
    minor_major_material = 0

    for piece_type in (chess.ROOK, chess.BISHOP, chess.KNIGHT):
        minor_major_material += len(board.pieces(piece_type, chess.WHITE))
        minor_major_material += len(board.pieces(piece_type, chess.BLACK))

    return white_queens + black_queens == 0 or minor_major_material <= 4
