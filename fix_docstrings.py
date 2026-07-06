"""
fix_docstrings.py - Fix all invalid docstrings in src/ folder
"""

import os
from pathlib import Path

def fix_file(filepath):
    """Fix a single Python file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if first line is a bare string (not a docstring)
    lines = content.split('\n')
    if lines and lines[0].strip() and not lines[0].strip().startswith(('"""', "'''", '#', 'import', 'from')):
        # It's a bare string - wrap it in docstring markers
        first_line = lines[0].strip()
        lines[0] = f'"""{first_line}"""'
        new_content = '\n'.join(lines)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed: {filepath}")
        return True
    else:
        print(f"⏭️ Already correct: {filepath}")
        return False

def main():
    """Fix all Python files in src/"""
    src_dir = Path('src')
    tests_dir = Path('tests')
    
    print("=" * 60)
    print("🔧 Fixing Docstrings...")
    print("=" * 60)
    
    files_fixed = 0
    
    # Fix src files
    for filepath in src_dir.glob('*.py'):
        if fix_file(filepath):
            files_fixed += 1
    
    # Fix test files (if they have issues)
    for filepath in tests_dir.glob('*.py'):
        if fix_file(filepath):
            files_fixed += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Fixed {files_fixed} files")
    print("=" * 60)

if __name__ == "__main__":
    main()