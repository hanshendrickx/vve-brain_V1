# Check both files
print("=== BEGROTING FILE (first 20 lines) ===")
with open(r"C:\Users\hansh\VVE_BRAIN\data\Zomer\prognose-2026-begroting-2027.csv.txt", 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 20:
            print(line.strip())
        else:
            break

print("\n=== SPLITSINGSAKTE FILE (first 10 lines) ===")
with open(r"C:\Users\hansh\VVE_BRAIN\data\splitsingsakte_clean.csv.txt", 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 10:
            print(line.strip())
        else:
            break