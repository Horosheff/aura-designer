# Установка Aura Designer

Aura Designer распространяется как набор sub-agent файлов и CLI-ядро. Его можно поставить локально в один проект или глобально для всех проектов.

## Установка в Cursor

Быстрый установщик:

```bash
python install.py --target cursor --scope project --project-dir your-project
```

### Вариант 1: в конкретный проект

```bash
mkdir -p .cursor/agents
cp path/to/aura-designer/.cursor/agents/aura-designer.md .cursor/agents/
cp path/to/aura-designer/.cursor/agents/aura-design-reviewer.md .cursor/agents/
```

После этого в Cursor можно вызывать:

```text
/aura-designer создай AURADESIGN.md и страницу по этой ссылке
/aura-design-reviewer проверь страницу перед публикацией
```

### Вариант 2: глобально для всех проектов

```bash
mkdir -p ~/.cursor/agents
cp path/to/aura-designer/.cursor/agents/*.md ~/.cursor/agents/
```

Cursor читает пользовательские агенты из `~/.cursor/agents/`, а проектные агенты из `.cursor/agents/`.

## Установка в Claude Code

Быстрый установщик:

```bash
python install.py --target claude --scope project --project-dir your-project
```

Скопируйте совместимые agent-файлы:

```bash
mkdir -p .claude/agents
cp path/to/aura-designer/.claude/agents/*.md .claude/agents/
```

Основной агент:

```text
/aura-designer
```

QA-агент:

```text
/aura-design-reviewer
```

## Установка в Codex

Быстрый установщик:

```bash
python install.py --target codex --scope project --project-dir your-project
```

Скопируйте совместимые agent-файлы:

```bash
mkdir -p .codex/agents
cp path/to/aura-designer/.codex/agents/*.md .codex/agents/
```

## Установка CLI

CLI можно использовать отдельно от sub-agent режима:

```bash
cd path/to/aura-designer
python "auradesign-agent/aura.py" preset bumaga --output "auradesign-agent/AURADESIGN.md"
python "auradesign-agent/aura.py" generate --contract "auradesign-agent/AURADESIGN.md" --niche bumaga --output "auradesign-agent/index.html"
```

## Проверка установки

Попросите агента:

```text
/aura-designer проверь, что ты установлен, и покажи карту своих возможностей
```

Если агент найден, IDE должна запустить sub-agent с именем `aura-designer`.
