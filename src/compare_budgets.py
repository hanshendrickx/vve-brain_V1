"""
compare_budgets.py - Vergelijk Bestuur vs Twins begroting
Voor Issue01_KC_2027
"""

import duckdb

print("=" * 60)
print("📊 BEGROTING VERGELIJKEN")
print("=" * 60)

# Connect to DuckDB
conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")

# Controleer of tabel bestaat
tables = conn.execute("SHOW TABLES").fetchall()
if ("budget",) not in tables:
    print("❌ Tabel 'budget' niet gevonden.")
    print("Run eerst: uv run python src/load_budget.py")
    exit(1)

# Vergelijk Bestuur vs Twins
comparison = conn.execute("""
    SELECT 
        COALESCE(b1.Post, b2.Post) AS Post,
        COALESCE(b1.Bedrag, 0) AS Bestuur,
        COALESCE(b2.Bedrag, 0) AS Twins,
        (COALESCE(b2.Bedrag, 0) - COALESCE(b1.Bedrag, 0)) AS Verschil
    FROM budget b1
    FULL OUTER JOIN budget b2 
        ON b1.Post = b2.Post 
        AND b1.Bron = 'Bestuur' 
        AND b2.Bron = 'Twins'
    WHERE b1.Bron = 'Bestuur' OR b2.Bron = 'Twins'
    ORDER BY Post
""").df()

print("\n📋 Vergelijking per post:")
print(comparison.to_string(index=False))

# Analyseer afwijkingen
afwijkingen = comparison[comparison["Verschil"] != 0]
if not afwijkingen.empty:
    print("\n⚠️ AFWIJKINGEN GEVONDEN:")
    print(afwijkingen.to_string(index=False))

    # Toon alleen posts met verschil
    print("\n🔍 Posts met afwijking:")
    for _, row in afwijkingen.iterrows():
        if abs(row["Verschil"]) > 1:
            print(
                f"   {row['Post']}: €{row['Bestuur']:.2f} → €{row['Twins']:.2f} (€{row['Verschil']:.2f})"
            )
else:
    print("\n✅ Geen afwijkingen gevonden. Begrotingen zijn identiek.")

# Totaal vergelijking
totalen = conn.execute("""
    SELECT 
        SUM(CASE WHEN Bron = 'Bestuur' THEN Bedrag ELSE 0 END) AS Bestuur_Totaal,
        SUM(CASE WHEN Bron = 'Twins' THEN Bedrag ELSE 0 END) AS Twins_Totaal
    FROM budget
""").df()

print("\n📊 Totalen:")
print(f"   Bestuur: €{totalen['Bestuur_Totaal'][0]:,.2f}")
print(f"   Twins:   €{totalen['Twins_Totaal'][0]:,.2f}")
print(f"   Verschil: €{totalen['Twins_Totaal'][0] - totalen['Bestuur_Totaal'][0]:,.2f}")

# Opslaan als CSV voor KasCie
comparison.to_csv("C:/Users/hansh/VVE_BRAIN/data/budget_comparison.csv", index=False)
print("\n✅ Vergelijking opgeslagen als: data/budget_comparison.csv")

print("\n✅ Script voltooid.")
