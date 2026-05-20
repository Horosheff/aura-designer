# Aura Designer от Kovcheg

**Aura Designer** — устанавливаемый sub-agent для Cursor, Claude Code и Codex, который превращает ссылку на сайт, скриншот, изображение или идею в глубокий `AURADESIGN.md` и полноценную адаптивную веб-страницу.

Агент создан для задач, где обычный AI-кодер делает «демо» или визуальный мусор: прозрачные кнопки, черное на черном, случайные картинки, короткий дизайн-файл и слабый hero-блок. Aura Designer фиксирует это через подробный дизайн-контракт, генерацию ассетов, правила контрастности и визуальное QA.

<p>
  <a href="docs/install.md#установка-в-cursor"><img alt="Установить в Cursor" src="https://img.shields.io/badge/Установить%20в-Cursor-000000?style=for-the-badge"></a>
  <a href="docs/install.md#установка-в-claude-code"><img alt="Установить в Claude Code" src="https://img.shields.io/badge/Установить%20в-Claude%20Code-5B35D5?style=for-the-badge"></a>
  <a href="docs/install.md#установка-в-codex"><img alt="Установить в Codex" src="https://img.shields.io/badge/Установить%20в-Codex-1F6FEB?style=for-the-badge"></a>
</p>

## Что делает агент

- Сканирует сайт или изображение и собирает стиль в `AURADESIGN.md`.
- Пишет не короткий «конспект», а глубокую дизайн-систему: цвета, типографика, сетка, компоненты, motion, ассеты, адаптив, accessibility, запреты и QA.
- Генерирует полноценную HTML-страницу, а не макет-превью.
- Координирует генерацию hero/case-study изображений через `gpt-image-2`, если инструмент доступен.
- Удаляет фон у ассетов через `recraft_remove_background`, если инструмент доступен.
- Проверяет визуальные провалы: черное на черном, белое на белом, прозрачные CTA, плохие ленты, случайные картинки, слабый hero.

## Карта агента

```text
Aura Designer
├─ Sub-agents
│  ├─ .cursor/agents/aura-designer.md          # основной агент-создатель
│  ├─ .cursor/agents/aura-design-reviewer.md   # readonly визуальный QA
│  ├─ .claude/agents/                          # копии для Claude Code
│  └─ .codex/agents/                           # копии для Codex
├─ CLI-ядро
│  └─ auradesign-agent/
│     ├─ aura.py                               # единая CLI-команда
│     ├─ aura_scanner.py                       # сканирование URL/изображений
│     ├─ aura_asset_manager.py                 # ассеты и прозрачные PNG fallback
│     ├─ aura_generator.py                     # HTML/CSS генератор
│     ├─ AURADESIGN_SPEC.md                    # спецификация формата
│     └─ presets/                              # библиотека дизайн-пресетов
├─ Документация
│  ├─ docs/install.md                          # установка в IDE
│  ├─ docs/agent-map.md                        # подробная карта агента
│  ├─ docs/capabilities.md                     # список возможностей
│  └─ docs/mcp-tools.md                        # инструменты изображений
└─ Примеры
   └─ examples/prompt-examples.md              # готовые промпты
```

Подробная карта: [`docs/agent-map.md`](docs/agent-map.md)  
Все возможности: [`docs/capabilities.md`](docs/capabilities.md)

## Быстрая установка

### Cursor

Скопируйте агентов в проект:

```bash
mkdir -p .cursor/agents
cp path/to/aura-designer/.cursor/agents/*.md .cursor/agents/
```

И вызывайте:

```text
/aura-designer сделай страницу по этому сайту и создай AURADESIGN.md
/aura-design-reviewer проверь итоговую страницу на визуальные ошибки
```

### Claude Code

```bash
mkdir -p .claude/agents
cp path/to/aura-designer/.claude/agents/*.md .claude/agents/
```

### Codex

```bash
mkdir -p .codex/agents
cp path/to/aura-designer/.codex/agents/*.md .codex/agents/
```

Полная инструкция: [`docs/install.md`](docs/install.md)

## Запуск CLI

CLI написан на Python 3 и не требует сторонних библиотек.

```bash
python "auradesign-agent/aura.py" preset bumaga --output "auradesign-agent/AURADESIGN.md"
python "auradesign-agent/aura.py" generate --contract "auradesign-agent/AURADESIGN.md" --niche bumaga --output "auradesign-agent/index.html"
```

Сквозной pipeline:

```bash
python "auradesign-agent/aura.py" pipeline --url "https://example.com" --output "auradesign-agent/index.html"
```

## Что такое AURADESIGN.md

`AURADESIGN.md` — главный контракт дизайна для ИИ-агента. Он состоит из двух слоев:

- YAML frontmatter: точные токены для цветов, типографики, spacing, radii, компонентов и motion.
- Markdown body: дизайнерская логика, настроение, правила композиции, доступность, поведение компонентов, asset policy и запреты.

Пример хорошего контракта лежит в [`AURADESIGN.md`](AURADESIGN.md), а эталон BUMAGA — в [`auradesign-agent/presets/bumaga.md`](auradesign-agent/presets/bumaga.md).

## Строгие правила Aura

- Никаких emoji в интерфейсе. Только SVG, CSS-формы или сгенерированные ассеты.
- Никаких прозрачных primary-кнопок, если это не осознанное решение с нормальной рамкой и контрастом.
- Никакого черного текста на черном фоне и белого текста на белом фоне.
- Hero-блок должен быть полноценным: композиция, заголовок, CTA, ассет, адаптив.
- Картинки должны быть сгенерированы или осознанно выбраны. Нельзя вставлять случайные плейсхолдеры.
- Если нужен объект в hero, фон должен быть удален.

## Лицензия

MIT. См. [`LICENSE`](LICENSE).