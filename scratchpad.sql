INSTALL aixchess FROM community; LOAD aixchess;

CREATE TABLE IF NOT EXISTS test_game_moves (
        move_str VARCHAR PRIMARY KEY,
        best INT,
        good INT,
        mid INT,
        blunder INT,
);
