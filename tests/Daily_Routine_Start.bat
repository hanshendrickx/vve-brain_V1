@echo off
REM ============================================================
REM Daily_Routine_Start.bat - Daily Development Routine
REM ============================================================

title VVE BRAIN - Daily Routine
color 0A

echo.
echo ============================================================
echo VVE BRAIN - Daily Routine Start
echo ============================================================
echo.

REM Step 1: Check Environment
echo [1] Checking Environment...
echo ------------------------------------------------------------
python --version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.13+
    pause
    exit /b 1
) else (
    echo [OK] Python found
)

uv --version 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] uv not found!
    echo Please install uv
    pause
    exit /b 1
) else (
    echo [OK] uv found
)

if exist .venv (
    echo [OK] Virtual environment found
) else (
    echo [WARN] Virtual environment not found
    echo Creating virtual environment...
    uv venv
)

echo.
echo ------------------------------------------------------------
echo.

REM Step 2: Git Sync
echo [2] Checking Git Sync...
echo ------------------------------------------------------------
git status --porcelain >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Not a git repository!
    echo Please initialize git: git init
    pause
    exit /b 1
)

git status --short
if %errorlevel% equ 0 (
    echo.
    echo [OK] Checking for updates...
    git fetch
    git status -sb | find "behind" >nul
    if %errorlevel% equ 0 (
        echo [INFO] Remote has updates - pulling...
        git pull
    ) else (
        echo [OK] Local is up to date
    )
)

echo.
echo ------------------------------------------------------------
echo.

REM Step 3: Quality Checks
echo [3] Running Quality Checks...
echo ------------------------------------------------------------
uv run python quality_check.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Quality checks failed!
    echo Options:
    echo   1. Auto-fix and continue
    echo   2. Continue anyway (not recommended)
    echo   3. Stop and fix manually
    choice /c 123 /n /m "Enter choice (1-3): "
    if errorlevel 3 goto stop
    if errorlevel 2 goto skip_quality
    if errorlevel 1 goto auto_fix
)

:auto_fix
echo.
echo Running auto-fix...
uv run python quality_check.py --fix
goto continue

:skip_quality
echo.
echo [WARN] Continuing despite quality issues...
goto continue

:stop
echo.
echo [STOP] Please fix issues manually and restart.
pause
exit /b 0

:continue
echo.
echo ------------------------------------------------------------
echo.

REM Step 4: Start Project
echo [4] Starting VVE BRAIN...
echo ------------------------------------------------------------
uv run python run.py

echo.
echo ------------------------------------------------------------
echo.

REM Step 5: Open BRAIN Documentation
echo [5] Opening BRAIN Documentation...
echo ------------------------------------------------------------
if exist README_BRAIN\INDEX.html (
    start README_BRAIN\INDEX.html
    echo [OK] BRAIN opened in browser
) else (
    echo [WARN] INDEX.html not found
)

echo.
echo ============================================================
echo [OK] Daily Routine Complete!
echo ============================================================
echo.
echo Summary:
echo    Environment: OK
echo    Git Sync: OK
echo    Quality: Checked
echo    Project: Started
echo    BRAIN: Opened
echo.
echo Have a productive day!
echo ============================================================
pause