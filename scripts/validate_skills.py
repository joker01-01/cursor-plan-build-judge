#!/usr/bin/env python3
"""Validate cross-platform Plan-Build-Judge skill packaging.

The repository intentionally publishes the same skill for Cursor and Claude
Code. This script fails when a platform copy is missing, when same-language
copies drift, or when core safety/interaction markers disappear.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PAIRS = {
    "English": (
        ROOT / ".cursor/skills/plan-build-judge/SKILL.md",
        ROOT / ".claude/skills/plan-build-judge/SKILL.md",
    ),
    "Chinese": (
        ROOT / ".cursor/skills/plan-build-judge-zh/SKILL.md",
        ROOT / ".claude/skills/plan-build-judge-zh/SKILL.md",
    ),
}

EXPECTED_NAMES = {
    "English": "plan-build-judge",
    "Chinese": "plan-build-judge-zh",
}

CORE_MARKERS = {
    "English": (
        "Planner",
        "Builder",
        "Judge",
        "disable-model-invocation: true",
        "Stop and wait for user confirmation",
        "actual evidence",
        "Do not automatically send work back to Builder",
    ),
    "Chinese": (
        "Planner",
        "Builder",
        "Judge",
        "disable-model-invocation: true",
        "停住，等待用户确认",
        "实际证据",
        "不要自动打回 Builder 返工",
    ),
}


def read_text(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"not valid UTF-8: {path.relative_to(ROOT)} ({exc})")
        return ""


def main() -> int:
    errors: list[str] = []

    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.is_file():
        errors.append("missing file: CLAUDE.md")

    for language, (cursor_path, claude_path) in PAIRS.items():
        cursor_text = read_text(cursor_path, errors)
        claude_text = read_text(claude_path, errors)

        if cursor_text and claude_text and cursor_text != claude_text:
            errors.append(
                f"{language} copies differ: "
                f"{cursor_path.relative_to(ROOT)} != "
                f"{claude_path.relative_to(ROOT)}"
            )

        text = cursor_text or claude_text
        if not text:
            continue

        expected_name = EXPECTED_NAMES[language]
        if f"name: {expected_name}" not in text:
            errors.append(f"{language} skill is missing name: {expected_name}")

        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append(f"{language} skill has invalid or missing YAML frontmatter")

        for marker in CORE_MARKERS[language]:
            if marker not in text:
                errors.append(f"{language} skill is missing core marker: {marker!r}")

    if errors:
        print("Skill validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    checked = sum(len(paths) for paths in PAIRS.values())
    print(f"Skill validation: PASS ({checked} skill files checked)")
    print("- Cursor and Claude Code copies match for English and Chinese")
    print("- Manual invocation, approval, evidence, and fail-stop markers are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
