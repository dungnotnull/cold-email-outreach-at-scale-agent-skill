#!/usr/bin/env python3
"""validate_skills.py — structural validation for the cold-email-outreach-at-scale skill.

Checks that every skill file has valid frontmatter, required sections, and that the
knowledge updater script compiles. Exits with non-zero status on failure.

Run:
    python tests/validate_skills.py
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REQUIRED_SKILL_FILES = [
    "main.md",
    "sub-audience-analysis.md",
    "sub-sequence-designer.md",
    "sub-deliverability-scorer.md",
    "sub-compliance-check.md",
    "sub-quality-reviewer.md",
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _check_frontmatter(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    m = FRONTMATTER_RE.match(text)
    if not m:
        errors.append(f"{path.name}: missing YAML frontmatter")
        return errors
    fm = m.group(1)
    if "name:" not in fm:
        errors.append(f"{path.name}: frontmatter missing 'name'")
    if "description:" not in fm:
        errors.append(f"{path.name}: frontmatter missing 'description'")
    return errors


def _check_sections(path: Path, text: str, required: list[str]) -> list[str]:
    errors: list[str] = []
    lower = text.lower()
    for section in required:
        if section.lower() not in lower:
            errors.append(f"{path.name}: missing required section '{section}'")
    return errors


def _check_knowledge_updater_compiles() -> list[str]:
    errors: list[str] = []
    ku = ROOT / "tools" / "knowledge_updater.py"
    if not ku.exists():
        errors.append("tools/knowledge_updater.py: file missing")
        return errors
    code = ku.read_text(encoding="utf-8")
    try:
        ast.parse(code)
    except SyntaxError as exc:
        errors.append(f"tools/knowledge_updater.py: syntax error at line {exc.lineno}: {exc.msg}")
    # Guard against the old stub
    if "def fetch_entries()" in code and "return []" in code:
        errors.append("tools/knowledge_updater.py: fetch_entries() still contains dummy 'return []'")
    return errors


def _check_brain() -> list[str]:
    errors: list[str] = []
    brain = ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
    if not brain.exists():
        errors.append("SECOND-KNOWLEDGE-BRAIN.md: file missing")
        return errors
    text = brain.read_text(encoding="utf-8")
    if "Self-Update Protocol" not in text:
        errors.append("SECOND-KNOWLEDGE-BRAIN.md: missing 'Self-Update Protocol' section")
    if "knowledge_updater.py" not in text:
        errors.append("SECOND-KNOWLEDGE-BRAIN.md: does not reference knowledge_updater.py")
    return errors


def main() -> int:
    errors: list[str] = []

    for name in REQUIRED_SKILL_FILES:
        path = SKILLS_DIR / name
        if not path.exists():
            errors.append(f"{name}: file missing")
            continue
        text = _read(path)
        errors.extend(_check_frontmatter(path, text))

    # Main harness specific sections
    main_text = _read(SKILLS_DIR / "main.md")
    errors.extend(_check_sections(SKILLS_DIR / "main.md", main_text, [
        "Workflow", "Sub-skills Available", "Tools", "Output Format",
        "Quality Gates", "Go / No-Go", "Error Handling",
    ]))

    # Sub-skill common sections
    common_sections = ["Purpose", "Inputs", "Procedure", "Quality Gate"]
    for sub in REQUIRED_SKILL_FILES[1:]:
        text = _read(SKILLS_DIR / sub)
        errors.extend(_check_sections(SKILLS_DIR / sub, text, common_sections))

    errors.extend(_check_knowledge_updater_compiles())
    errors.extend(_check_brain())

    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("VALIDATION PASSED: all skill files, frontmatter, sections, and tooling are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
