# AURA_BRAND_KIT_IMAGE_PROMPT

Этот файл является брифом для MCP `gpt-image-2`. Агент должен сгенерировать **одну большую brand-kit картинку**, похожую на набор слайдов на одном холсте.

## Prompt для `gpt-image-2`

```text
Создай одну большую high-resolution brand-kit картинку для сайта/дизайн-системы "Duong Minh Thanh Portfolio Design System".
Источник-референс: assets/c__Users_mrrut_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_a5e0597df6eb796fe0870877297bcf9f-67eb6b50-0cb7-4a9f-8b16-31247ce5124a.png.

Картинка должна выглядеть как несколько аккуратных презентационных слайдов, разложенных на одном большом холсте.
Обязательно включи: цветовую палитру с HEX-подписями, примеры типографики, разбор hero-композиции, фоновые текстуры, состояния кнопок, стили карточек, поля форм, SVG/иконографику, spacing grid, motion notes, стиль изображений/ассетов, accessibility contrast pairs и mobile responsive preview.

Используй точную композицию и визуальный язык источника. Не придумывай новое направление бренда.
Если в источнике объект расположен в центре, а крупный заголовок находится за ним, покажи эту же логику слоев в hero breakdown.

Палитра: #1153fc, #0a45d0, #ffffff, #facc15, #09122c, #9333ea, #e2e8f0, #ef4444.
Шрифты: Unbounded, Plus Jakarta Sans.
Стиль: source-accurate, production design system, чистая editorial-раскладка, читаемые подписи, без emoji, без случайных stock images.
Соотношение сторон: 16:9 или шире.
Результат: одна отполированная brand-kit картинка.
```

## После генерации

1. Проверить, что brand-kit board соответствует источнику.
2. Если на board есть отдельный объект для hero, обязательно прогнать его через MCP KV `user-mcp-kv/recraft_remove_background`.
3. Сохранить URL результата в отчет агента, `AURA_SOURCE_ANALYSIS.md` и `AURA_ASSET_REGISTRY.json`.

