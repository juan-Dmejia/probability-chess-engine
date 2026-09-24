# Probability Chess Engine Roadmap
Read this to get an explanation and guide through my thought process and creation of this project. This is seperate from the README, which just explains the project structure and how to use it.

## Data Extraction
- [x] Set up local DuckDB database connection
- [x] Query using DuckDB VScode extension
- [x] Create local table by sampling ~10,000 games

## Single Game Test
Before running the tests on thousands of games and positions, I will extract data from one singular game and go through the entire process for that game.

- [x] Select 1 game at random
- [x] Create table of moves to RAM using selected game
    - Choose arbitrary condition; in this case: # of white pawns
    - Columns should include game movedata (same throughout), ply (current move), arbitrary condition (white pawns)
- [x] Filter out positions with less than 5 white pawns
- [x] From filtered list, select a random ply
- [x] Convert the original movedata blob into a pgn-string using the Aix Extension function: to_pgn()

The pgn-string will be notated "1. (white move) (black move) 2. (white move) (black move) 3. etc.'
- [x] Cut off the pgn-string at previously selected ply using custom function

Now I have a pgn-string denoting a randomly selected position from a randomly selected game

## Generating legal moves
While I could spend a very long time creating my own custom chess board reader and parser, as well as a legal move generator, I opted to use the already available functions from the Python Chess Library. The chess library also allows for communication with a local stockfish application.

- [x] install python-chess and test code snippets
- [x] parse pgn-string into a Game object, then get the board state at the end of the string
- [x] generate and store legal moves as a list at end position using legal_moves()
    - At most, the # of legal moves will be 218. Proven by Tobs40 in his Lichess Blog <i>Why a reachable position can have at most 218 playable moves</i>
- [x] Extract moves in SAN format for easy reading and later appending onto pgn-strings
- [x] Append SAN format legal move strings to base pgn-string using custom function

## Running and Comparing Stockfish Evaluations
This part will require a local stockfish application installed somewhere on the computer. I will denote this in the README file. 

- [x] Store custom pgn-strings in a dictionary numbering each legal move: dict(position_num: dict(pgn: str, eval: int))
- [x] Run and store stockfish evaluation on base pgn-string
- [x] Run stockfish evaluations on all the custom pgn-strings with appended moves
    - A stockfish depth of 10 will be used initially
- [x] Store stockfish evaluations with their corresponding pgn-strings number
- [x] Classify moves based on the difference between their evaluation and the base evaluation (original pgn-string)
    - Best: (0-10), Good: (10-30), Innacurate: (30-100), Bad/Blunder: (100+)
- [x] Create SQL table to store the number of every type of move (best -> blunder)

We now have one statistical sample for some legal moves on one given condition (white_pawns >= 5).
The above test must be run a large amount of times to collect multiple instances of each move being played.
For example, with a large sample size of the move e5 being played, we can estimate the probability of e5 being a good move to play for white, given that the position has 5+ white pawns, to be:
> (# of times e5 is categorized as at least good) / (# of times e5 is played)

## Probability Estimations and Engine Strength
Before I aimlessley run the simulation hundreds of times, I need to determine the concrete conditions the engine will use to determine probabilities. Then I must create custom functions that will run the simulations for me and organize the data in a way easy for the engine to collect and compute with.



## Engine Logic