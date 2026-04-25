# Chess AI with Minimax and Alpha-Beta Pruning

## Overview
This project implements a chess-playing AI using classical adversarial search techniques. The system uses `python-chess` for board representation and legal move generation, then applies search algorithms to choose moves based on a depth-limited lookahead and a heuristic evaluation function.

The project currently supports:
- Human vs AI play in a desktop GUI
- Human vs AI play in the terminal
- Depth-limited Minimax search
- Alpha-Beta pruning
- Heuristic board evaluation
- Automated self-play experiments
- CSV-based metric collection
- Plot generation for runtime and node expansion analysis

## Features
- Board representation and legal move generation with `python-chess`
- Minimax and Alpha-Beta search implementations
- Desktop GUI for interactive play
- Heuristic evaluation based on:
  - material balance
  - mobility
  - piece-square positional scoring
  - center control and occupation
  - pawn structure
  - bishop pair bonus
  - king safety and castling
  - terminal state handling (checkmate, stalemate, insufficient material)
- Node counting for search performance analysis
- Automated self-play benchmarking across algorithms and depths
- CSV output for experiment results
- Visualization of runtime and nodes expanded versus search depth

## Project Structure
- `ai.py`: Minimax and Alpha-Beta search implementations
- `evaluate.py`: Board evaluation heuristic
- `gui.py`: Desktop GUI for Human vs AI play
- `main.py`: Default project entry point that launches the GUI
- `cli.py`: Terminal-based Human vs AI demo
- `experiment.py`: Automated self-play experiments and CSV generation
- `plot_results.py`: Graph generation from CSV results
- `results.csv`: Example experiment output
- `runtime_vs_depth.png`: Example runtime graph
- `nodes_vs_depth.png`: Example node expansion graph

## Installation
Install the project dependencies with:

```bash
pip install -r requirements.txt
```

If needed, you can also install the main packages directly:

```bash
pip install python-chess matplotlib
```

## How to Run

### Play Against the AI in the GUI
Run the desktop GUI:

```bash
python main.py
```

You will play as White against the AI. Click one of your pieces, then click a highlighted legal destination square. The control panel lets you:
- change AI search depth
- start a new game
- undo the last turn

In `AI vs AI` mode, you can also:
- set a different search depth for White and Black
- autoplay the game
- step through one full turn at a time

### Play Against the AI in the Terminal
If you want the original terminal version:

```bash
python cli.py
```

You will be prompted for a search depth and then play as White. Enter moves in UCI format such as `e2e4` or `g1f3`.

### Run Automated Experiments
Run self-play experiments and save the results to a CSV file:

```bash
python experiment.py --algorithms alphabeta minimax --depths 1 2 3 --trials 3 --output results.csv
```

This command runs multiple self-play games for each algorithm and depth combination and records one row per trial in `results.csv`.

Available experiment options:
- `--algorithms`: choose one or more algorithms from `alphabeta` and `minimax`
- `--depths`: choose one or more search depths
- `--trials`: set how many games to run for each algorithm/depth pair
- `--output`: choose the CSV output file name

### Generate Graphs from Results
Create plots directly from the experiment CSV:

```bash
python plot_results.py --input results.csv
```

Optional plot arguments:
- `--runtime-output`: output file name for the runtime graph
- `--nodes-output`: output file name for the nodes expanded graph

If the CSV includes both `alphabeta` and `minimax` runs, each graph will show both algorithms together for direct comparison.

## CSV Metrics
Each experiment row currently records:
- `algorithm`
- `trial`
- `depth`
- `moves`
- `result`
- `time_seconds`
- `nodes`
- `avg_time_per_move`
- `avg_nodes_per_move`

These metrics make it easier to compare the effect of search depth and algorithm choice on performance.

## Current Evaluation Function
The evaluation function combines several weighted heuristics:
- material balance using standard piece values
- piece-square tables for positional play
- mobility based on legal move counts for both sides
- center attack and center occupation of the four central squares
- pawn-structure penalties for doubled and isolated pawns
- bishop pair bonus
- king safety / castling incentives
- terminal position scoring for checkmate and draws

The weights and bonuses are defined as named constants in `evaluate.py`, which makes the heuristic easier to tune and explain during experiments or in the final report.

## Example Workflow
1. Run `python experiment.py --algorithms alphabeta minimax --depths 1 2 3 --trials 3 --output results.csv`
2. Run `python plot_results.py --input results.csv`
3. Review `results.csv`, `runtime_vs_depth.png`, and `nodes_vs_depth.png`

## Notes
- Alpha-Beta pruning is expected to be more efficient than plain Minimax as depth increases.
- Runtime and node counts grow quickly with depth, so deeper experiments may take significantly longer.
- The current plotting script averages results across trials for each algorithm and depth combination.
