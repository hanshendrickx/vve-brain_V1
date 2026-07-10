import os

import duckdb

# Get project root and convert to DuckDB path format
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base = base.replace("\\", "/")  # Convert Windows to Unix style

# Files with correct path format
owners_file = f"{base}/data/splitsingsakte.csv.txt"
decisions_file = f"{base}/data/alv_decisions.csv.txt"

# Connect
conn = duckdb.connect(f"{base}/data/vve.duckdb")

# Load files
conn.execute(f"""
    CREATE OR REPLACE TABLE owners AS 
    SELECT * FROM read_csv_auto('{owners_file}')
""")

conn.execute(f"""
    CREATE OR REPLACE TABLE decisions AS 
    SELECT * FROM read_csv_auto('{decisions_file}')
""")

print("✅ Owners loaded:", conn.execute("SELECT COUNT(*) FROM owners").fetchone()[0])
print(
    "✅ Decisions loaded:", conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]
)
