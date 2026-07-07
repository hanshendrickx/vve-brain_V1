#!/usr/bin/env python3
"""
test_imports.py - Simple import test for VVE BRAIN
"""

import sys
from pathlib import Path

def test_imports():
    """Test all imports are working"""
    print("=" * 60)
    print("PYTEST: Testing VVE BRAIN Imports")
    print("=" * 60)
    
    packages = [
        ("pandas", "pd"),
        ("matplotlib", "plt"),
        ("plotly", "px"),
        ("duckdb", "duckdb"),
        ("openpyxl", "openpyxl"),
    ]
    
    all_ok = True
    for pkg_name, alias in packages:
        try:
            if alias == "pd":
                import pandas as pd
                print(f"[OK] pandas version: {pd.__version__}")
            elif alias == "plt":
                import matplotlib.pyplot as plt
                print(f"[OK] matplotlib version: {plt.matplotlib.__version__}")
            elif alias == "px":
                import plotly.express as px
                print(f"[OK] plotly version: {px.__version__}")
            elif alias == "duckdb":
                import duckdb
                print(f"[OK] duckdb version: {duckdb.__version__}")
            elif alias == "openpyxl":
                import openpyxl
                print(f"[OK] openpyxl version: {openpyxl.__version__}")
        except ImportError as e:
            print(f"[FAIL] {pkg_name} not found: {e}")
            all_ok = False
    
    # Test VVE BRAIN imports
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from vve_brain import VVEBrain
        print("[OK] VVE BRAIN imported successfully")
    except ImportError as e:
        print(f"[FAIL] VVE BRAIN import failed: {e}")
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("[OK] All imports successful!")
    else:
        print("[FAIL] Some imports failed!")
    
    return all_ok

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)