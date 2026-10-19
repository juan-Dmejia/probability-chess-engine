import io
import re
import chess.pgn
import chess.engine
import chess
import pandas as pd

def ply_to_move_number(ply: int):
    if (ply % 2 == 0):
        return ((ply + 2)//2)
    else:
        return ((ply + 1)//2)

def cut_pgn(pgn: str, max_move: int) -> str:
    pattern = r'\s+' + str(max_move + 1) + r'\.'
    cut_string = re.split(pattern, pgn, maxsplit=1)[0]
    return cut_string.strip()

def append_to_pgn(base_pgn: str, new_move: str, last_move_num: int):
    parts = [base_pgn, f"{last_move_num + 1}.", new_move]
    return " ".join(parts)

def is_hanging(board: chess.Board, square: int) -> bool:
    """Checks if a piece on a specific square is hanging (under-defended)."""
    piece = board.piece_at(square)
    if piece is None:
        return False

    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    piece_color = piece.color
    opponent_color = not piece_color

    attackers = board.attackers(opponent_color, square)
    defenders = board.attackers(piece_color, square)

    total_attacker_value = sum(
        PIECE_VALUES.get(board.piece_type_at(sq), 0) for sq in attackers
    )
    total_defender_value = sum(
        PIECE_VALUES.get(board.piece_type_at(sq), 0) for sq in defenders
    )

    return total_attacker_value > total_defender_value


class BoardScanner:
    def __init__(self, base_pgn: str):
        self.base_pgn = base_pgn
        self.game = chess.pgn.read_game(io.StringIO(base_pgn))
        self.board = self.game.end().board()
        self.path = "C:/Users/Juan/Desktop/stockfish/stockfish-windows-x86-64-universal.exe"

    def set_base_pgn(self, pgn: str):
        self.base_pgn = pgn

    def get_legal_moves(self):
        return [self.board.san(move) for move in self.board.legal_moves]

    def get_eval(self, pgn):
        temp_game = chess.pgn.read_game(io.StringIO(pgn))
        temp_board = temp_game.end().board()

        with chess.engine.SimpleEngine.popen_uci(self.path) as engine:
            info = engine.analyse(temp_board, chess.engine.Limit(depth=10))
            score = info["score"].white()
            
            if score.is_mate():
                return 10000
            else:
                return score.score()

    def possible_positions(self):
        moves = self.get_legal_moves()
        positions = {"base": {"pgn": self.base_pgn, "eval": self.get_eval(self.base_pgn)}}

        for i in range(len(moves)):
            current_pgn = append_to_pgn(self.base_pgn, moves[i], self.board.fullmove_number)
            positions[str(i)] = {"pgn": current_pgn, "eval": self.get_eval(current_pgn)}

        return positions

    # CONDITION CHECKERS

    def get_pawn_conditions(self):        
        highest_pawn_rank = 1
        pawn_count = 0
        for pawn_sq in self.board.pieces(chess.PAWN, chess.WHITE):
            # python-chess built-in rank helper (0 to 7 -> add 1 for 1 to 8)
            rank = chess.square_rank(pawn_sq) + 1

            if (rank > highest_pawn_rank):
                highest_pawn_rank = rank
            pawn_count += 1

        return {'pawn_count': pawn_count, 'max_pawn_rank': highest_pawn_rank}

    def get_king_rank(self):
        king_pos = self.board.king(chess.WHITE)
        if king_pos is None:
            return {'king_rank': 0}
        return {'king_rank': chess.square_rank(king_pos) + 1}
        
    def is_piece_hanging(self, piece_type: chess.PieceType):
        pieces_to_check = self.board.pieces(piece_type, chess.WHITE)

        hanging_found = False
        for piece_sq in pieces_to_check:
            if is_hanging(self.board, piece_sq):
                hanging_found = True
                break

        return {f'{chess.piece_name(piece_type)} hanging': hanging_found}

    def pieces_threatened(self, attack_piece_type: chess.PieceType, threatened_piece_type: chess.PieceType):
        pieces_to_check = self.board.pieces(attack_piece_type, chess.WHITE)
        threatened_squares_set = set()

        for piece_sq in pieces_to_check:
            # Squares attacked by this white piece
            pieces_attacked = self.board.attacks(piece_sq)
            for sq in pieces_attacked:
                # Ensure the square actually contains an enemy piece of the target type, and it's hanging
                target_piece = self.board.piece_at(sq)
                if target_piece and target_piece.color == chess.BLACK and target_piece.piece_type == threatened_piece_type:
                    if is_hanging(self.board, sq):
                        threatened_squares_set.add(sq)

        key_name = f'# of ({chess.piece_name(threatened_piece_type)}) threatened by ({chess.piece_name(attack_piece_type)})'
        return {key_name: len(threatened_squares_set)}

    def check_all_conditions(self):
        hanging_piece_dict = {}
        threatened_piece_dict = {}
        chess_piece_types = [chess.KING, chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.PAWN]

        for piece_type in chess_piece_types:
            hanging_piece_dict.update(self.is_piece_hanging(piece_type))

        for atk_type in chess_piece_types:
            for def_type in chess_piece_types:
                threatened_piece_dict.update(self.pieces_threatened(atk_type, def_type))

        return (
            self.get_pawn_conditions() |
            self.get_king_rank() |
            hanging_piece_dict |
            threatened_piece_dict
        )


# test case
pgn_string = "1. e4 e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 Be7 5. e5 Nfd7 6. Bxe7 Qxe7 7. f4 O-O 8. Nf3 c5 9. dxc5 Nxc5"
test_scanner = BoardScanner(pgn_string)
df = pd.DataFrame([test_scanner.check_all_conditions()])

# Disable column truncation (shows all columns)
pd.set_option('display.max_columns', None)

# Also prevent text inside columns from getting cut off
pd.set_option('display.max_colwidth', None)

print(test_scanner.board)
print(df)