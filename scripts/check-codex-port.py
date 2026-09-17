#!/usr/bin/env python3
"""Validate the structural invariants of the Codex workflow port."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []

    agents_md = ROOT / "AGENTS.md"
    if not agents_md.is_file():
        errors.append("missing AGENTS.md")
    elif ".agents/skills/" not in agents_md.read_text(encoding="utf-8"):
        errors.append("AGENTS.md does not describe the Codex skill location")

    skills = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("no project skills found under .agents/skills")

    agent_files = sorted((ROOT / ".codex" / "agents").glob("*.toml"))
    if not agent_files:
        errors.append("no custom agents found under .codex/agents")

    required = {"name", "description", "developer_instructions"}
    for path in agent_files:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid TOML: {exc}")
            continue
        missing = required.difference(data)
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)}: missing {', '.join(sorted(missing))}"
            )

    if errors:
        print("Codex port validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Codex port validation: PASS ({len(skills)} skills, "
        f"{len(agent_files)} custom agents)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
