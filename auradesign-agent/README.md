# Aura Designer Agent

**Aura Designer** — автономный программный комплекс для воссоздания веб-интерфейсов из любого источника (ссылка на живой сайт или изображение макета) на основе независимых дизайн-контрактов `AURADESIGN.md`.

Агент использует двухслойный подход к описанию интерфейсов: машиночитаемые токены YAML и высокоуровневые Markdown-инструкции для ИИ-верстальщика. Он независим от сторонних дизайн-брендов и глубоко интегрирован со сквозным циклом генерации безфоновой графики с помощью нейросетей.

---

## Основные возможности

1. **Source-first и copy-in-copy:** если пользователь дал сайт, скриншот или изображение, источник считается законом. Aura Designer сначала повторяет композицию, сетку, слои, формы, палитру, типографику, hero-структуру и адаптив максимально точно. Улучшения добавляются только после отдельного разрешения пользователя.
2. **Сканирование стилей (`aura_scanner.py`):** извлекает цветовую палитру, шрифты, контейнеры, размеры, настроение и визуальные паттерны с живого URL или изображения-образца, переводя их в точный дизайн-контракт `AURADESIGN.md`.
3. **Source Analyzer (`aura_source_analyzer.py`):** создает `AURA_SOURCE_MAP.json`, `AURA_COMPOSITION_LOCK.json`, `AURA_COMPONENT_MAP.json` и `AURA_SHAPE_MAP.json`. Эти файлы фиксируют заголовки, изображения, кнопки, компоненты, порядок слоев, композиционные ограничения и карту форм: кляксы, blobs, круги, капсулы, линии, рамки, тени и запреты на замену формы.
4. **Дизайн-контракт (`AURADESIGN_SPEC.md`):** фиксирует жесткие правила композиции для ИИ-верстальщика в едином документе-источнике правды. Контракт включает YAML-токены, Markdown-логику, правила цветов, типографику, сетку, motion, accessibility, asset policy, do/don't и QA.
5. **Подбор шрифтов:** для русскоязычных и мультиязычных проектов агент подбирает Google Fonts с поддержкой кириллицы и фиксирует shortlist в `AURA_FONT_MATCH.md`. Выбор шрифтов должен соответствовать источнику, а не личному вкусу агента.
6. **Репликация форм:** агент не заменяет форму на «примерно похожую». Если в источнике клякса, должна быть клякса; если круг, должен быть круг; если мягкий blob, должен быть blob. Для этого используются CSS, SVG, `clip-path`, border-radius, маски или MCP-ассеты.
7. **Модуль ассетов (`aura_asset_manager.py`):** работает как MCP Asset Gate: не выдает fallback-картинки и не имитирует генерацию, а требует реальный URL из `user-mcp-kv/gpt-image-2` и, для прозрачных объектов, `user-mcp-kv/recraft_remove_background`.
8. **Генератор сайтов (`aura_generator.py`):** превращает дизайн-контракт в чистую, интерактивную, адаптивную и готовую к публикации HTML-страницу с Tailwind, шрифтовым ритмом, плавными анимациями, inline SVG и полноценными секциями.
9. **Репликатор (`aura_replicator.py`):** генерирует HTML по `AURA_SOURCE_MAP.json` без архетипной вольности и без подмешивания старых стилей.
10. **Визуальное QA (`aura_visual_qa.py`):** создает `AURA_VISUAL_QA.md`, проверяет наличие обязательных файлов, source-map, shape-map, headline/image в HTML, placeholder, emoji, `AURA_VISUAL_DIFF.md` и `AURA_REVIEWER_PASS.md`.
11. **Linter (`aura_linter.py`):** проверяет `AURADESIGN.md` на обязательные разделы, достаточную глубину, source lock, asset rules, color psychology и отсутствие placeholder.
12. **Единая CLI-консоль (`aura.py`):** управляет всеми модулями в одно касание или запускает автоматический сквозной конвейер. Консоль очищена от emoji-выводов для стабильности на Windows и других ОС.

---

## Обязательные deliverables

Каждый серьезный прогон Aura Designer должен оставлять не только HTML, но и набор проверяемых артефактов:

- `AURADESIGN.md` — главный дизайн-контракт.
- `AURA_REPLICATION_TODO.md` — рабочий todo-list по словам пользователя и источнику.
- `AURA_SOURCE_ANALYSIS.md` — разбор композиции, слоев, сетки, hero, ассетов и motion.
- `AURA_SOURCE_MAP.json` — машинная карта источника.
- `AURA_COMPOSITION_LOCK.json` — ограничения композиции, которые нельзя самовольно менять.
- `AURA_COMPONENT_MAP.json` — карта компонентов и повторяющихся UI-паттернов.
- `AURA_SHAPE_MAP.json` — карта форм и запреты на style bleeding.
- `AURA_FONT_MATCH.md` — shortlist Google Fonts с кириллицей и выбранная пара.
- `AURA_BRAND_KIT_IMAGE_PROMPT.md` — prompt для brand-kit изображения через `gpt-image-2`.
- `AURA_COLOR_PSYCHOLOGY.md` — психология цвета и рекомендации, которые нельзя применять без разрешения пользователя.
- `AURA_ASSET_REGISTRY.json` — реестр URL ассетов, полученных через MCP KV.
- `AURA_VISUAL_DIFF.md` — visual-diff gate для side-by-side проверки source/result на 1440/768/375px.
- `AURA_REVIEWER_PASS.md` — обязательный второй проход `aura-design-reviewer`.
- `AURA_VISUAL_QA.md` — итоговый QA-отчет.

---

## Архитектура проекта

```
auradesign-agent/
├── aura.py                    # Главный пульт управления (CLI)
├── aura_scanner.py            # Анализатор веб-страниц и изображений
├── aura_source_analyzer.py    # Source-map, composition lock, component map, shape map
├── aura_generator.py          # Сборщик готовых HTML-страниц по контракту
├── aura_replicator.py         # Copy-in-copy HTML по source-map
├── aura_deliverables.py       # TODO, source analysis, font match, brand-kit, visual diff
├── aura_asset_manager.py      # MCP Asset Gate без fallback-картинок
├── aura_visual_qa.py          # QA отчет репликации
├── aura_linter.py             # Проверка AURADESIGN.md
├── AURADESIGN_SPEC.md         # Спецификация и стандарт формата AuraDesign
├── AURADESIGN.md              # Текущий рабочий дизайн-контракт
├── AURA_*.md / AURA_*.json    # Обязательные deliverables
└── index.html                 # Готовый собранный сайт
```

---

## Руководство по запуску

Инструмент написан на чистом Python 3 и **не требует сторонних библиотек** для парсинга и генерации. Для запуска достаточно установленного Python.

### 1. Source-first подход без пресетов
Папка пресетов удалена намеренно: готовые стили провоцировали style bleeding. Новый контракт создается из источника или вручную:
```bash
python aura.py scan --url https://linear.app --output AURADESIGN.md
```
*Файл спецификации будет записан в локальный `AURADESIGN.md`.*

### 2. Сканирование живого сайта
Запуск сканера для анализа любого интернет-ресурса (например, Linear или Stripe):
```bash
python aura.py scan --url https://linear.app --dark
```
*Интеллектуальный парсер выявит основные цвета, шрифты, замерит скругления и сформирует канонический `AURADESIGN.md` под стиль бренда.*

### 3. Генерация готового веб-интерфейса
Запуск сборки страницы по вашему текущему контракту `AURADESIGN.md`:
```bash
python aura.py generate --contract AURADESIGN.md --niche saas --asset-url "https://tempfile.aiquickdraw.com/r/generated-transparent.png" --output index.html
```
*Перед этой командой агент обязан вызвать MCP KV `gpt-image-2`, затем `recraft_remove_background`, зафиксировать результат в `AURA_ASSET_REGISTRY.json` и только после этого передать прозрачный PNG через `--asset-url`.*

### 4. Сквозной автоматический конвейер (Pipeline)
Запуск полной цепочки в один шаг: сканирование -> построение контракта -> подбор безфоновой графики -> генерация готового сайта:
```bash
python aura.py pipeline --url https://weather-site.com --output index.html
```

### 5. Точная репликация источника
Для copy-in-copy режима используется расширенная цепочка: анализ источника -> генерация карт -> репликация -> deliverables -> QA.
```bash
python aura.py analyze --url https://example.com --output-dir .
python aura.py replicate --source-map AURA_SOURCE_MAP.json --contract AURADESIGN.md --output index.html
python aura.py deliverables --contract AURADESIGN.md --source https://example.com --output-dir .
python aura.py qa --source-map AURA_SOURCE_MAP.json --html index.html --output-dir .
```

### 6. Проверка контракта
```bash
python aura.py lint --contract AURADESIGN.md
```

---

## Интеграция с ИИ и удаление фонов

Агент использует обязательную двухэтапную связку MCP KV для создания визуала в Hero-блоках:
1. **Генерация:** `user-mcp-kv/gpt-image-2` создает нужный объект или сцену.
2. **Очистка фона:** `user-mcp-kv/recraft_remove_background` возвращает прозрачный PNG.
3. **Реестр:** оба URL записываются в `AURA_ASSET_REGISTRY.json`.
4. **Размещение:** HTML использует только реальный URL из MCP KV.

Запрещены локальные Python/Pillow/crop/chroma key, stock/fallback URL и отчеты «ассет создан» без URL результата MCP KV.

---

## Визуальные gate-проверки

Перед тем как считать страницу готовой, агент обязан пройти несколько уровней проверки:

- `AURA_VISUAL_DIFF.md` — ручной или автоматизированный side-by-side gate: источник рядом с результатом на desktop, tablet и mobile.
- `AURA_REVIEWER_PASS.md` — второй проход `aura-design-reviewer`, который ищет style bleeding, неправильные формы, случайные тени, слабый hero, плохой контраст и сломанный адаптив.
- `AURA_VISUAL_QA.md` — итоговый отчет CLI-проверки.

Если source был задан, страница не считается готовой, пока форма, сетка, hero, шрифты, слои и ассеты не сверены с источником.

---

## Что запрещено

- Использовать пресеты и подмешивать прошлые стили вместо анализа источника.
- Добавлять черные контуры, глубокие тени, brutal-стиль или декоративные формы, которых нет в источнике.
- Менять форму объекта: круг на капсулу, blob на карточку, кляксу на звезду и так далее.
- Использовать emoji в интерфейсе. Допустимы только SVG, CSS-формы или сгенерированные ассеты.
- Вставлять stock/fallback-картинки вместо MCP KV результата.
- Делать «демо в рамке», если пользователь просит сайт на весь экран.
- Оставлять прозрачные primary-кнопки, черное на черном, белое на белом или нечитаемые ticker-ленты.
- Применять рекомендации из `AURA_COLOR_PSYCHOLOGY.md` без отдельного разрешения пользователя.
