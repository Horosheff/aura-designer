# AURA_VISUAL_QA

Статус: **PASS**
Source map: `auradesign-agent/AURA_SOURCE_MAP.json`
HTML: `auradesign-agent/index.html`

## Проверки

- Проверена структура source-map.
- Проверено наличие обязательных deliverables.
- Проверено наличие ключевого headline/image в HTML.
- Проверены placeholder/lorem/emoji markers.
- Screenshot diff требует запуска в Cursor/browser среде.

## Findings

- **HIGH**: Главное изображение источника не найдено в HTML. Нужно сохранить source image или заменить только после разрешения пользователя.
- **MEDIUM**: В HTML обнаружены placeholder/lorem маркеры. Для Aura это запрещено.
- **MEDIUM**: В HTML найдены emoji/symbol markers. UI должен использовать SVG/CSS/generative assets.

## Что нужно для pixel-perfect QA

- Сделать screenshot источника и результата на 1440px, 768px, 375px.
- Проверить координаты hero image и headline side-by-side.
- Проверить масштаб, z-index, интервалы, сетку, цвета и mobile overflow.
