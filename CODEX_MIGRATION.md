# Codex migration

This workspace is a Codex-native port of `lovisareiche/codex-code-pedrohcgs` (upstream commit `9d371f0`). The academic workflow, templates, rules, skills, quality scripts, Git hooks, and CI definitions are retained.

## Compatibility map

| Upstream Claude surface | Codex surface | Status |
| --- | --- | --- |
| `CLAUDE.md` | `AGENTS.md` | Converted; Codex loads it as project guidance. |
| `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` | Converted; invoke with `$skill-name` or natural language. |
| `.claude/agents/*.md` | `.codex/agents/*.toml` | Converted to project-scoped custom agents. |
| `.claude/rules/` and `.claude/references/` | `.agents/rules/` and `.agents/references/` | Moved and relinked. Skills load relevant files progressively. |
| Claude tool names (`Read`, `Grep`, `Bash`, `Agent`) | Codex file, shell, web, and collaboration tools | Interpreted semantically. Claude-only frontmatter fields are retained as documentation and are not permission grants. |
| Slash skill calls such as `/verify-claims` | `$verify-claims` | Historical slash notation in long-form docs maps to the same named Codex skill. |
| `.claude/settings.json` permissions | Codex app/CLI permission controls | Not migrated. The unsafe `bypassPermissions` default was intentionally removed. |
| Claude lifecycle hooks and status line | Git hook, CI, and explicit scripts | No exact automatic port. Preserved under `.agents/hooks/` as reference; portable checks run through `scripts/backtest.sh`, `.githooks/pre-commit`, and GitHub Actions. |
| Claude model routing (Haiku/Sonnet/Opus) | Parent-model inheritance and Codex agent settings | Vendor-specific pins were dropped from generated agents. Configure models in `.codex/agents/*.toml` only when needed. |

## Using the workflow

Open this folder as a Codex project and start a new task so Codex loads `AGENTS.md` and discovers the skills and custom agents. Fill in the bracketed project metadata in `AGENTS.md`, then ask naturally for a workflow or invoke a skill explicitly, for example:

```text
$review-paper manuscript/main.tex
$data-analysis analyze the files in data/
$verify-claims draft.md --source paper.pdf
```

For repository-wide verification, run `bash scripts/backtest.sh` in a Bash-capable environment. On Windows, use Git Bash or WSL because the upstream gate runner and several helpers are shell scripts.

## Known limitations

- Imported prose still contains some historical Claude terminology, upstream URLs, and slash-command examples. These are provenance or documentation, not active configuration.
- Skills that explicitly depend on a Claude-only hook event, status line, `claude -p`, or a named third-party MCP server require a Codex-native replacement before that optional feature works.
- Custom agents were translated mechanically. Their task instructions are preserved, but tool allowlists from Claude frontmatter do not control Codex permissions.
- The generated HTML guide describes the upstream Claude edition. `AGENTS.md`, this migration note, `.agents/skills/`, and `.codex/agents/` are the authoritative Codex surfaces.

## Validation

The port includes `scripts/check-codex-port.py`, which checks that the Codex instruction file, skill tree, project agent TOML files, and core links are present and parseable.

