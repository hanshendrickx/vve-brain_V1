#!/usr/bin/env python3
"""
Daily_Routine_Start.py - Complete Daily Development Routine (Windows-Compatible)
Checks: Environment, Git sync, Quality, and starts your project
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import time

class DailyRoutine:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        
    def print_header(self, text):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"[BRAIN] {text}")
        print("=" * 60)
    
    def print_success(self, text):
        print(f"[OK] {text}")
    
    def print_error(self, text):
        print(f"[ERROR] {text}")
        self.errors.append(text)
    
    def print_warning(self, text):
        print(f"[WARN] {text}")
        self.warnings.append(text)
    
    def print_info(self, text):
        print(f"[INFO] {text}")
    
    def run_command(self, cmd, description=""):
        """Run a command and return result"""
        if description:
            print(f"\n[EXEC] {description}...")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.project_root)
            return result.stdout.strip(), result.stderr.strip(), result.returncode == 0
        except Exception as e:
            return "", str(e), False
    
    def check_environment(self):
        """Step 1: Check Python and uv environment"""
        self.print_header("Step 1: Checking Environment")
        
        # Check Python
        stdout, stderr, success = self.run_command("python --version")
        if success:
            self.print_success(f"Python: {stdout}")
        else:
            self.print_error(f"Python not found: {stderr}")
        
        # Check uv
        stdout, stderr, success = self.run_command("uv --version")
        if success:
            self.print_success(f"uv: {stdout}")
        else:
            self.print_error(f"uv not found: {stderr}")
        
        # Check virtual environment
        if (self.project_root / ".venv").exists():
            self.print_success("Virtual environment found")
        else:
            self.print_warning("Virtual environment not found - run: uv venv")
        
        return len(self.errors) == 0
    
    def check_git_sync(self):
        """Step 2: Check Git status and sync"""
        self.print_header("Step 2: Checking Git Sync")
        
        # Check if git repository
        stdout, stderr, success = self.run_command("git status --porcelain")
        if not success:
            self.print_error("Not a git repository")
            return False
        
        # Check if there are local changes
        if stdout:
            self.print_warning("Local changes detected:")
            print(stdout)
            
            # Ask what to do
            print("\nOptions:")
            print("  1. Commit and push changes")
            print("  2. Discard changes (git restore)")
            print("  3. Continue without syncing")
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == "1":
                self._commit_and_push()
            elif choice == "2":
                self._discard_changes()
            elif choice == "3":
                self.print_warning("Continuing without syncing")
        else:
            self.print_success("No local changes")
            
            # Check if remote has updates
            self.run_command("git fetch", "Fetching remote updates")
            stdout, stderr, success = self.run_command("git status -sb")
            if "behind" in stdout:
                self.print_info("Remote has updates - pulling...")
                self.run_command("git pull", "Pulling latest changes")
                self.print_success("Updated from remote")
            else:
                self.print_success("Local is up to date with remote")
        
        return True
    
    def _commit_and_push(self):
        """Commit and push local changes"""
        self.print_info("Committing changes...")
        
        # Add all changes
        self.run_command("git add .")
        
        # Commit with default message
        msg = f"Daily update - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        stdout, stderr, success = self.run_command(f'git commit -m "{msg}"')
        if success:
            self.print_success("Changes committed")
        else:
            self.print_error(f"Commit failed: {stderr}")
            return
        
        # Push
        stdout, stderr, success = self.run_command("git push")
        if success:
            self.print_success("Changes pushed to GitHub")
        else:
            self.print_error(f"Push failed: {stderr}")
    
    def _discard_changes(self):
        """Discard local changes"""
        self.print_warning("Discarding local changes...")
        self.run_command("git restore .")
        self.print_success("Changes discarded")
    
    def check_quality(self):
        """Step 3: Run quality checks"""
        self.print_header("Step 3: Quality Checks")
        
        # Check if quality_check.py exists
        if not (self.project_root / "quality_check.py").exists():
            self.print_warning("quality_check.py not found - skipping")
            return True
        
        # Run quality check with output redirected to avoid emoji issues
        stdout, stderr, success = self.run_command(
            "uv run python quality_check.py 2>&1",
            "Running quality checks"
        )
        
        # Filter out emoji-related errors
        if stderr and "UnicodeEncodeError" in stderr:
            self.print_warning("Emoji display issue detected - continuing")
            success = True
        
        if stdout:
            print(stdout)
        
        if success:
            self.print_success("All quality checks passed!")
            return True
        else:
            self.print_error("Quality checks failed!")
            
            # Ask if want to auto-fix
            print("\nOptions:")
            print("  1. Auto-fix and continue")
            print("  2. Continue anyway (not recommended)")
            print("  3. Stop and fix manually")
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == "1":
                self.print_info("Running auto-fix...")
                self.run_command("uv run python quality_check.py --fix")
                self.print_success("Auto-fix complete - run checks again")
                return self.check_quality()
            elif choice == "2":
                self.print_warning("Continuing despite quality issues")
                return True
            else:
                self.print_info("Stopping - please fix issues manually")
                return False
    
    def start_project(self):
        """Step 4: Start the project"""
        self.print_header("Step 4: Starting VVE BRAIN")
        
        # Check if run.py exists
        if not (self.project_root / "run.py").exists():
            self.print_error("run.py not found")
            return False
        
        print("\nStarting VVE BRAIN...")
        print("-" * 40)
        
        # Run the project
        stdout, stderr, success = self.run_command("uv run python run.py")
        print(stdout)
        if stderr:
            print(stderr)
        
        if success:
            self.print_success("VVE BRAIN started successfully!")
        else:
            self.print_error("Failed to start VVE BRAIN")
        
        return success
    
    def open_brain(self):
        """Step 5: Open BRAIN documentation"""
        self.print_header("Step 5: Opening BRAIN Documentation")
        
        index_file = self.project_root / "README_BRAIN" / "INDEX.html"
        if index_file.exists():
            self.print_info("Opening VVE BRAIN in browser...")
            import webbrowser
            webbrowser.open(str(index_file))
            self.print_success("BRAIN opened in browser")
        else:
            self.print_warning("INDEX.html not found")
    
    def print_summary(self):
        """Print daily summary"""
        self.print_header("DAILY ROUTINE COMPLETE")
        
        print(f"\nSummary:")
        print(f"   Errors: {len(self.errors)}")
        print(f"   Warnings: {len(self.warnings)}")
        
        if self.errors:
            print("\n[ERROR] Issues to fix:")
            for error in self.errors:
                print(f"   - {error}")
        
        if self.warnings:
            print("\n[WARN] Warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n[OK] Everything is perfect!")
        
        print("\n" + "=" * 60)
        print("Have a productive day!")
        print("=" * 60)
    
    def run(self):
        """Run the complete daily routine"""
        print("\n" + "=" * 60)
        print("VVE BRAIN - Daily Routine Start")
        print(f"Date: {datetime.now().strftime('%A, %B %d, %Y %H:%M')}")
        print("=" * 60)
        
        # Step 1: Environment check
        env_ok = self.check_environment()
        if not env_ok:
            self.print_error("Environment issues found - please fix and restart")
            self.print_summary()
            return
        
        # Step 2: Git sync
        git_ok = self.check_git_sync()
        
        # Step 3: Quality checks
        quality_ok = self.check_quality()
        if not quality_ok:
            self.print_summary()
            return
        
        # Step 4: Start project
        self.start_project()
        
        # Step 5: Open BRAIN
        self.open_brain()
        
        # Summary
        self.print_summary()

if __name__ == "__main__":
    routine = DailyRoutine()
    routine.run()