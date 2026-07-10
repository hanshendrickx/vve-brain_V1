import duckdb

conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")

# Show all owners with combined data
result = conn.execute("""
    SELECT 
        Split_Number,
        Votes,
        Breukdelen,
        Total_Votes,
        Total_Breukdelen,
        Payment_Year,
        Payment_Month
    FROM owners_with_parking
    ORDER BY Split_Number
""").fetchall()

for row in result:
    print(row)
