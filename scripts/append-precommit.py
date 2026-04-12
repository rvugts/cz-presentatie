#!/usr/bin/env python3
"""
Merge (append) language-specific pre-commit hook checks into main pre-commit hook.

This script intelligently merges language-specific pre-commit hook templates
into the main .git/hooks/pre-commit, avoiding duplicates and maintaining
idempotency.

Each language section is wrapped in comment markers to enable safe merging.

Usage:
  python scripts/append-precommit.py python
  python scripts/append-precommit.py terraform
"""

import os
import re
import sys
from pathlib import Path


def extract_language_section(template_file: str, language: str) -> str:
    """
    Extract language-specific section from pre-commit template.

    Looks for section marked with:
    # ============================================================================
    # <LANGUAGE> CHECKS (AUTO-GENERATED)
    # ============================================================================
    [code]

    Returns the full section including markers, or empty string if not found.
    """
    try:
        with open(template_file) as f:
            content = f.read()
    except FileNotFoundError:
        return ""

    # Look for language-specific section - match from language header to next language section or EOF
    # Pattern: captures from "# ============" through "# LANGUAGE CHECKS" to end or next "# [LANGUAGE] CHECKS"
    pattern = rf"# =+\n# {language.upper()} CHECKS.*?\n# =+\n(.*?)(?=\n# =+\n# [A-Z]+ CHECKS|\Z)"
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if match:
        # Return the section header plus captured content
        header_match = re.search(rf"# =+\n# {language.upper()} CHECKS.*?\n# =+", content, re.IGNORECASE)
        if header_match:
            return header_match.group(0) + "\n" + match.group(1).rstrip()

    return ""


def remove_language_section(hook_content: str, language: str) -> str:
    """Remove existing language section from pre-commit hook."""
    pattern = rf"# =+\n# {language.upper()} CHECKS.*?\n# =+\n.*?(?=\n# =|\Z)"
    return re.sub(pattern, "", hook_content, flags=re.IGNORECASE | re.DOTALL).strip()


def merge_precommit(language: str) -> None:
    """Merge language-specific pre-commit checks into main hook."""
    # Try language-specific template first, fall back to main template
    language_template = f".github/hooks/{language}-pre-commit.template"
    main_template = ".github/hooks/pre-commit.template"

    if Path(language_template).exists():
        template_file = language_template
    elif Path(main_template).exists():
        template_file = main_template
    else:
        print(f"⚠️  No pre-commit template found, skipping pre-commit merge")
        return

    hook_file = Path(".git/hooks/pre-commit")

    if not Path(template_file).exists():
        print(f"⚠️  {template_file} not found, skipping pre-commit merge")
        return

    # Extract language section from template
    language_section = extract_language_section(template_file, language)

    if not language_section:
        print(f"⚠️  No {language.upper()} section found in template, skipping")
        return

    # Read existing hook or create new one
    if hook_file.exists():
        with open(hook_file) as f:
            hook_content = f.read()

        # Check if language section already exists
        if f"{language.upper()} CHECKS" in hook_content:
            print(f"✅ {language.upper()} checks already in pre-commit hook, skipping")
            return
    else:
        # Create new hook with shebang and preamble
        hook_content = """#!/bin/bash

# Pre-commit Hook: Enforce Code Quality
# This hook runs language-specific checks to prevent commits that don't meet quality standards.

set -e

echo "🔍 Running pre-commit checks..."
echo ""
"""

    # Remove shebang/initial comments from language section if present
    lines = language_section.split('\n')
    if lines[0].startswith('#!/bin/bash'):
        lines = lines[1:]

    # Remove initial comment lines before first section marker
    while lines and not lines[0].startswith('# ='):
        lines.pop(0)

    language_section = '\n'.join(lines)

    # Append language section to hook
    merged = hook_content.rstrip() + '\n\n' + language_section + '\n'

    # Write back
    with open(hook_file, 'w') as f:
        f.write(merged)

    # Make executable
    os.chmod(hook_file, 0o755)

    print(f"✅ Merged {language.upper()} checks into pre-commit hook")


def main() -> None:
    """Merge pre-commit checks for specified language."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/append-precommit.py <language>")
        print("Example: python scripts/append-precommit.py python")
        sys.exit(1)

    language = sys.argv[1]
    print(f"🔧 Merging {language} pre-commit checks...")
    merge_precommit(language)


if __name__ == "__main__":
    main()
