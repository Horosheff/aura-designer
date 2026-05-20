# Installing Aura Designer As A Cursor Subagent

Aura Designer is distributed as Markdown subagent files.

## Project Install

Copy the agents into a project:

```bash
mkdir -p your-project/.cursor/agents
cp .cursor/agents/aura-designer.md your-project/.cursor/agents/
cp .cursor/agents/aura-design-reviewer.md your-project/.cursor/agents/
```

Use:

```text
/aura-designer scan this URL and create AURADESIGN.md plus the page
/aura-design-reviewer check the final page for contrast, responsiveness, and design quality
```

## Global Install

Copy the agents into the Cursor user folder:

```bash
mkdir -p ~/.cursor/agents
cp .cursor/agents/*.md ~/.cursor/agents/
```

Global agents are available in every Cursor project for the current user.

## Compatibility Folders

The repository also includes:

```text
.claude/agents/
.codex/agents/
```

These mirror the Cursor subagent definitions for environments that support Claude/Codex-style agent folders.

## Frontmatter Fields

Aura Designer uses the official Cursor fields:

```yaml
name: aura-designer
description: Short routing description used by Cursor for delegation
model: inherit
readonly: false
is_background: false
```

Use `aura-designer` for implementation and `aura-design-reviewer` for readonly critique.
