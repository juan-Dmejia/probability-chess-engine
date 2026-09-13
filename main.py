import duckdb

# Connect and initialize the extension
con = duckdb.connect()
con.execute("INSTALL aixchess FROM community;")
con.execute("LOAD aixchess;")

# Create a virtual table alias pointing to Hugging Face
dataset_url = "hf://datasets/thomasd1/aix-lichess-database/low_compression/aix_lichess_2023-01_low.parquet"
con.execute(f"CREATE VIEW games AS SELECT * FROM '{dataset_url}'")

# Check that the view exists in DuckDB's internal catalog
print(con.execute("SHOW TABLES;").df())

# View the column names and first 5 rows of data
print(con.execute("SELECT * FROM games LIMIT 5;").df())