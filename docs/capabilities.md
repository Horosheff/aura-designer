# Возможности Aura Designer

## Основные сценарии

### 0. Copy-in-copy репликация источника

Если пользователь дал источник, агент сначала повторяет его максимально точно.

```text
/aura-designer повтори этот hero copy-in-copy: изображение в центре, заголовок за изображением, без смены темы
```

Правила:

- источник является законом;
- композиция не улучшается без разрешения;
- если объект в центре, он остается в центре;
- если заголовок за изображением, он остается за изображением;
- порядок слоев, масштаб, сетка, фон и ритм копируются до любых творческих изменений.

### 1. Сайт по ссылке

Пользователь дает URL. Агент анализирует стиль, пишет `AURADESIGN.md`, подбирает ассеты и собирает страницу.

```text
/aura-designer сделай страницу по https://example.com, сохрани стиль и создай AURADESIGN.md
```

### 2. Сайт по скриншоту

Пользователь дает изображение. Агент извлекает визуальную систему: палитру, сетку, типографику, блоки, плотность, настроение.

```text
/aura-designer возьми этот скриншот как референс и пересобери страницу
```

### 3. Глубокий дизайн-контракт

Агент пишет не короткий файл, а полноценную спецификацию:

- YAML-токены.
- Правила применения цветов.
- Типографика.
- Сетка.
- Компоненты.
- Motion.
- Ассеты.
- Accessibility.
- Do/Don't.
- QA checklist.
- Prompt integration для других AI-агентов.

### 3.1. Обязательные deliverables

Каждый серьезный прогон должен создавать:

- `AURADESIGN.md` — дизайн-контракт.
- `AURA_REPLICATION_TODO.md` — рабочий todo-list по словам пользователя и источнику.
- `AURA_SOURCE_ANALYSIS.md` — разбор композиции, слоев, ассетов, сетки, hero и motion.
- `AURA_BRAND_KIT_IMAGE_PROMPT.md` — prompt для генерации brand-kit картинки через MCP.
- `AURA_COLOR_PSYCHOLOGY.md` — психология цвета и рекомендации.

Команда:

```bash
python "auradesign-agent/aura.py" analyze --url "https://example.com" --output-dir "."
python "auradesign-agent/aura.py" replicate --source-map "AURA_SOURCE_MAP.json" --contract "AURADESIGN.md" --output "index.html"
python "auradesign-agent/aura.py" deliverables --contract "AURADESIGN.md" --source "https://example.com" --output-dir "."
python "auradesign-agent/aura.py" qa --source-map "AURA_SOURCE_MAP.json" --html "index.html" --output-dir "."
```

### 3.2. Brand-kit image

Агент должен готовить или генерировать одну большую brand-kit картинку: много мини-слайдов на одном холсте.

На картинке должны быть:

- палитра с HEX;
- шрифты и примеры заголовков;
- фоны и текстуры;
- кнопки и состояния;
- карточки и формы;
- сетка и spacing;
- hero composition breakdown;
- image/asset style;
- mobile preview;
- accessibility/contrast pairs.

### 4. Генерация ассетов

Для новых изображений агент обязан использовать MCP KV:

- `user-mcp-kv/gpt-image-2` для генерации изображений.
- `user-mcp-kv/recraft_remove_background` для удаления фона.

Если MCP KV недоступен, агент останавливает задачу и сообщает блокер. Fallback-ассеты, Python/Pillow/crop/chroma key и stock-картинки запрещены для новых hero/case-study/person/object изображений.

### 5. Полноценная страница

Агент должен выдавать именно сайт:

- шапка,
- hero,
- секции преимуществ,
- кейсы,
- CTA,
- форма или demo-блок,
- footer,
- адаптив.

Нельзя отдавать «демо в рамке», если пользователь просит сайт.

### 6. Визуальное QA

`aura-design-reviewer` проверяет:

- черное на черном,
- белое на белом,
- прозрачные primary-кнопки,
- плохой hero,
- нечитаемые ticker-ленты,
- случайные изображения,
- отсутствие удаления фона,
- сломанный mobile layout,
- слишком короткий `AURADESIGN.md`.

## Что агент не должен делать

- Не использовать emoji в интерфейсе.
- Не вставлять случайные картинки вместо генерации.
- Не оставлять `Lorem ipsum`.
- Не делать «презентационный мокап», если нужен сайт.
- Не писать короткий дизайн-файл на 20 строк.
- Не смешивать стили без системы.
- Не применять рекомендации психологии цвета без разрешения пользователя.

## Команды CLI

```bash
python "auradesign-agent/aura.py" scan --url "https://example.com" --output "AURADESIGN.md"
python "auradesign-agent/aura.py" analyze --url "https://example.com" --output-dir "."
python "auradesign-agent/aura.py" preset bumaga --output "AURADESIGN.md"
python "auradesign-agent/aura.py" generate --contract "AURADESIGN.md" --niche bumaga --output "index.html"
python "auradesign-agent/aura.py" replicate --source-map "AURA_SOURCE_MAP.json" --contract "AURADESIGN.md" --output "index.html"
python "auradesign-agent/aura.py" deliverables --contract "AURADESIGN.md" --source "https://example.com" --output-dir "."
python "auradesign-agent/aura.py" lint --contract "AURADESIGN.md"
python "auradesign-agent/aura.py" qa --source-map "AURA_SOURCE_MAP.json" --html "index.html" --output-dir "."
python "auradesign-agent/aura.py" pipeline --url "https://example.com" --output "index.html"
```
