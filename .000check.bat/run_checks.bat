uv pip check || goto :error

echo.
echo [6] Security audit...
uv audit || goto :error

echo.
echo [7] Pytest...
uv run pytest || goto :error

echo.
echo ============================================================
echo ALL CHECKS PASSED
echo ============================================================
exit /b 0

:error
echo.
echo ============================================================
echo CHECKS FAILED
echo ============================================================
exit /b 1============================================================
VVE BRAIN - ALL CHECKS
============================================================

[1] Sync...
Resolved 46 packages...

[2] Format check...
All done!

[3] Ruff lint...
All checks passed!

[4] Type check...
Success!

[5] Dependency check...
All good!

[6] Security audit...
0 vulnerabilities found

[7] Pytest...
2 passed in 0.04s

============================================================
ALL CHECKS PASSED
============================================================

run C:\Users\hansh\VVE_BRAIN\src\check_all_data_eigenaren.py
uv run C:\Users\hansh\VVE_BRAIN\src\balance_sheet.py
run C:\Users\hansh\VVE_BRAIN\.000check.bat\run_checks.bat
uv run C:\Users\hansh\VVE_BRAIN\src\balance_sheet.py
uv run C:\Users\hansh\VVE_BRAIN\src\check_all_data_eigenaren.py
uv run C:\Users\hansh\VVE_BRAIN\src\code test_imports.py

