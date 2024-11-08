# Tic-Tac-Toe over TCP/IP

This project is a Python implementation of the classic Tic-Tac-Toe game that allows two players to play over a network using TCP/IP sockets. The game runs in the console, and players take turns making moves on a 3x3 grid. The server manages the game session while the two clients independently participate in the game.

## Features

- **Network-based gameplay**: Two players can join the game via TCP/IP sockets and play against each other.
- **Game board display**: The current game board is shown in the console after each move.
- **Victory check**: The game checks for a winner after every move and announces the winner when applicable.
- **Replay option**: After a player wins, the game prompts both players for a rematch.
- **Invalid move handling**: If a player attempts to make an invalid move, they will be prompted to make another move.

## How to Install and Run the Project

Follow these steps to install and run the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/guisoaresdev/tcp-tictactoe-py
   ```
2. **Navigate to the project folder**:
   ```bash
   cd tcp-tictactoe-py
   ```
3. **Run the server**:
   ```bash
   python host.py
   ```
4. **Run the clients (You'll need 2 terminals, one for each client)**:
   ```bash
   python client.py
   ```
