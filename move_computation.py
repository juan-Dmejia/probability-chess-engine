import io
import chess.pgn

pgn_string = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6"

# Parse string into a Game object
game = chess.pgn.read_game(io.StringIO(pgn_string))

# Get the board state at the final move of the PGN
board = game.end().board()

print(board)
# 1. Standard legal move generator (returns Move objects)
legal_moves = list(board.legal_moves)

# 3. Extract moves in SAN format (e.g., 'Ba4', 'Bxc6', 'Nf6')
san_moves = [board.san(move) for move in board.legal_moves]

print("Legal SAN Moves:", san_moves)