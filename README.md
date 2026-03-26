# Chess AI with Minimax and Alpha-Beta Pruning

## Overview
This project implements a Chess-playing AI using classical adversarial search algorithms:
- Minimax
- Alpha-Beta Pruning

The agent evaluates board positions using a heuristic function and selects moves based on search depth.

---

## Features

- Chess game simulation using `python-chess`
- Minimax and Alpha-Beta search
- Heuristic evaluation function:
  - Material balance
  - Mobility
  - Center control
  - Terminal state handling (checkmate/draw)
- Node counting for performance analysis
- Experiment system for benchmarking
- Graph visualization (runtime and nodes)
- Interactive **Human vs AI** mode

---

## File Structure

ai.py              # Minimax and Alpha-Beta algorithms
evaluate.py        # Heuristic evaluation function
main.py            # Demo (Human vs AI or AI vs AI)
experiment.py      # Run experiments and collect results
plot_results.py    # Generate graphs
requirements.txt   # Dependencies

## Installation
pip install chess matplotlib

## How to run
python main.py (play against AI)

python experiment.py (run games at different depths, output: runtime, nodes expanded, game results)

python plot_results.py (generate graphs, outputs: runtime vs depth.png, nodes vs depths.png)

## Algorithms
Minimax: explores all possible moves up to a depth limit and assumes optimal play from both players
Alpha-Beta Pruning: optimizes minimax by pruning branches that cannot affect the final decision, reduving computation. 