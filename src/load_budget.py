"""
load_budget.py - Laad begrotingsdata in DuckDB
Voor Issue01_KC_2027: Vergelijking Bestuur vs Twins
"""

import os

import duckdb

print("=" * 60)
print("📊 BEGROTING LADEN IN DUCKDB")
print("=" * 60)

# Controleer of bestand bestaat
budget_file = "C:/Users/hansh/VVE_BRAIN/data/Issue01_KC_2027.txt"
if not os.path.exists(budget_file):
    print(f"❌ Bestand niet gevonden: {budget_file}")
    print("Maak eerst het bestand aan met de begrotingsdata.")
    exit(1)

# Connect to DuckDB
conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")

# Laad de begrotingsdata
try:
    conn.execute(f"""
        CREATE OR REPLACE TABLE budget AS 
        SELECT * FROM read_csv_auto('{budget_file}')
    """)
    print("✅ Begrotingsdata geladen")

    # Toon eerste rijen ter controle
    print("\n📋 Eerste 5 rijen:")
    print(conn.execute("SELECT * FROM budget LIMIT 5").df())

    # Toon totalen per bron
    totals = conn.execute("""
        SELECT Bron, SUM(Bedrag) AS Totaal
        FROM budget
        GROUP BY Bron
    """).df()

    print("\n📊 Totalen per bron:")
    print(totals.to_string(index=False))

except Exception as e:
    print(f"❌ Fout bij laden: {e}")
    exit(1)

print("\n✅ Script voltooid.")
