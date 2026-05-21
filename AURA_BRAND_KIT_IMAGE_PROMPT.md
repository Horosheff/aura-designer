# AURA_BRAND_KIT_IMAGE_PROMPT

Этот файл является брифом для MCP `gpt-image-2`. Агент должен сгенерировать **одну большую brand-kit картинку**, похожую на набор слайдов на одном холсте.

## Prompt для `gpt-image-2`

```text
Создай одну большую high-resolution brand-kit картинку для сайта/дизайн-системы "Language You+ Design System".
Источник-референс: assets/c__Users_mrrut_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_4c0d6218605807c704ded04f41921622-06e4fdca-3505-4a11-92a7-099c617cd735.png.

Картинка должна выглядеть как несколько аккуратных презентационных слайдов, разложенных на одном большом холсте.
Обязательно включи: цветовую палитру с HEX-подписями, примеры типографики, разбор hero-композиции, фоновые текстуры, состояния кнопок, стили карточек, поля форм, SVG/иконографику, spacing grid, motion notes, стиль изображений/ассетов, accessibility contrast pairs и mobile responsive preview.

Используй точную композицию и визуальный язык источника. Не придумывай новое направление бренда.
Если в источнике объект расположен в центре, а крупный заголовок находится за ним, покажи эту же логику слоев в hero breakdown.

Палитра: #6320ee, #5811ec, #fbe452, #fbe135, #141414, #5f5f5f, #a78bfa, #7c3aed, #ffffff, #f3f2f1, #fef3c7, #dcfce7.
Шрифты: Onest, Inter.
Стиль: source-accurate, production design system, чистая editorial-раскладка, читаемые подписи, без emoji, без случайных stock images.
Соотношение сторон: 16:9 или шире.
Результат: одна отполированная brand-kit картинка.
```

## После генерации

1. Проверить, что brand-kit board соответствует источнику.
2. Если на board есть отдельный объект для hero, обязательно прогнать его через MCP KV `user-mcp-kv/recraft_remove_background` и записать URL в `AURA_ASSET_REGISTRY.json`.
3. Сохранить URL результата в отчет агента и в `AURA_SOURCE_ANALYSIS.md` при следующем обновлении.
