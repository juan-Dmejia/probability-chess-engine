import duckdb

con = duckdb.connect("chess_data_with_evals.db")
con.execute("INSTALL aixchess FROM community; LOAD aixchess;")

dataset_url = "hf://datasets/thomasd1/aix-lichess-database/low_compression/aix_lichess_2023-01_low.parquet"

# Step 1: Create a virtual view pointing to the remote dataset
con.execute(f"CREATE VIEW IF NOT EXISTS remote_games AS SELECT * FROM '{dataset_url}'")

# Step 2: Download a small local sample using a subquery
con.execute("""
    CREATE OR REPLACE TABLE games_sample AS 
    SELECT * FROM remote_games
    WHERE evals IS NOT NULL
    LIMIT 10000
""")

con.close()
print("Done! Local table created successfully.")



