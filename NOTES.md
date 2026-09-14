# Probability Chess Engine Roadmap

## Data Extraction
- [x] Set up local DuckDB database connection
- [x] Query using DuckDB VScode extension
- Set up following Queries (n - iterative variable/position)
    - [ ] get eval in a sample of positions with n # of pawns
    - [ ] get eval in a sample of positions with king position at n
    - [ ] get evla in a sample of positions with n # of moves from promotion
- Set up probability simulations
    - [ ] In those previous queries, find all possible moves x
    - [ ] Query for positions where x is played
        - i.e. look for move ke5 when # of pawns is 7
    - [ ] If eval remains the same or similar, consider move good
    - [ ] Compute probability for all possible moves
        - Might need a way to skip absurd or obviously bad moves
    - [ ] Export numbers to external excel sheet?

## Engine Logic
- [ ] Build move recommendation function based on previously calculated probabilites