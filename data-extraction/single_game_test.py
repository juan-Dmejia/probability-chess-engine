import duckdb
import functions

con = duckdb.connect("chess_data.db")
con.execute("LOAD aixchess;")

df = con.execute("""
    WITH move_table AS (
    SELECT 
        movedata,
        m.ply,
        piece_counts_at_position(movedata, m.ply)."wP" AS white_pawns
    FROM (
        SELECT * FROM games_sample LIMIT 1
    ),
    UNNEST(move_details(movedata)) AS t(m)
    ), -- Filter moves by pawn count and delete if it is black to play (ply is even)
    filtered_moves AS (
        SELECT * FROM move_table
        WHERE white_pawns >= 7 AND ply % 2 <> 0
    )
    -- Select a random ply from the filtered results
    SELECT
        ply,
        to_pgn(movedata) AS pgn_string
    FROM filtered_moves
    USING SAMPLE 1 ROWS;
""").df()

con.close()

max_move = functions.ply_to_move_number(df.ply.iloc[0])
base_pgn = functions.cut_pgn(df.pgn_string.iloc[0], max_move)
legal_moves = functions.return_legal_moves(base_pgn)
custom_pgns = []
for i in range(len(legal_moves)):
    custom_pgns.append(functions.append_to_pgn(base_pgn, legal_moves[i], max_move))

