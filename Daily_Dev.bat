# 1. Write code
# 2. Run quality checks
uv run python quality_check.py

# 3. If issues found, auto-fix
uv run python quality_check.py --fix

# 4. Push with checks
uv run python github_push.py