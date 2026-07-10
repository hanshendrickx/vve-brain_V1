#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
import os
from datetime import datetime

# File paths
BEGROTING_FILE = r"C:\Users\hansh\VVE_BRAIN\data\Zomer\prognose-2026-begroting-2027.csv.txt"
SPLITSING_FILE = r"C:\Users\hansh\VVE_BRAIN\data\splitsingsakte_clean.csv.txt"
BACKUP_FILE = SPLITSING_FILE.replace('.csv.txt', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv.txt')

def get_2027_bijdrage_from_begroting():
    """Extract the 2027 'Periodieke bijdrage eigenaars' from begroting file"""
    print(f"Reading: {BEGROTING_FILE}")
    
    with open(BEGROTING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            # Look for the row with "Periodieke bijdrage eigenaars"
            if row[0].strip() == "Periodieke bijdrage eigenaars":
                # Columns: 0=Category, 1=Subcategory, 2=2024 Begroot, 3=2024 Realisatie,
                #          4=2025 Begroot, 5=2025 Realisatie, 6=2026 Begroot,
                #          7=2026 Prognose, 8=2027 Begroot
                # So index 8 is 2027 Begroot
                bijdrage_str = row[8].replace(',', '').replace('.', '').strip()
                bijdrage = int(bijdrage_str)
                print(f"✅ Found 2027 bijdrage: {bijdrage}")
                return bijdrage
    
    raise ValueError("Could not find 'Periodieke bijdrage eigenaars' in begroting file")

def update_splitsingsakte(new_bijdrage):
    """Update the bijdrage 2027 value in splitsingsakte"""
    print(f"\nUpdating: {SPLITSING_FILE}")
    
    # First, create a backup
    print(f"📁 Creating backup: {BACKUP_FILE}")
    with open(SPLITSING_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Show the old value
    old_match = re.search(r'bijdragen\s+2027\s*[,;]\s*(\d+)', content, re.IGNORECASE)
    if old_match:
        old_value = old_match.group(1)
        print(f"Old bijdrage 2027 value: {old_value}")
    else:
        print("⚠️ Could not find 'bijdragen 2027' - checking for other patterns...")
        # Try alternative patterns
        old_match = re.search(r'2027\s*[,;]\s*(\d+)', content)
        if old_match:
            old_value = old_match.group(1)
            print(f"Old value found (alternative pattern): {old_value}")
        else:
            old_value = "unknown"
    
    # Replace the value - multiple patterns to catch different formats
    patterns = [
        # Pattern: "bijdragen 2027,250000" or "bijdragen 2027;250000"
        (r'(bijdragen\s+2027\s*[,;]\s*)\d+', rf'\g<1>{new_bijdrage}'),
        # Pattern: "2027,250000" (if just year and value)
        (r'(2027\s*[,;]\s*)(\d+)', rf'\g<1>{new_bijdrage}'),
        # Pattern: "bijdrage 2027 = 250000"
        (r'(bijdrage\s+2027\s*=\s*)\d+', rf'\g<1>{new_bijdrage}'),
        # Pattern: "bijdrage2027:250000"
        (r'(bijdrage\s*2027\s*[:;]\s*)\d+', rf'\g<1>{new_bijdrage}'),
    ]
    
    updated_content = content
    for pattern, replacement in patterns:
        if re.search(pattern, updated_content, re.IGNORECASE):
            updated_content = re.sub(pattern, replacement, updated_content, flags=re.IGNORECASE)
            print(f"✅ Applied pattern: {pattern}")
            break
    else:
        print("❌ No matching pattern found! Please check the file format.")
        print("First 5 lines of splitsingsakte:")
        with open(SPLITSING_FILE, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 5:
                    print(f"  {i+1}: {line.strip()}")
        return False
    
    # Write the updated file
    with open(SPLITSING_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    # Verify the change
    with open(SPLITSING_FILE, 'r', encoding='utf-8') as f:
        new_content = f.read()
        verify_match = re.search(r'bijdragen\s+2027\s*[,;]\s*(\d+)', new_content, re.IGNORECASE)
        if verify_match:
            new_value = verify_match.group(1)
            print(f"✅ Verification: New value is {new_value}")
            if new_value == str(new_bijdrage):
                print("✅ SUCCESS: Value correctly updated!")
                return True
            else:
                print(f"❌ ERROR: Expected {new_bijdrage}, got {new_value}")
                return False
        else:
            print("⚠️ Could not verify - value may not be in expected format")
            return False

def main():
    print("=" * 60)
    print("UPDATE BIJDRAGE 2027 IN SPLITSINGSAKTE")
    print("=" * 60)
    
    try:
        # Get the new value
        new_bijdrage = get_2027_bijdrage_from_begroting()
        
        # Update the splitsingsakte
        success = update_splitsingsakte(new_bijdrage)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ DONE! Splitsingsakte updated successfully.")
            print(f"📊 New bijdrage 2027: {new_bijdrage}")
            print("=" * 60)
        else:
            print("\n❌ Update failed. Check the file format.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()