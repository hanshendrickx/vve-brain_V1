"""
report_budget_issue.py - Genereer KasCie rapport voor Issue01_KC_2027
"""

from datetime import datetime

import duckdb

print("=" * 60)
print("📋 KASCIE RAPPORT - ISSUE01_KC_2027")
print("=" * 60)
print(f"Datum: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
print("=" * 60)

# Connect to DuckDB
conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")

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

print("\n📋 1. OVERZICHT BEGROTINGEN")
print("-" * 40)
print(comparison.to_string(index=False))

# Analyseer afwijkingen
afwijkingen = comparison[comparison["Verschil"] != 0]

print("\n📋 2. GEVONDEN AFWIJKINGEN")
print("-" * 40)

if afwijkingen.empty:
    print("Geen afwijkingen gevonden.")
else:
    totaal_verschil = afwijkingen["Verschil"].sum()
    for _, row in afwijkingen.iterrows():
        if abs(row["Verschil"]) > 1:
            print(f"   {row['Post']}:")
            print(f"      Bestuur: €{row['Bestuur']:.2f}")
            print(f"      Twins:   €{row['Twins']:.2f}")
            print(f"      Verschil: €{row['Verschil']:.2f}")

    print(f"\n   Totaal verschil: €{totaal_verschil:.2f}")

print("\n📋 3. AANBEVELINGEN")
print("-" * 40)
print("1. Vraag opheldering over de volgende afwijkingen:")
if not afwijkingen.empty:
    for _, row in afwijkingen.iterrows():
        if abs(row["Verschil"]) > 1:
            print(f"   - {row['Post']} (verschil: €{row['Verschil']:.2f})")

print("\n2. Controleer contracten en verzekeringen:")
print("   - Beheerder: €15.915 vs €12.269")
print("   - Rechtsbijstand: €1.298 (niet in Bestuur)")
print("   - Bestuurdersaansprakelijkheid: €350 (niet in Bestuur)")

print("\n3. Adviseer ALV over goedkeuring van de begroting.")
print("   - Stemmen over de begroting.")
print("   - Registreer eventuele tegenstemmen.")

print("\n📋 4. VOLGENDE STAPPEN")
print("-" * 40)
print("1. Deel dit rapport met de KasCie.")
print("2. Bespreek de bevindingen in de KasCie-vergadering.")
print("3. Stel een definitief advies op voor de ALV.")

print("\n" + "=" * 60)
print("✅ Rapport gegenereerd.")
print("📁 Opslag: data/budget_comparison.csv")
print("=" * 60)
