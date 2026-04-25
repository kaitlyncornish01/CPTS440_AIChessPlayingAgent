import tkinter as tk
from tkinter import messagebox, ttk

import chess

from ai import alphabeta


LIGHT_SQUARE = "#f0d9b5"
DARK_SQUARE = "#b58863"
SELECTED_SQUARE = "#f6f669"
MOVE_TARGET_SQUARE = "#cde88f"
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8

PIECE_SYMBOLS = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}

HUMAN_VS_AI = "Human vs AI"
AI_VS_AI = "AI vs AI"


class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess AI Demo")
        self.board = chess.Board()
        self.selected_square = None
        self.legal_targets = set()
        self.auto_play_job = None
        self.auto_play_stop_requested = False

        self.status_var = tk.StringVar(value="Your turn. You are White.")
        self.depth_var = tk.IntVar(value=2)
        self.mode_var = tk.StringVar(value=HUMAN_VS_AI)

        self._build_layout()
        self._draw_board()

    def _build_layout(self):
        container = ttk.Frame(self.root, padding=12)
        container.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=0)
        container.rowconfigure(0, weight=1)

        board_frame = ttk.Frame(container)
        board_frame.grid(row=0, column=0, sticky="nsew")

        self.board_canvas = tk.Canvas(
            board_frame,
            width=BOARD_SIZE,
            height=BOARD_SIZE,
            highlightthickness=0,
            bg="#d8d2c4",
        )
        self.board_canvas.grid(row=0, column=0, sticky="nsew")
        self.board_canvas.bind("<Button-1>", self.on_canvas_click)

        side_panel = ttk.Frame(container, padding=(12, 0, 0, 0))
        side_panel.grid(row=0, column=1, sticky="ns")

        ttk.Label(side_panel, text="Chess AI Controls", font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        ttk.Label(side_panel, text="Game mode").grid(row=1, column=0, sticky="w")
        mode_selector = ttk.Combobox(
            side_panel,
            textvariable=self.mode_var,
            values=[HUMAN_VS_AI, AI_VS_AI],
            state="readonly",
            width=18,
        )
        mode_selector.grid(row=2, column=0, sticky="ew", pady=(4, 12))
        mode_selector.bind("<<ComboboxSelected>>", self.on_mode_change)

        ttk.Label(side_panel, text="AI search depth").grid(row=3, column=0, sticky="w")
        depth_selector = ttk.Spinbox(
            side_panel,
            from_=1,
            to=4,
            textvariable=self.depth_var,
            width=5,
        )
        depth_selector.grid(row=4, column=0, sticky="w", pady=(4, 12))

        ttk.Button(side_panel, text="New Game", command=self.new_game).grid(
            row=5, column=0, sticky="ew", pady=(0, 8)
        )
        ttk.Button(side_panel, text="Undo Last Move", command=self.undo_last_turn).grid(
            row=6, column=0, sticky="ew", pady=(0, 8)
        )
        self.start_auto_play_button = ttk.Button(
            side_panel, text="Start Auto Play", command=self.start_auto_play
        )
        self.start_auto_play_button.grid(row=7, column=0, sticky="ew", pady=(0, 8))
        self.stop_auto_play_button = ttk.Button(
            side_panel, text="Stop Auto Play", command=self.request_stop_auto_play
        )
        self.stop_auto_play_button.grid(row=8, column=0, sticky="ew", pady=(0, 8))
        self.step_move_button = ttk.Button(
            side_panel, text="Play One Turn", command=self.play_one_ai_turn
        )
        self.step_move_button.grid(row=9, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(side_panel, text="How to play").grid(row=10, column=0, sticky="w", pady=(12, 4))
        instructions = (
            "Human vs AI: click a White piece, then click a highlighted square.\n"
            "AI vs AI: start a new game, then use Start Auto Play or Play One Turn."
        )
        ttk.Label(side_panel, text=instructions, wraplength=220, justify="left").grid(
            row=11, column=0, sticky="w"
        )

        ttk.Label(side_panel, textvariable=self.status_var, wraplength=220, justify="left").grid(
            row=12, column=0, sticky="w", pady=(16, 0)
        )

        self._update_mode_controls()

    def new_game(self):
        self.stop_auto_play()
        self.board.reset()
        self.selected_square = None
        self.legal_targets.clear()

        if self.mode_var.get() == AI_VS_AI:
            self.status_var.set("New AI vs AI game ready. Click Start Auto Play.")
        else:
            self.status_var.set("New game started. Your turn as White.")

        self._draw_board()

    def undo_last_turn(self):
        self.stop_auto_play()

        if len(self.board.move_stack) >= 2:
            self.board.pop()
            self.board.pop()
            self.selected_square = None
            self.legal_targets.clear()
            self.status_var.set("Undid the last full turn.")
            self._draw_board()
        elif len(self.board.move_stack) == 1:
            self.board.pop()
            self.selected_square = None
            self.legal_targets.clear()
            self.status_var.set("Undid the last move.")
            self._draw_board()
        else:
            self.status_var.set("There are no moves to undo.")

    def on_mode_change(self, _event=None):
        self.stop_auto_play()
        self.selected_square = None
        self.legal_targets.clear()
        self._update_mode_controls()

        if self.mode_var.get() == AI_VS_AI:
            self.status_var.set("AI vs AI selected. Start a new game or click Start Auto Play.")
        else:
            self.status_var.set("Human vs AI selected. You are White.")

        self._draw_board()

    def on_canvas_click(self, event):
        if self.mode_var.get() != HUMAN_VS_AI:
            return

        if self.board.is_game_over() or self.board.turn != chess.WHITE:
            return

        file_index = event.x // SQUARE_SIZE
        rank_index = event.y // SQUARE_SIZE

        if not (0 <= file_index < 8 and 0 <= rank_index < 8):
            return

        square = chess.square(file_index, 7 - rank_index)
        self.on_square_click(square)

    def on_square_click(self, square):
        piece = self.board.piece_at(square)

        if self.selected_square is None:
            if piece is not None and piece.color == chess.WHITE:
                self._select_square(square)
            return

        if square == self.selected_square:
            self._clear_selection()
            self._draw_board()
            return

        if piece is not None and piece.color == chess.WHITE:
            self._select_square(square)
            return

        move = self._find_matching_move(self.selected_square, square)
        if move is None:
            self.status_var.set("That move is not legal. Choose a highlighted square.")
            return

        self.board.push(move)
        self._clear_selection()
        self._draw_board()

        if self.board.is_game_over():
            self._finish_game()
            return

        self.root.after(150, self.run_single_ai_turn)

    def start_auto_play(self):
        if self.mode_var.get() != AI_VS_AI:
            self.status_var.set("Switch to AI vs AI mode to start autoplay.")
            return

        if self.board.is_game_over():
            self.status_var.set("The game is over. Start a new game first.")
            return

        if self.auto_play_job is None:
            self.auto_play_stop_requested = False
            self.status_var.set("AI vs AI autoplay started.")
            self._schedule_auto_play()

    def request_stop_auto_play(self):
        if self.auto_play_job is None:
            self.status_var.set("Auto play is not currently running.")
            return

        if self.board.turn == chess.WHITE:
            self.stop_auto_play()
            self.status_var.set("Auto play stopped after Black completed the turn.")
        else:
            self.auto_play_stop_requested = True
            self.status_var.set("Stop requested. Black will make one final move.")

    def stop_auto_play(self):
        if self.auto_play_job is not None:
            try:
                self.root.after_cancel(self.auto_play_job)
            except tk.TclError:
                pass
            self.auto_play_job = None
        self.auto_play_stop_requested = False

    def _update_mode_controls(self):
        if self.mode_var.get() == AI_VS_AI:
            self.start_auto_play_button.grid()
            self.stop_auto_play_button.grid()
            self.step_move_button.grid()
        else:
            self.start_auto_play_button.grid_remove()
            self.stop_auto_play_button.grid_remove()
            self.step_move_button.grid_remove()

    def _schedule_auto_play(self):
        self.auto_play_job = self.root.after(250, self.run_auto_play_turn)

    def run_auto_play_turn(self):
        self.auto_play_job = None

        if self.mode_var.get() != AI_VS_AI or self.board.is_game_over():
            return

        self.status_var.set(
            f"AI is thinking for {'White' if self.board.turn == chess.WHITE else 'Black'}..."
        )
        self.root.update_idletasks()
        self._run_ai_move()

        if self.board.is_game_over():
            self._finish_game()
            return

        if self.auto_play_stop_requested and self.board.turn == chess.WHITE:
            self.stop_auto_play()
            self.status_var.set("Auto play stopped after Black completed the turn.")
            return

        self._schedule_auto_play()

    def play_one_ai_turn(self):
        self.stop_auto_play()

        if self.mode_var.get() != AI_VS_AI:
            self.status_var.set("Switch to AI vs AI mode to step through AI moves.")
            return

        if self.board.is_game_over():
            self.status_var.set("The game is over. Start a new game first.")
            return

        starting_side = "White" if self.board.turn == chess.WHITE else "Black"
        self.status_var.set(f"Playing one full turn starting with {starting_side}...")
        self.root.update_idletasks()
        self._run_ai_move()

        if self.board.is_game_over():
            self._finish_game()
            return

        self._run_ai_move()

        if self.board.is_game_over():
            self._finish_game()
            return

        next_side = "White" if self.board.turn == chess.WHITE else "Black"
        self.status_var.set(f"Turn complete. {next_side} to move.")

    def run_single_ai_turn(self):
        if self.board.is_game_over():
            return

        self.status_var.set("AI is thinking...")
        self.root.update_idletasks()
        self._run_ai_move()

        if self.board.is_game_over():
            self._finish_game()
            return

        self.status_var.set(f"AI played the move. Your turn.")

    def _run_ai_move(self):
        maximizing_player = self.board.turn == chess.WHITE
        _, move = alphabeta(
            self.board,
            depth=self.depth_var.get(),
            alpha=float("-inf"),
            beta=float("inf"),
            maximizing_player=maximizing_player,
        )

        if move is None:
            return

        self.board.push(move)
        self._draw_board()

    def _select_square(self, square):
        self.selected_square = square
        self.legal_targets = {
            move.to_square for move in self.board.legal_moves if move.from_square == square
        }
        self.status_var.set(f"Selected {chess.square_name(square)}.")
        self._draw_board()

    def _clear_selection(self):
        self.selected_square = None
        self.legal_targets.clear()

    def _find_matching_move(self, from_square, to_square):
        matching_moves = [
            move
            for move in self.board.legal_moves
            if move.from_square == from_square and move.to_square == to_square
        ]

        if not matching_moves:
            return None

        for move in matching_moves:
            if move.promotion == chess.QUEEN:
                return move

        return matching_moves[0]

    def _draw_board(self):
        self.board_canvas.delete("all")

        for rank_index in range(8):
            for file_index in range(8):
                square = chess.square(file_index, 7 - rank_index)
                x1 = file_index * SQUARE_SIZE
                y1 = rank_index * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                is_light_square = (rank_index + file_index) % 2 == 0
                background = LIGHT_SQUARE if is_light_square else DARK_SQUARE

                if square == self.selected_square:
                    background = SELECTED_SQUARE
                elif square in self.legal_targets:
                    background = MOVE_TARGET_SQUARE

                self.board_canvas.create_rectangle(
                    x1, y1, x2, y2, fill=background, outline=background
                )

                piece = self.board.piece_at(square)
                if piece is not None:
                    self.board_canvas.create_text(
                        x1 + (SQUARE_SIZE / 2),
                        y1 + (SQUARE_SIZE / 2),
                        text=PIECE_SYMBOLS[piece.symbol()],
                        font=("Segoe UI Symbol", 38),
                        fill="#1f1f1f",
                    )

        self._draw_coordinates()

        if not self.board.is_game_over() and self.mode_var.get() == HUMAN_VS_AI:
            if self.board.turn == chess.WHITE and self.selected_square is None:
                self.status_var.set("Your turn. Select a White piece.")

    def _draw_coordinates(self):
        for file_index in range(8):
            self.board_canvas.create_text(
                file_index * SQUARE_SIZE + 10,
                BOARD_SIZE - 10,
                text=chr(ord("a") + file_index),
                font=("Segoe UI", 10),
                fill="#3f3124",
                anchor="sw",
            )

        for rank_index in range(8):
            self.board_canvas.create_text(
                6,
                rank_index * SQUARE_SIZE + 10,
                text=str(8 - rank_index),
                font=("Segoe UI", 10),
                fill="#3f3124",
                anchor="nw",
            )

    def _finish_game(self):
        self.stop_auto_play()
        result = self.board.result()
        outcome_message = f"Game over. Result: {result}"
        self.status_var.set(outcome_message)
        messagebox.showinfo("Game Over", outcome_message)


def main():
    root = tk.Tk()
    ChessApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
