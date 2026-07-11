#!/usr/bin/env python3
"""
BOD_EOD_test.py - Begin Of Day / End Of Day Quality Checks
Runs all tests and reports status
"""

import subprocess
import sys
from datetime import datetime

def run_command(cmd, description):
    """Run a command and print result"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode == 0:
            print(f"✅ {description} PASSED")
            return True
        else:
            print(f"❌ {description} FAILED")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("🧠 VVE BRAIN - BOD/EOD Quality Check")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # List of checks to run
    checks = [
        ("uv sync", "Sync dependencies"),
        ("uv run ruff check src/ tests/", "Ruff linting"),
        ("uv run black --check src/ tests/", "Black formatting"),
        ("uv run pytest tests/ -v", "Pytest tests"),
        ("git status --porcelain", "Git status"),
    ]
    
    results = []
    for cmd, desc in checks:
        success = run_command(cmd, desc)
        results.append((desc, success))
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    for desc, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status} - {desc}")
    
    print(f"\n   Total: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED - Ready to work!")
    else:
        print("\n⚠️ SOME CHECKS FAILED - Please fix before proceeding")
        sys.exit(1)
    
    print("="*80)

if __name__ == "__main__":
    main()