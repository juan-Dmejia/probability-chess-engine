import duckdb
import functions

PATH_TO_STOCKFISH = "C:/Users/Juan/Desktop/stockfish/stockfish-windows-x86-64-universal.exe"

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


max_move = functions.ply_to_move_number(df.ply.iloc[0])
base_pgn = functions.cut_pgn(df.pgn_string.iloc[0], max_move)
legal_moves = functions.return_legal_moves(base_pgn)
base_eval = functions.stockfish_eval(base_pgn, PATH_TO_STOCKFISH)

positions = {"base": {"pgn": base_pgn, "eval": base_eval}}

for i in range(len(legal_moves)):
    current_pgn = functions.append_to_pgn(base_pgn, legal_moves[i], max_move)
    positions[str(i)] = {"pgn": current_pgn, "eval": functions.stockfish_eval(current_pgn, PATH_TO_STOCKFISH)}

print(f"base eval: {positions['base']['eval']}, pgn: {positions['base']['pgn']}")
print(f"last move: {positions[str(len(legal_moves) - 1)]['eval']}, pgn: {positions[str(len(legal_moves) - 1)]['pgn']}")

con.execute("""
    CREATE OR REPLACE TABLE test_game_moves (
        quality VARCHAR PRIMARY KEY,
        count INT
    );

""")

move_count = 0
best_count = 0
good_count = 0
mid_count = 0
blunder_count = 0

for key in positions:
    if key == "base":
        continue

    eval_diff = positions["base"]["eval"] - positions[key]["eval"]
    move_count += 1

    if eval_diff <= 10:
        best_count += 1
    elif eval_diff <= 30:
        good_count += 1
    elif eval_diff <= 100:
        mid_count += 1
    else:
        blunder_count += 1

con.execute(f"""
    INSERT INTO test_game_moves
    VALUES
    ('total', {move_count}),
    ('best', {best_count}),
    ('good', {good_count}),
    ('mid', {mid_count}),
    ('blunder', {blunder_count});
""")

rows = con.execute("SELECT * FROM test_game_moves;").fetchall()
print(rows)
con.close()

