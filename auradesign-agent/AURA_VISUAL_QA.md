# AURA_VISUAL_QA

Статус: **PASS**
Source map: `auradesign-agent/AURA_SOURCE_MAP.json`
HTML: `auradesign-agent/index.html`

## Проверки

- Проверена структура source-map.
- Проверено наличие обязательных deliverables.
- Проверено наличие ключевого headline/image в HTML.
- Проверена доступность всех `<img src>` из HTML.
- Проверен `AURA_ASSET_REGISTRY.json` для MCP KV ассетов.
- Проверен overlap hero-person asset: низ фигуры должен уходить под второй блок, а не обрываться на синем фоне.
- Проверены placeholder/lorem/emoji markers.
- Screenshot diff требует запуска в Cursor/browser среде.

## Findings

- Критических структурных проблем не найдено.

## Что нужно для pixel-perfect QA

- Сделать screenshot источника и результата на 1440px, 768px, 375px.
- Проверить координаты hero image и headline side-by-side.
- Проверить масштаб, z-index, интервалы, сетку, цвета и mobile overflow.
