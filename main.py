import duckdb

# Connect to your local database file
con = duckdb.connect("chess_data.db")
con.execute("INSTALL aixchess FROM community; LOAD aixchess;")

dataset_url = "hf://datasets/thomasd1/aix-lichess-database/low_compression/aix_lichess_2023-01_low.parquet"

# Download ONLY 1,000 games locally so the schema loads instantly
con.execute(f"""
    CREATE OR REPLACE TABLE games_sample AS 
    SELECT * FROM '{dataset_url}' 
    LIMIT 1000
""")

con.close()
print("Done! Local table created successfully.")

