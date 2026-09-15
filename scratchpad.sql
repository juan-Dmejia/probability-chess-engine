INSTALL aixchess FROM community; LOAD aixchess;

-- Unest move_details into table 
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

