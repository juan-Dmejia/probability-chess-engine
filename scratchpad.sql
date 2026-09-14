INSTALL aixchess FROM community; LOAD aixchess;

SELECT 
    white, 
    black, 
    result, 
    evals[1] AS centipawns,
    move_details_at(movedata, 0) AS first_move
FROM games_sample
WHERE evals IS NOT NULL
LIMIT 10;

DESCRIBE games_sample;