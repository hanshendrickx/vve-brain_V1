import duckdb

conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")

# Export to CSV
df = conn.execute("SELECT * FROM owners_with_parking ORDER BY Split_Number").df()
df.to_csv("C:/Users/hansh/VVE_BRAIN/data/owners_complete.csv", index=False)

print(f"Exported {len(df)} owners to data/owners_complete.csv")
