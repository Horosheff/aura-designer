# AURA_VISUAL_QA

Статус: **PASS**
Source map: `AURA_SOURCE_MAP.json`
HTML: `index.html`

## Проверки

- Проверена структура source-map.
- Проверено наличие обязательных deliverables.
- Проверено наличие `AURA_SHAPE_MAP.json` и `AURA_FONT_MATCH.md`.
- Проверены visual-diff gate и reviewer-pass артефакты.
- Проверено наличие ключевого headline/image в HTML.
- Проверена доступность всех `<img src>` из HTML.
- Проверен `AURA_ASSET_REGISTRY.json` для MCP KV ассетов.
- Проверен overlap hero-person asset: низ фигуры должен уходить под второй блок, а не обрываться на синем фоне.
- Проверены placeholder/lorem/emoji markers.
- Screenshot diff требует запуска в Cursor/browser среде.

## Findings

- **HIGH**: Главное изображение источника не найдено в HTML. Нужно сохранить source image или заменить только после разрешения пользователя.
- **MEDIUM**: В HTML обнаружены placeholder/lorem маркеры. Для Aura это запрещено.

## Что нужно для pixel-perfect QA

- Сделать screenshot источника и результата на 1440px, 768px, 375px.
- Заполнить `AURA_VISUAL_DIFF.md` по зонам Hero/Typography/Shapes/Spacing/Colors.
- Запустить `aura-design-reviewer` и заполнить `AURA_REVIEWER_PASS.md`.
- Проверить координаты hero image и headline side-by-side.
- Проверить масштаб, z-index, интервалы, сетку, цвета и mobile overflow.
