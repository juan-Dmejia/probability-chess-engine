import io
import re
import chess.pgn

def return_legal_moves(pgn: str):
    # Parse string into a Game object
    game = chess.pgn.read_game(io.StringIO(pgn))

    # Get the board state at the final move of the PGN
    board = game.end().board()

    # Standard legal move generator (returns Move objects)
    legal_moves = list(board.legal_moves)

    # Extract moves in SAN format (e.g., 'Ba4', 'Bxc6', 'Nf6')
    return [board.san(move) for move in board.legal_moves]

def ply_to_move_number(ply: int):
    if (ply % 2 == 0):
        return ((ply + 2)//2)
    else:
        return ((ply + 1)//2)

def cut_pgn(pgn: str, max_move: int) -> str:
    # Matches the space right before the next move number (e.g., " 4.")
    pattern = r'\s+' + str(max_move + 1) + r'\.'
    
    # Split the string at that move number
    cut_string = re.split(pattern, pgn, maxsplit=1)[0]
    return cut_string.strip()

def append_to_pgn(base_pgn: str, new_move: str, last_move_num: int):
    parts = [base_pgn, f"{last_move_num + 1}.", new_move]
    new_pgn = " ".join(parts)
    return new_pgn