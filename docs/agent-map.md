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
python aura.py preset bumaga
python aura.py generate --contract AURADESIGN.md --niche bumaga --output index.html
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
- Создает стартовый `AURADESIGN.md`.

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

## 5. Менеджер ассетов

Файл:

```text
auradesign-agent/aura_asset_manager.py
```

Что делает:

- Подбирает прозрачные PNG fallback-ассеты.
- Координирует работу с `gpt-image-2` и `recraft_remove_background`, если они доступны в среде.
- Возвращает `RESULT_ASSET_URL` для генератора.

## 6. Пресеты

Папка:

```text
auradesign-agent/presets/
```

Содержит готовые дизайн-контракты:

- `bumaga.md` — яркий нео-брутализм, бумажные слои, сигнальные ленты.
- `saas.md` — чистый SaaS.
- `fintech.md` — темный технологичный интерфейс.
- `glassmorphism.md` — стекло, блюр, свет.
- `pets.md` — теплый pet/family стиль.
- `cosmic.md` — темный космический стиль.
- `alpinism.md` — научная винтажная экспедиция.

## 7. Документация и примеры

```text
docs/install.md
docs/capabilities.md
docs/mcp-tools.md
examples/prompt-examples.md
```

Эти файлы нужны, чтобы пользователь GitHub сразу понял, как установить агента и какие задачи ему отдавать.
