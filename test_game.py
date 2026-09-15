import duckdb
import re


con = duckdb.connect("chess_data_with_evals.db")
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

max_move = ply_to_move_number(df.ply.iloc[0])
print(cut_pgn(df.pgn_string.iloc[0], max_move))

