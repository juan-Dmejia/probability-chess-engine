INSTALL aixchess FROM community;
LOAD aixchess;

SELECT 
    white, 
    black, 
    result, 
    white_rating,
    move_details_at(movedata, 0) AS first_move
FROM games_sample
LIMIT 10;