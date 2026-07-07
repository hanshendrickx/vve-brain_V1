#!/usr/bin/env python3
"""
[BRAIN] or (blank) VVE BRAIN - Main Entry Point
"""

import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("[BRAIN] or (blank) VVE BRAIN")
    print("The Complete VVE Governance and Financial Management System")
    print("=" * 60)
    
    # Import and run your VVE BRAIN
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from vve_brain import VVEBrain
        
        brain = VVEBrain(year=2025)
        brain.run_complete_analysis()
        
    except ImportError as e:
        print(f"[FAIL] Error importing VVE BRAIN: {e}")
        print("Make sure you have all dependencies installed.")
        print("Run: uv add pandas matplotlib plotly duckdb openpyxl wigglystuff")

if __name__ == "__main__":
    main()