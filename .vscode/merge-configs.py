#!/usr/bin/env python3
"""
Merge VS Code settings and extensions from language-specific configs.

This script is called by language setup scripts (e.g., enable-python.sh)
to merge language-specific VS Code configurations into the main settings.

Usage:
  python .vscode/merge-configs.py python
"""

import json
import re
import sys
from pathlib import Path


def load_jsonc(path: Path):
    """Load JSON or JSONC file by removing comments before parsing."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^\s*//.*$", "", text)
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    return json.loads(text)


def parse_jsonc_comments(path: Path):
    """Capture top-level leading comments for each key in a JSONC file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    comment_map = {}
    current = []
    top_comment = ""
    key_seen = False
    in_block = False

    key_pattern = re.compile(r'^(  )"(?P<key>[^"]+)"\s*:\s*')

    for line in lines:
        stripped = line.strip()

        if in_block:
            current.append(line)
            if "*/" in stripped:
                in_block = False
            continue

        if stripped.startswith("/*"):
            current.append(line)
            if "*/" not in stripped:
                in_block = True
            continue

        if stripped.startswith("//") or stripped == "":
            current.append(line)
            continue

        match = key_pattern.match(line)
        if match:
            key = match.group("key")
            if not key_seen:
                top_comment = "\n".join(current).rstrip()
                if top_comment:
                    top_comment += "\n\n"
            else:
                comment_map[key] = "\n".join(current).rstrip()
            key_seen = True
            current = []
            continue

        # Ignore other lines such as braces or array markers.

    return top_comment, comment_map


def dump_jsonc(path: Path, data: dict, top_comment: str, comment_map: dict) -> None:
    """Write JSON data while preserving top-level comment blocks."""
    with open(path, "w", encoding="utf-8") as f:
        if top_comment:
            f.write(top_comment)
        f.write("{\n")

        keys = list(data.keys())
        for index, key in enumerate(keys):
            comments = comment_map.get(key, "")
            if comments:
                f.write(f"{comments}\n")

            value_json = json.dumps(data[key], indent=2, ensure_ascii=False)
            value_lines = value_json.splitlines()
            if len(value_lines) == 1:
                f.write(f'  "{key}": {value_lines[0]}')
            else:
                f.write(f'  "{key}": {value_lines[0]}\n')
                for line in value_lines[1:]:
                    f.write(f"  {line}\n")

            if index < len(keys) - 1:
                f.write(",\n")
            else:
                f.write("\n")

        f.write("}\n")


def merge_extensions(language: str) -> None:
    """Merge language-specific extensions into main extensions.json."""
    vscode_dir = Path(".vscode")
    main_file = vscode_dir / "extensions.json"
    lang_file = vscode_dir / f"extensions.{language}.json"

    if not lang_file.exists():
        print(f"⚠️  {lang_file} not found, skipping extensions merge")
        return

    # Load both files
    main = load_jsonc(main_file)
    lang = load_jsonc(lang_file)

    # Merge recommendations (unique)
    merged_recs = list(dict.fromkeys(main["recommendations"] + lang["recommendations"]))

    # Write back
    with open(main_file, "w") as f:
        json.dump({"recommendations": merged_recs}, f, indent=2)

    print(f"✅ Merged {lang_file.name} → extensions.json ({len(merged_recs)} total)")


def merge_settings(language: str) -> None:
    """Merge language-specific settings into main settings.json."""
    vscode_dir = Path(".vscode")
    main_file = vscode_dir / "settings.json"
    lang_file = vscode_dir / f"settings.{language}.json"

    if not lang_file.exists():
        print(f"⚠️  {lang_file} not found, skipping settings merge")
        return

    # Load both files
    main = load_jsonc(main_file)
    lang = load_jsonc(lang_file)

    # Preserve top-level comments from the main settings file
    top_comment, comment_map = parse_jsonc_comments(main_file)

    # Merge: language-specific settings override main
    merged = {**main, **lang}

    # Write back while preserving comments on the main file
    dump_jsonc(main_file, merged, top_comment, comment_map)

    print(f"✅ Merged {lang_file.name} → settings.json")


def main() -> None:
    """Merge VS Code configs for a specific language."""
    if len(sys.argv) < 2:
        print("Usage: python .vscode/merge-configs.py <language>")
        print("Example: python .vscode/merge-configs.py python")
        sys.exit(1)

    language = sys.argv[1]

    print(f"🔧 Merging {language} VS Code configuration...")
    merge_extensions(language)
    merge_settings(language)
    print("✅ VS Code configuration updated!")


if __name__ == "__main__":
    main()
