#!/usr/bin/env python3
"""
github_push.py - Push VVE BRAIN to GitHub with Quality Control
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def run_command(cmd, description="", check=True):
    """Run a command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode == 0
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, False

def main():
    print("=" * 60)
    print("[BRAIN] or (blank) VVE BRAIN - GitHub Push with Quality Control")
    print("=" * 60)
    
    # Step 1: Run quality checks
    print("\n📋 Step 1: Running Quality Checks...")
    print("-" * 60)
    
    # Run quality_check.py
    stdout, stderr, success = run_command("uv run python quality_check.py", check=False)
    
    print(stdout)
    if stderr:
        print(stderr)
    
    if not success:
        print("\n[FAIL] Quality checks FAILED!")
        print("\nWhat would you like to do?")
        print("  1. Auto-fix and continue")
        print("  2. Push anyway (not recommended)")
        print("  3. Cancel")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🔧 Running auto-fix...")
            run_command("uv run python quality_check.py --fix")
            print("\n🔄 Running checks again...")
            run_command("uv run python quality_check.py")
        elif choice == "2":
            print("\n[WARN] Pushing despite quality issues...")
        else:
            print("\n[FAIL] Push cancelled.")
            sys.exit(0)
    
    # Step 2: Check git status
    print("\n📋 Step 2: Checking Git Status...")
    print("-" * 60)
    
    stdout, stderr, success = run_command("git status --porcelain")
    if not stdout and success:
        print("[OK] No changes to commit.")
        print("\n📤 Pushing to GitHub...")
        run_command("git push")
        print("\n[OK] Complete!")
        sys.exit(0)
    
    print("\nSUMMARY: Changes detected:")
    print(stdout)
    
    # Step 3: Commit
    print("\n📋 Step 3: Committing Changes...")
    print("-" * 60)
    
    default_msg = f"VVE BRAIN update - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    print(f"📝 Default message: '{default_msg}'")
    print("   Press Enter to use default, or type your own:")
    msg = input("> ").strip()
    if not msg:
        msg = default_msg
    
    # Add and commit
    run_command("git add .")
    stdout, stderr, success = run_command(f'git commit -m "{msg}"')
    print(stdout)
    
    # Step 4: Push
    print("\n📋 Step 4: Pushing to GitHub...")
    print("-" * 60)
    
    stdout, stderr, success = run_command("git push")
    print(stdout)
    
    if success:
        print("\n" + "=" * 60)
        print("[OK] SUCCESS! Code pushed to GitHub!")
        print(f"🌐 https://github.com/hanshendrickx/vve-brain_V1")
        print("=" * 60)
    else:
        print("\n[FAIL] Push failed!")
        print(stderr)

if __name__ == "__main__":
    main()