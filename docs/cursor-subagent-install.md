# Установка Aura Designer как sub-agent

Aura Designer распространяется как Markdown-файлы sub-agent. Их можно поставить в Cursor, Claude Code или Codex.

## Установка в проект

```bash
mkdir -p your-project/.cursor/agents
cp .cursor/agents/aura-designer.md your-project/.cursor/agents/
cp .cursor/agents/aura-design-reviewer.md your-project/.cursor/agents/
```

Вызов в Cursor:

```text
/aura-designer просканируй URL, создай AURADESIGN.md и собери страницу
/aura-design-reviewer проверь финальную страницу на контраст, адаптив и качество дизайна
```

## Глобальная установка

Скопируйте агентов в пользовательскую папку Cursor:

```bash
mkdir -p ~/.cursor/agents
cp .cursor/agents/*.md ~/.cursor/agents/
```

Глобальные агенты доступны во всех проектах текущего пользователя.

## Совместимые папки

В репозитории также есть:

```text
.claude/agents/
.codex/agents/
```

Это копии agent-файлов для сред, которые читают Claude/Codex-style директории.

## Поля frontmatter

Aura Designer использует официальный формат Cursor:

```yaml
name: aura-designer
description: Короткое описание, по которому IDE понимает, когда запускать агента
model: inherit
readonly: false
is_background: false
```

Используйте `aura-designer` для генерации и правок, а `aura-design-reviewer` для readonly-критики и QA.
