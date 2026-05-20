# Карта Aura Designer

Эта карта показывает, из каких частей состоит агент и за что отвечает каждый слой.

## 1. Sub-agent слой

### `aura-designer`

Файл:

```text
.cursor/agents/aura-designer.md
```

Назначение:

- Создает и улучшает сайты.
- Пишет глубокие `AURADESIGN.md`.
- Работает в режиме copy-in-copy: сначала точно повторяет источник, потом предлагает улучшения.
- Создает обязательные deliverables: todo, source analysis, brand-kit prompt и психологию цвета.
- Генерирует или координирует ассеты.
- Следит за hero-блоками, типографикой, motion, адаптивом и визуальной целостностью.
- Может редактировать файлы проекта.

### `aura-design-reviewer`

Файл:

```text
.cursor/agents/aura-design-reviewer.md
```

Назначение:

- Работает в readonly-режиме.
- Проверяет страницу после генерации.
- Ищет визуальные ошибки: плохой контраст, прозрачные кнопки, сломанные картинки, слабую композицию, поверхностный `AURADESIGN.md`.
- Возвращает список правок перед публикацией.

## 2. CLI-слой

Файл:

```text
auradesign-agent/aura.py
```

Команды:

```bash
python aura.py scan --url https://example.com
python aura.py analyze --url https://example.com --output-dir .
python aura.py generate --contract AURADESIGN.md --asset-url https://mcp-generated-image.example/transparent.png --output index.html
python aura.py replicate --source-map AURA_SOURCE_MAP.json --contract AURADESIGN.md --output index.html
python aura.py deliverables --contract AURADESIGN.md --source https://example.com --output-dir .
python aura.py lint --contract AURADESIGN.md
python aura.py qa --source-map AURA_SOURCE_MAP.json --html index.html --output-dir .
python aura.py pipeline --url https://example.com --output index.html
```

## 3. Сканер

Файл:

```text
auradesign-agent/aura_scanner.py
```

Что делает:

- Анализирует URL или изображение.
- Извлекает базовые цвета, шрифты, паттерны и настроение.
- Создает стартовый `AURADESIGN.md` с правилами `Source Replication Doctrine` и `Composition Lock`.

## 4. Генератор сайта

Файл:

```text
auradesign-agent/aura_generator.py
```

Что делает:

- Читает YAML-токены и Markdown-логику из `AURADESIGN.md`.
- Определяет визуальный архетип.
- Генерирует готовый HTML/CSS сайт.
- Встраивает шрифты, SVG, анимации, карточки, формы и hero-блок.

## 5. Source Analyzer

Файл:

```text
auradesign-agent/aura_source_analyzer.py
```

Что делает:

- Создает `AURA_SOURCE_MAP.json`.
- Создает `AURA_COMPOSITION_LOCK.json`.
- Создает `AURA_COMPONENT_MAP.json`.
- Фиксирует заголовки, изображения, кнопки, цвета, шрифты, компоненты и первичные композиционные сигналы.

## 6. Репликатор

Файл:

```text
auradesign-agent/aura_replicator.py
```

Что делает:

- Генерирует HTML по `AURA_SOURCE_MAP.json`.
- Не использует архетипную вольность.
- Сохраняет принцип source-accurate layout.

## 7. Visual QA

Файл:

```text
auradesign-agent/aura_visual_qa.py
```

Что делает:

- Создает `AURA_VISUAL_QA.md`.
- Проверяет наличие source-map, deliverables, headline/image в HTML, placeholder и emoji.
- Готовит список проблем перед browser/screenshot diff.

## 8. Linter

Файл:

```text
auradesign-agent/aura_linter.py
```

Что делает:

- Проверяет `AURADESIGN.md` на обязательные разделы.
- Ищет слишком короткие контракты, отсутствие source lock, asset rules, color psychology и placeholder.

## 9. Менеджер ассетов

Файл:

```text
auradesign-agent/aura_asset_manager.py
```

Что делает:

- Не подбирает fallback-ассеты и не имитирует генерацию.
- Пропускает дальше только URL, реально полученный через MCP KV `user-mcp-kv/gpt-image-2` и `user-mcp-kv/recraft_remove_background`.
- Возвращает `RESULT_ASSET_URL` для генератора.

## 10. Генератор deliverables

Файл:

```text
auradesign-agent/aura_deliverables.py
```

Что делает:

- Создает `AURA_REPLICATION_TODO.md` — рабочий todo-list для точного повторения источника.
- Создает `AURA_SOURCE_ANALYSIS.md` — анализ композиции, слоев, сетки, hero и визуальных правил.
- Создает `AURA_BRAND_KIT_IMAGE_PROMPT.md` — готовый prompt для MCP `gpt-image-2`, чтобы получить одну большую brand-kit картинку.
- Создает `AURA_COLOR_PSYCHOLOGY.md` — анализ психологии цветов и рекомендации, которые нельзя применять без разрешения пользователя.

## 11. Project Skills

Папка:

```text
.cursor/skills/
```

Содержит точечные способности, которые не дают агенту скатываться в шаблоны:

- `aura-cyrillic-google-fonts` — большой каталог Google Fonts пар с поддержкой кириллицы и правила подключения.
- `aura-shape-replication` — копирование любых форм из источника: клякс, blobs, кругов, капсул, волн, карточек, линий, обводок и теней.

## 12. Пресеты удалены

Папка `auradesign-agent/presets/` удалена намеренно. Готовые стили навязывали прошлые паттерны и мешали copy-in-copy репликации. Aura Designer должен анализировать источник с чистого листа и повторять его, а не подгонять под `bumaga`, `saas` или другой старый шаблон.

## 13. Документация и примеры

```text
docs/install.md
docs/capabilities.md
docs/mcp-tools.md
examples/prompt-examples.md
```

Эти файлы нужны, чтобы пользователь GitHub сразу понял, как установить агента и какие задачи ему отдавать.
