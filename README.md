# Rook vs Bishop Chess Simulation

## Overview

This project is a simplified and special chess simulation featuring only two pieces on the board: a **Bishop (white)** and a **Rook (black)**. Unlike standard chess, the gameplay focuses solely on these two pieces, each with their traditional movement rules but simplified to just one piece per player.

The primary goal is to simulate a battle where the rook tries to survive up to 15 rounds by moving randomly either *up* or *right*, while the bishop tries to capture the rook. The rook wins if it survives all rounds without capture, otherwise the bishop wins.

---

## How the Game Works

- The board is an 8x8 chess grid with files labeled 'a' to 'h' (left to right) and ranks 1 to 8 (bottom to top).
- The bishop always starts at position **c3**, and the rook always starts at **h1**.
- The bishop moves diagonally in any direction.
- The rook moves either straight *up* (along the same file) or *right* (along the same rank).
- The rook moves are determined by:
  1. Tossing a coin: heads = move up, tails = move right.
  2. Rolling two six-sided dice and summing the result to determine how many squares to move.
  3. If the rook moves beyond the top or right edge, it wraps around to the opposite side (e.g., exiting right wraps to the left).
- Players can choose bishop movement mode:
  - **Stationary:** Bishop stays in the initial position.
  - **Human-controlled:** Player can move the bishop each turn.
- The rook and bishop capture each other if, after a move, they occupy the same valid path according to their movement rules.
- The game tracks and displays the number of wins for each side.

---

## Design Decisions and Trade-offs

### Why Only Two Pieces?

Focusing on just one bishop and one rook simplifies the complexity, making it easier to simulate and visualize interactions and rules between two different piece types without full chess mechanics or AI.

### Movement Wrapping

The rook's wrapping movement around the edges is a non-standard chess rule, introduced to add complexity and unpredictability to the rook's survival. It makes the rook's path cyclical and prevents it from getting stuck or cornered too easily.

### User Interface with Pygame

Using Pygame provides a straightforward way to visualize the board, pieces, and animations with minimal dependencies. It allows for interactive play when the bishop is human-controlled and smooth animation of rook moves.

### Modularity and Code Organization

The project is split into logical modules:

- `pieces.py` — Defines piece classes, their movement, and capture rules.
- `board.py` — Handles board drawing and UI rendering.
- `game.py` — Contains game state management, rook movement logic, and game rules.
- `chess_simulation_main.py` — Main loop handling user input, UI updates, and game flow.

This modular design makes the code easier to maintain, test, and extend.

---

## Requirements

- Python 3.7+
- Pygame library (install with `pip install pygame`)

---

## How to Run

1. Clone the repository.
2. Install Pygame if you don’t have it:  
   ```bash
   pip install pygame
