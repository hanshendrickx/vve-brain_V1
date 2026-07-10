import duckdb

print("=" * 60)
print("VALIDATING VVE DATA")
print("=" * 60)

errors = 0
warnings = 0

try:
    conn = duckdb.connect("C:/Users/hansh/VVE_BRAIN/data/vve.duckdb")
    print("Database connected")

    tables = conn.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]

    if "owners_with_parking" in table_names:
        print("owners_with_parking table exists")
    else:
        print("owners_with_parking table NOT found")
        errors += 1

    count = conn.execute("SELECT COUNT(*) FROM owners_with_parking").fetchone()[0]
    if count == 56:
        print(f"Total owners: {count} (expected 56)")
    else:
        print(f"Total owners: {count} (expected 56)")
        warnings += 1

    total_breukdelen = conn.execute(
        "SELECT SUM(Total_Breukdelen) FROM owners_with_parking"
    ).fetchone()[0]
    if abs(total_breukdelen - 8006.0) < 0.001:
        print(f"Total Breukdelen: {total_breukdelen:.6f} (expected 8006)")
    else:
        print(f"Total Breukdelen: {total_breukdelen:.6f} (expected 8006)")
        errors += 1

    null_check = conn.execute("""
        SELECT COUNT(*) FROM owners_with_parking 
        WHERE Split_Number IS NULL OR Total_Breukdelen IS NULL OR Votes IS NULL
    """).fetchone()[0]
    if null_check == 0:
        print("No NULL values found")
    else:
        print(f"Found {null_check} rows with NULL values")
        errors += 1

    parking_count = conn.execute("""
        SELECT COUNT(*) FROM owners_with_parking 
        WHERE Total_Breukdelen > Breukdelen
    """).fetchone()[0]
    if parking_count == 3:
        print(f"{parking_count} owners have parking added")
    else:
        print(f"{parking_count} owners have parking added (expected 3)")
        warnings += 1

    print("\n" + "-" * 60)
    print("OWNERS WITH PARKING ADDED")
    print("-" * 60)

    parking_owners = conn.execute("""
        SELECT 
            Split_Number,
            Votes,
            Breukdelen,
            Total_Breukdelen,
            Total_Votes
        FROM owners_with_parking 
        WHERE Total_Breukdelen > Breukdelen
    """).fetchall()

    for row in parking_owners:
        print(
            f"{row[0]} -> {row[1]} votes, {row[2]} -> {row[3]} breukdelen, {row[4]} total votes"
        )

    contributions = conn.execute("""
        SELECT SUM(Total_Breukdelen) / (SELECT SUM(Total_Breukdelen) FROM owners_with_parking) * 250000 
        FROM owners_with_parking
    """).fetchone()[0]

    if abs(contributions - 250000) < 0.01:
        print(f"Total contributions: {contributions:.2f} (matches 250,000)")
    else:
        print(f"Total contributions: {contributions:.2f} (expected 250,000)")
        errors += 1

except Exception as e:
    print(f"Validation error: {e}")
    errors += 1

print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)
print(f"Errors: {errors}")
print(f"Warnings: {warnings}")

if errors == 0:
    print("ALL CHECKS PASSED - Data is valid")
elif errors > 0:
    print(f"{errors} ERROR(S) FOUND - Please fix")
print("=" * 60)
