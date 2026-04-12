#!/usr/bin/env python3
"""
Merge (append) language-specific Makefile targets into main Makefile.

This script intelligently appends targets from language-specific Makefile
templates into the main Makefile, avoiding duplicates and maintaining
idempotency.

Usage:
  python scripts/append-makefile.py python
  python scripts/append-makefile.py terraform
"""

import re
import sys
from pathlib import Path


def extract_targets(makefile_content: str) -> dict[str, str]:
    """
    Extract targets and their rules from Makefile content.

    Returns dict: {target_name: full_rule_text}
    """
    targets: dict[str, str] = {}
    lines: list[str] = makefile_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        # Match target: (lines that start with non-whitespace and contain :)
        if line and not line.startswith('\t') and not line.startswith(' ') and ':' in line:
            target_match = re.match(r'^([a-zA-Z0-9_-]+):', line)
            if target_match:
                target_name = target_match.group(1)
                # Collect this target and all its recipe lines (indented)
                rule_lines = [line]
                i += 1
                while i < len(lines) and lines[i] and (lines[i].startswith('\t') or lines[i].startswith(' ')):
                    rule_lines.append(lines[i])
                    i += 1
                targets[target_name] = '\n'.join(rule_lines)
                continue
        i += 1

    return targets


def merge_makefiles(language: str) -> None:
    """Merge language-specific Makefile targets into main Makefile."""
    template_file = Path(f"Makefile.{language}.template")
    main_file = Path("Makefile")

    if not template_file.exists():
        print(f"⚠️  {template_file} not found, skipping Makefile merge")
        return

    # Read template
    with open(template_file) as f:
        template_content = f.read()

    template_targets = extract_targets(template_content)

    if not template_targets:
        print(f"⚠️  No targets found in {template_file}, skipping")
        return

    # Read or create main Makefile
    if main_file.exists():
        with open(main_file) as f:
            main_content = f.read()
        main_targets: dict[str, str] = extract_targets(main_content)
    else:
        main_content = ""
        main_targets: dict[str, str] = {}

    # Merge: add new targets, skip if already exist
    added_targets: list[str] = []
    for target_name, rule in template_targets.items():
        if target_name not in main_targets:
            added_targets.append(target_name)
            main_targets[target_name] = rule
        else:
            # Target exists, skip to avoid overwriting
            pass

    if not added_targets:
        print(f"✅ All {language} Makefile targets already exist, skipping")
        return

    # Reconstruct Makefile with merged targets
    # Preserve original content and append new targets
    merged_content = main_content

    # Add new targets at the end
    if merged_content and not merged_content.endswith('\n'):
        merged_content += '\n'

    merged_content += '\n'.join([template_targets[t] for t in added_targets])
    if not merged_content.endswith('\n'):
        merged_content += '\n'

    with open(main_file, 'w') as f:
        f.write(merged_content)

    print(f"✅ Merged {language} Makefile targets: {', '.join(added_targets)}")


def main() -> None:
    """Merge Makefile targets for specified language."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/append-makefile.py <language>")
        print("Example: python scripts/append-makefile.py python")
        sys.exit(1)

    language = sys.argv[1]
    print(f"🔧 Merging {language} Makefile targets...")
    merge_makefiles(language)


if __name__ == "__main__":
    main()
