"""
analyze_budgets.py - Vergelijk Bestuur en TwinQ begrotingen
"""

import duckdb

print("=" * 60)
print("📊 BEGROTINGEN VERGELIJKEN")
print("=" * 60)

conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")

# Totaal vergelijking
totaal_bestuur = conn.execute("SELECT SUM(Bedrag) FROM begroting_bestuur").fetchone()[0]
totaal_twinq = conn.execute("SELECT SUM(Bedrag) FROM begroting_twinq").fetchone()[0]

print(f"Bestuur totaal: €{totaal_bestuur:,.2f}")
print(f"TwinQ totaal:   €{totaal_twinq:,.2f}")
print(f"Verschil:       €{totaal_twinq - totaal_bestuur:,.2f}")

# Controleer of TwinQ som klopt met breukdelen
print("\n📋 TwinQ detail check:")
twinq_check = conn.execute("""
    SELECT 
        SUM(Bedrag) AS Totaal,
        SUM(Breukdelen) AS Breukdelen,
        COUNT(*) AS Aantal
    FROM begroting_twinq
""").df()
print(twinq_check.to_string(index=False))

# Vergelijk per appartement met splitsingsakte
print("\n📋 Vergelijking met splitsingsakte:")
conn.execute("""
    CREATE OR REPLACE TABLE vergelijking_bijdragen AS
    SELECT 
        t.Appartement,
        t.Bedrag AS TwinQ_Bedrag,
        t.Breukdelen AS TwinQ_Breukdelen,
        s.Breukdelen AS Akte_Breukdelen,
        (t.Breukdelen - s.Breukdelen) AS Breukdelen_Verschil
    FROM begroting_twinq t
    LEFT JOIN owners_with_parking s ON t.Appartement = s.Split_Number
""")

afwijkingen = conn.execute("""
    SELECT * FROM vergelijking_bijdragen
    WHERE Breukdelen_Verschil != 0
""").df()

if afwijkingen.empty:
    print("✅ Geen afwijkingen gevonden tussen TwinQ en splitsingsakte")
else:
    print(f"⚠️ {len(afwijkingen)} afwijkingen gevonden:")
    print(afwijkingen.to_string(index=False))
