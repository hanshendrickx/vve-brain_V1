@echo off
REM ============================================================
REM github_push.bat - Push VVE BRAIN to GitHub
REM ============================================================

title VVE BRAIN - GitHub Push
color 0A

echo.
echo ============================================================
echo [BRAIN] or (blank) VVE BRAIN - GitHub Push
echo ============================================================
echo.
echo 📍 Current Directory: %CD%
echo.

REM Check if we're in a git repository
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Not a git repository!
    echo    Please run this from your project folder.
    pause
    exit /b 1
)

echo SUMMARY: Current Status:
echo.
git status --short

echo.
echo ============================================================
echo 📤 Choose an action:
echo ============================================================
echo.
echo 1. Add all files, commit, and push (Standard)
echo 2. Add all files, commit with custom message, and push
echo 3. Just push (if already committed)
echo 4. Pull latest changes (sync from GitHub first)
echo 5. Show status only
echo 6. Cancel
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto action_add_commit_push
if "%choice%"=="2" goto action_custom_message
if "%choice%"=="3" goto action_push_only
if "%choice%"=="4" goto action_pull
if "%choice%"=="5" goto action_status
if "%choice%"=="6" goto cancel
goto invalid

:action_add_commit_push
echo.
echo 📤 Adding all files...
git add .

echo.
echo 📝 Committing...
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg="VVE BRAIN update - %date% %time%"
git commit -m %commit_msg%

echo.
echo 📤 Pushing to GitHub...
git push
goto complete

:action_custom_message
echo.
echo 📤 Adding all files...
git add .

echo.
echo 📝 Enter your commit message:
set /p commit_msg="> "
if "%commit_msg%"=="" set commit_msg="VVE BRAIN update - %date% %time%"
git commit -m %commit_msg%

echo.
echo 📤 Pushing to GitHub...
git push
goto complete

:action_push_only
echo.
echo 📤 Pushing to GitHub...
git push
goto complete

:action_pull
echo.
echo 📥 Pulling latest changes from GitHub...
git pull
goto complete

:action_status
echo.
echo SUMMARY: Current Status:
echo.
git status
echo.
pause
goto complete

:invalid
echo.
echo [FAIL] Invalid choice. Please try again.
pause
goto complete

:cancel
echo.
echo [FAIL] Operation cancelled.
pause
goto complete

:complete
echo.
echo ============================================================
echo [OK] Complete!
echo ============================================================
echo.
echo 📂 Repository: https://github.com/hanshendrickx/vve-brain_V1
echo.
pause
