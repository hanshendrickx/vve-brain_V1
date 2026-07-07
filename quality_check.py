#!/usr/bin/env python3
"""
quality_check.py - Run black, ruff, and tests before pushing
Professional code quality control for VVE BRAIN
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

class QualityChecker:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.src_dir = self.project_root / "src"
        self.tests_dir = self.project_root / "tests"
        self.results = {
            "black": {"status": "[X]", "output": ""},
            "ruff": {"status": "[X]", "output": ""},
            "tests": {"status": "[X]", "output": ""}
        }
        self.all_passed = True

    def run_command(self, cmd, description):
        """Run a command and capture output"""
        print(f"\n[EXEC] {description}...")
        print("-" * 50)
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.project_root)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            if result.returncode == 0:
                print(f"[OK] {description} PASSED")
                return True, result.stdout
            else:
                print(f"[FAIL] {description} FAILED")
                self.all_passed = False
                return False, result.stderr
        except Exception as e:
            print(f"[ERROR] Error running {description}: {e}")
            self.all_passed = False
            return False, str(e)

    def check_black(self):
        """Run black code formatter (check mode)"""
        print("\n" + "=" * 60)
        print("BLACK: Code Formatter Check")
        print("=" * 60)

        # Check if black is installed
        check = subprocess.run("uv pip show black", shell=True, capture_output=True)
        if check.returncode != 0:
            print("[INSTALL] Installing black...")
            subprocess.run("uv add --dev black", shell=True)

        # Run black in check mode
        success, output = self.run_command(
            "uv run black --check src/ tests/ --quiet",
            "Black (check mode)"
        )

        if not success:
            print("\n[INFO] To auto-format, run: uv run black src/ tests/")

        self.results["black"]["status"] = "[OK]" if success else "[FAIL]"
        self.results["black"]["output"] = output
        return success

    def check_ruff(self):
        """Run ruff linter"""
        print("\n" + "=" * 60)
        print("RUFF: Code Linter Check")
        print("=" * 60)

        # Check if ruff is installed
        check = subprocess.run("uv pip show ruff", shell=True, capture_output=True)
        if check.returncode != 0:
            print("[INSTALL] Installing ruff...")
            subprocess.run("uv add --dev ruff", shell=True)

        # Run ruff check
        success, output = self.run_command(
            "uv run ruff check src/ tests/",
            "Ruff (lint check)"
        )

        if not success:
            print("\n[INFO] To auto-fix, run: uv run ruff check --fix src/ tests/")

        self.results["ruff"]["status"] = "[OK]" if success else "[FAIL]"
        self.results["ruff"]["output"] = output
        return success

    def check_tests(self):
        """Run pytest tests"""
        print("\n" + "=" * 60)
        print("PYTEST: Unit Tests")
        print("=" * 60)

        # Check if pytest is installed
        check = subprocess.run("uv pip show pytest", shell=True, capture_output=True)
        if check.returncode != 0:
            print("[INSTALL] Installing pytest...")
            subprocess.run("uv add --dev pytest", shell=True)

        # Run tests with coverage
        success, output = self.run_command(
            "uv run pytest tests/ -v --tb=short",
            "Pytest (unit tests)"
        )

        self.results["tests"]["status"] = "[OK]" if success else "[FAIL]"
        self.results["tests"]["output"] = output
        return success

    def run_all(self, auto_fix=False):
        """Run all quality checks"""
        print("=" * 60)
        print("VVE BRAIN - Quality Control System")
        print("=" * 60)
        print(f"Project: {self.project_root}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Step 1: Black
        black_ok = self.check_black()

        # Step 2: Ruff
        ruff_ok = self.check_ruff()

        # Step 3: Tests
        tests_ok = self.check_tests()

        # Summary
        self.print_summary()

        if self.all_passed:
            print("\n" + "=" * 60)
            print("ALL CHECKS PASSED! Ready to push to GitHub!")
            print("=" * 60)
            return True
        else:
            print("\n" + "=" * 60)
            print("Some checks FAILED. Please fix before pushing.")
            print("=" * 60)

            # Auto-fix suggestions
            print("\nSuggested fixes:")
            if not black_ok:
                print("   - Run: uv run black src/ tests/")
            if not ruff_ok:
                print("   - Run: uv run ruff check --fix src/ tests/")
            if not tests_ok:
                print("   - Check tests in tests/ folder")

            return False

    def print_summary(self):
        """Print quality check summary"""
        print("\n" + "=" * 60)
        print("QUALITY CHECK SUMMARY")
        print("=" * 60)

        for tool, result in self.results.items():
            status = result["status"]
            print(f"   {status} {tool.upper()}")
            if result["output"] and len(result["output"]) > 100:
                print(f"      {result['output'][:100]}...")
            elif result["output"]:
                print(f"      {result['output']}")

        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r["status"] == "[OK]")
        print(f"\n   Total: {passed}/{total} checks passed")

    def auto_fix(self):
        """Run auto-fix for black and ruff"""
        print("\n" + "=" * 60)
        print("Auto-fixing code...")
        print("=" * 60)

        # Black auto-format
        print("\n[EXEC] Running Black auto-format...")
        subprocess.run("uv run black src/ tests/", shell=True, cwd=self.project_root)

        # Ruff auto-fix
        print("\n[EXEC] Running Ruff auto-fix...")
        subprocess.run("uv run ruff check --fix src/ tests/", shell=True, cwd=self.project_root)

        print("\n[OK] Auto-fix complete!")
        print("[INFO] Now run quality_check.py again to verify")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="VVE BRAIN Quality Control")
    parser.add_argument("--fix", action="store_true", help="Auto-fix code issues")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    args = parser.parse_args()

    checker = QualityChecker()

    if args.fix:
        checker.auto_fix()
        return

    # Run quality checks
    success = checker.run_all()

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()