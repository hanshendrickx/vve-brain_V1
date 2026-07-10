import duckdb
import pandas as pd

# Load owners
df_owners = pd.read_csv(
    "C:/Users/hansh/VVE_BRAIN/data/splitsingsakte_clean.csv.txt",
    sep="\t",
    encoding="utf-8",
    skiprows=1,
    header=None,
)

if len(df_owners.columns) > 10:
    df_owners = df_owners.iloc[:, :10]

df_owners.columns = [
    "Index",
    "Split_Number",
    "Address",
    "Type",
    "Votes",
    "Breukdelen",
    "Eigen",
    "Payment_Year",
    "Payment_Month",
    "Extra",
]

df_owners = df_owners.dropna(subset=["Split_Number"])

# Load parking with Linked_To column
df_parking = pd.read_csv(
    "C:/Users/hansh/VVE_BRAIN/data/extra_parking_place.csv.txt", encoding="utf-8"
)

print(f"✅ Loaded {len(df_owners)} owners")
print(f"✅ Loaded {len(df_parking)} parking places")

# Connect to DuckDB
conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")
conn.register("owners_df", df_owners)
conn.register("parking_df", df_parking)

# Combine using Linked_To
conn.execute("""
    CREATE OR REPLACE TABLE owners_with_parking AS
    SELECT 
        o.*,
        o.Breukdelen + COALESCE(p.Breukdelen, 0) AS Total_Breukdelen,
        o.Votes + COALESCE(p.Votes, 0) AS Total_Votes
    FROM owners_df o
    LEFT JOIN parking_df p ON o.Split_Number = p.Linked_To
""")

print("✅ Combined data created")

# Show affected owners
result = conn.execute("""
    SELECT o.Split_Number, o.Votes, o.Breukdelen, 
           p.Split_Number AS Parking_Split, p.Votes AS Parking_Votes, p.Breukdelen AS Parking_Breukdelen,
           o.Total_Votes, o.Total_Breukdelen
    FROM owners_with_parking o
    LEFT JOIN parking_df p ON o.Split_Number = p.Linked_To
    WHERE p.Split_Number IS NOT NULL
""").fetchall()

print("Affected owners with parking:")
for row in result:
    print(row)
