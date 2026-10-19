import io
import re
import chess.pgn
import chess.engine
import math

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
    return  " ".join(parts)


class BoardScanner:
    def __init__(self, base_pgn: str):
        self.base_pgn = base_pgn
        self.game = chess.pgn.read_game(io.StringIO(base_pgn))
        self.board = self.game.end().board()
        self.path = "C:/Users/Juan/Desktop/stockfish/stockfish-windows-x86-64-universal.exe"

    def set_base_pgn(self, pgn: str):
        self.base_pgn = pgn

    # POSITION GENERATION

    def get_legal_moves(self):
        # Extract and return moves in SAN format directly
        return [self.board.san(move) for move in self.board.legal_moves]

    def get_eval(self, pgn):
        # Set temporary game and board vars
        temp_game = chess.pgn.read_game(io.StringIO(pgn))
        temp_board = temp_game.end().board()

        # Open Stockfish and run evaluation
        with chess.engine.SimpleEngine.popen_uci(self.path) as engine:
            # Use depth=10 for quick evaluation
            info = engine.analyse(temp_board, chess.engine.Limit(depth=10))
        
            # Extract score from White's perspective
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
        for pawn in self.board.pieces(chess.PAWN, chess.WHITE):
            # pawns are stored as square they reside on (from 0 - 63)
            rank = math.ceil(pawn / 7)

            if (rank > highest_pawn_rank):
                highest_pawn_rank = rank
            pawn_count += 1

        return {'pawn_count': pawn_count, 'pawn_rank': highest_pawn_rank}

    def get_king_rank(self):
        king_pos = self.board.king(chess.WHITE)
        return {'king_rank': math.ceil(king_pos / 7)}
        
    def is_piece_hanging(self, piece_type: chess.PieceType):
        PIECE_VALUES = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        pieces_to_check = self.board.pieces(piece_type, chess.WHITE)

        for piece in pieces_to_check:
            attackers = self.board.attackers(chess.BLACK, piece)
            defenders = self.board.attackers(chess.WHITE, piece)

            # Sum the actual material value of the attacking and defending pieces
            total_attacker_value = sum(
                PIECE_VALUES.get(self.board.piece_type_at(sq), 0) for sq in attackers
            )
            total_defender_value = sum(
                PIECE_VALUES.get(self.board.piece_type_at(sq), 0) for sq in defenders
            )

            if total_attacker_value > total_defender_value:
                return {f'{chess.piece_name(piece_type)} hanging': True}

        return {f'{chess.piece_name(piece_type)} hanging': False}

    def threatens_piece(self, piece_type: chess.PieceType):
        pieces_to_check = self.board.pieces(piece_type, chess.WHITE)

        for piece in pieces_to_check:
            squares_attacked = self.board.attacks(piece)
            pieces_attacked = []
            for sq in squares_attacked:
                if self.board.color_at(sq) == chess.BLACK:
                    if self.board.piece_type_at(sq)
                    return {f'{chess.piece_name(piece_type)} threatens piece': True}
                

        

    def check_all_conditions(self):
        return (
            self.get_pawn_conditions() |
            self.get_king_rank() |
            self.is_piece_hanging(chess.QUEEN) |
            self.is_piece_hanging(chess.ROOK) |
            self.is_piece_hanging(chess.BISHOP) |
            self.is_piece_hanging(chess.KNIGHT) |
            self.is_piece_hanging(chess.PAWN)
        )
            


# test case
pgn_string = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Bxc6 dxc6 5. O-O"
test_scanner = BoardScanner(pgn_string)

print(test_scanner.check_all_conditions())
print(test_scanner.threatens_piece(chess.QUEEN))
print(test_scanner.board)