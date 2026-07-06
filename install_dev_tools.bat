@echo off
REM install_dev_tools.bat - Install development tools

echo ============================================================
echo 🧠 VVE BRAIN - Installing Development Tools
echo ============================================================

echo.
echo 📦 Installing black (code formatter)...
uv add --dev black

echo.
echo 📦 Installing ruff (linter)...
uv add --dev ruff

echo.
echo 📦 Installing pytest (testing)...
uv add --dev pytest pytest-cov

echo.
echo 📦 Installing pre-commit (optional)...
uv add --dev pre-commit

echo.
echo ============================================================
echo ✅ Development tools installed!
echo ============================================================
echo.
echo 📋 Usage:
echo   uv run python quality_check.py     - Run all quality checks
echo   uv run python quality_check.py --fix - Auto-fix issues
echo   uv run python github_push.py       - Quality check + push
echo   uv run pytest tests/               - Run tests
echo   uv run black src/ tests/           - Auto-format code
echo   uv run ruff check src/ tests/      - Lint code
echo.
pause