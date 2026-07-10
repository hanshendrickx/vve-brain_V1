uv sync

# 1. Fix linting
uv run ruff check --fix src/ tests/

# 2. Format code
uv run black src/ tests/

# 3. Run quality check
uv run python quality_check.py


