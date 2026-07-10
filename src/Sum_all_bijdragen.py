import duckdb

print("=" * 60)
print("VVE FINANCIAL SUMMARY")
print("=" * 60)

try:
    # Connect to DuckDB
    conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")

    # Check if table exists
    tables = conn.execute("SHOW TABLES").fetchall()
    print("Tables found:", tables)

    # Calculate total contributions
    result = conn.execute("""
        SELECT 
            COUNT(*) AS Total_Owners,
            SUM(Total_Breukdelen) AS Total_Breukdelen,
            SUM(Total_Breukdelen) / 
                (SELECT SUM(Total_Breukdelen) FROM owners_with_parking) * 250000 
                AS Total_Contributions,
            AVG(Total_Breukdelen) AS Avg_Breukdelen,
            AVG(Total_Breukdelen) / 
                (SELECT SUM(Total_Breukdelen) FROM owners_with_parking) * 250000 
                AS Avg_Contribution
        FROM owners_with_parking
    """).fetchall()

    print(f"Total Owners: {result[0][0]}")
    print(f"Total Breukdelen: {result[0][1]:.6f}")
    print(f"Total Annual Contributions: €{result[0][2]:.2f}")

except Exception as e:
    print(f"Error: {e}")
