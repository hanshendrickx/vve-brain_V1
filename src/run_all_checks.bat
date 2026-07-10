uv run ruff check --fix --unsafe-fixes src/ tests/
uv sync
uv run ruff check --fix --unsafe-fixes src/ tests/
uv run black src/ tests/
uv run python quality_check.py
