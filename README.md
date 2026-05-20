# Aura Designer

Aura Designer is a reusable Cursor subagent and Python CLI for turning a website URL, screenshot, or design idea into a deep `AURADESIGN.md` contract and a complete responsive website page.

Built by Kovcheg for high-quality AI-assisted interface generation.

## What Is Included

- `auradesign-agent/` — Python CLI runtime: scanner, contract generator, asset coordinator, HTML generator, presets.
- `.cursor/agents/aura-designer.md` — installable Cursor subagent that can edit UI code and generate Aura pages.
- `.cursor/agents/aura-design-reviewer.md` — readonly visual QA subagent for checking design quality and production readiness.
- `.claude/agents/` and `.codex/agents/` — compatibility copies for environments that read Claude/Codex-style agent folders.
- `.cursor/rules/aura-design.mdc` — project rule that keeps Cursor aligned with Aura Designer standards while developing the agent itself.
- `AURADESIGN.md` — current working design contract example.

## Install In Cursor

Project-level install:

```bash
mkdir -p .cursor/agents
cp .cursor/agents/aura-designer.md your-project/.cursor/agents/aura-designer.md
cp .cursor/agents/aura-design-reviewer.md your-project/.cursor/agents/aura-design-reviewer.md
```

Global install:

```bash
mkdir -p ~/.cursor/agents
cp .cursor/agents/*.md ~/.cursor/agents/
```

Invoke in Cursor:

```text
/aura-designer create a landing page from this URL and produce AURADESIGN.md
/aura-design-reviewer review the generated page for visual quality and contrast
```

## Run The CLI

The CLI uses Python 3 and currently has no required third-party packages.

```bash
cd auradesign-agent
python aura.py preset bumaga --output AURADESIGN.md
python aura.py generate --contract AURADESIGN.md --niche bumaga --output index.html
```

From the repository root:

```bash
python "auradesign-agent/aura.py" preset bumaga --output "auradesign-agent/AURADESIGN.md"
python "auradesign-agent/aura.py" generate --contract "auradesign-agent/AURADESIGN.md" --niche bumaga --output "auradesign-agent/index.html"
```

## Cursor Subagent Format

Aura Designer follows the official Cursor subagent format:

```markdown
---
name: aura-designer
description: Aura Designer by Kovcheg. Use proactively when creating or improving websites and AURADESIGN.md contracts.
model: inherit
readonly: false
is_background: false
---

Subagent prompt...
```

Project agents live in `.cursor/agents/`. User-global agents live in `~/.cursor/agents/`.

## Asset Tools

When running inside Cursor with MCP tools available, Aura Designer can coordinate:

- `gpt-image-2` for generated hero and case-study images.
- `recraft_remove_background` for transparent PNG assets.

The Python CLI includes high-quality transparent fallbacks so it can still run without MCP access.

## Design Rules

- No emojis in generated UI. Use inline SVG, CSS shapes, or generated assets.
- `AURADESIGN.md` must be detailed enough for another agent to reproduce the design.
- Full website pages only. Do not ship unfinished demo frames.
- Primary buttons must be readable, filled or intentionally outlined, and tested for contrast.
- Hero blocks require real composition, headline hierarchy, CTA pair, asset placement, and responsive behavior.
- Generated images must be intentional. Do not use random placeholder images when the user requested generated assets.

## Repository Hygiene

This repository intentionally excludes research dumps, cloned reference repositories, screenshots, local caches, and generated request files. The distributable package is the Aura Designer code, subagent definitions, rules, presets, docs, and example output.
