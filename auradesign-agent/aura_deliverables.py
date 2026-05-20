#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aura Designer - Deliverables Builder
====================================
Создает обязательные аналитические документы вокруг AURADESIGN.md:
todo-карту репликации, анализ источника, prompt для brand-kit изображения
и психологию цвета. Не вызывает MCP напрямую; sub-agent использует эти файлы
как строгий бриф для gpt-image-2 и recraft_remove_background.
"""

import argparse
import os
import re
import sys
from datetime import datetime


if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def read_text(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def write_text(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def extract_field(content, field, default=""):
    match = re.search(rf"^{re.escape(field)}:\s*(.+)$", content, re.MULTILINE)
    if not match:
        return default
    return match.group(1).strip().strip('"').strip("'")


def extract_colors(content):
    colors = []
    for color in re.findall(r"#[0-9a-fA-F]{6}", content):
        normalized = color.lower()
        if normalized not in colors:
            colors.append(normalized)
    return colors[:12]


def extract_fonts(content):
    fonts = []
    for font in re.findall(r'fontFamily:\s*["\']?([^"\']+)["\']?', content):
        clean = font.strip()
        if clean and clean not in fonts:
            fonts.append(clean)
    return fonts[:6]


def color_psychology(color):
    mapping = {
        "red": ("энергия, тревога, скорость, опасность, импульс", "использовать для срочных CTA, предупреждений и эмоционального напряжения"),
        "orange": ("драйв, тепло, креатив, дружелюбная активность", "использовать для живых акцентов, промо и playful-секций"),
        "yellow": ("внимание, оптимизм, сигнал, визуальный шум", "использовать дозированно для бейджей, маркеров и подсветки"),
        "green": ("рост, безопасность, природа, подтверждение", "использовать для успеха, доверия, органики и позитивных метрик"),
        "blue": ("доверие, технология, стабильность, рациональность", "использовать для интерфейсов, данных, ссылок и доверительных CTA"),
        "purple": ("премиальность, воображение, AI, мистичность", "использовать для инноваций, креатива и сложных продуктов"),
        "pink": ("экспрессия, смелость, молодежность, эмоциональность", "использовать для брендов с яркой идентичностью и bold-коммуникацией"),
        "black": ("сила, контраст, люкс, драматургия", "использовать как сцену для ярких акцентов, но строго контролировать читаемость"),
        "white": ("чистота, воздух, простота, редакционность", "использовать как базу и паузу между плотными блоками"),
        "gray": ("нейтральность, структура, фон, техничность", "использовать как поддерживающий слой, не как главный характер"),
    }

    value = color.lstrip("#")
    r = int(value[0:2], 16)
    g = int(value[2:4], 16)
    b = int(value[4:6], 16)

    if r > 230 and g > 230 and b > 230:
        key = "white"
    elif r < 35 and g < 35 and b < 35:
        key = "black"
    elif abs(r - g) < 18 and abs(g - b) < 18:
        key = "gray"
    elif r > 190 and g < 100 and b < 120:
        key = "red"
    elif r > 200 and 90 <= g <= 170 and b < 90:
        key = "orange"
    elif r > 200 and g > 180 and b < 100:
        key = "yellow"
    elif g > r and g > b:
        key = "green"
    elif b > r and b > g:
        key = "blue"
    elif r > 140 and b > 140:
        key = "purple" if b >= r else "pink"
    else:
        key = "gray"

    emotion, usage = mapping[key]
    return key, emotion, usage


def build_todo(source, output_html):
    return f"""# AURA_REPLICATION_TODO

Источник: `{source or "не указан"}`
Целевой файл страницы: `{output_html}`

## Обязательный порядок работы

- [ ] Зафиксировать источник как закон: не менять тему, композицию, изображения, палитру и смысл без явного запроса пользователя.
- [ ] Снять/получить визуальный референс источника: screenshot, URL snapshot или изображение.
- [ ] Разобрать композицию hero: где стоит изображение, где заголовок, какой слой сверху, какие перекрытия и пропорции.
- [ ] Создать глубокий `AURADESIGN.md`.
- [ ] Создать `AURA_SOURCE_ANALYSIS.md` с описанием композиции, иерархии, сетки, ассетов и motion.
- [ ] Создать brand-kit board через MCP KV `user-mcp-kv/gpt-image-2`: одна большая картинка с палитрой, шрифтами, UI-компонентами, фонами, паттернами и ассетами.
- [ ] Если на странице нужен вырезанный объект, сгенерировать изображение через MCP KV `user-mcp-kv/gpt-image-2`, удалить фон через MCP KV `user-mcp-kv/recraft_remove_background` и записать URL в `AURA_ASSET_REGISTRY.json`.
- [ ] Создать `AURA_COLOR_PSYCHOLOGY.md` и вынести туда предложения по улучшению цвета, не применяя их без разрешения пользователя.
- [ ] Собрать HTML-страницу как copy-in-copy репликацию источника.
- [ ] Проверить side-by-side: источник против результата.
- [ ] Исправить несовпадения: позиция, масштаб, слои, отступы, контраст, ассеты, адаптив.

## Запреты

- [ ] Не придумывать новый hero, если источник уже задан.
- [ ] Не менять центральное изображение, если пользователь не попросил.
- [ ] Не менять расположение заголовка за/перед изображением.
- [ ] Не вставлять random placeholder images.
- [ ] Не применять рекомендации из психологии цвета без подтверждения пользователя.
"""


def build_source_analysis(name, source, colors, fonts):
    return f"""# AURA_SOURCE_ANALYSIS

Проект: **{name}**
Источник: `{source or "не указан"}`

## Принцип репликации

Aura Designer работает в режиме **copy-in-copy**: исходная композиция является главным ограничением. Агент должен сначала повторить источник, а уже потом, если пользователь попросит, адаптировать тему, картинку или настроение.

## Что нужно зафиксировать перед версткой

| Область | Что фиксировать |
| --- | --- |
| Hero | Позиция изображения, слой заголовка, масштаб, фон, CTA, плотность воздуха |
| Заголовки | Размер, регистр, трекинг, line-height, перекрытия |
| Изображения | Тема, материал, цвет, обрезка, наличие/отсутствие фона |
| Палитра | Главные цвета, роли цветов, контрастные пары |
| Сетка | Max-width, колонки, safe margins, gap, вертикальный ритм |
| Компоненты | Кнопки, карточки, формы, навигация, бейджи |
| Motion | Ticker, hover, scroll reveal, float, transitions |
| Адаптив | Как композиция перестраивается на 375px, 768px, 1024px |

## Найденная палитра

{chr(10).join(f"- `{color}`" for color in colors) if colors else "- Цвета пока не извлечены автоматически."}

## Найденные шрифты

{chr(10).join(f"- `{font}`" for font in fonts) if fonts else "- Шрифты пока не извлечены автоматически."}

## Source Lock

Если источник показывает крупное изображение по центру, заголовок за изображением, диагональные ленты, конкретный порядок карточек или особую сетку, агент обязан повторить именно это. Любое улучшение выносится в рекомендации, но не применяется без разрешения.
"""


def build_brand_kit_prompt(name, source, colors, fonts):
    palette = ", ".join(colors) if colors else "extract exact palette from source"
    font_list = ", ".join(fonts) if fonts else "extract exact typography from source"
    return f"""# AURA_BRAND_KIT_IMAGE_PROMPT

Этот файл является брифом для MCP `gpt-image-2`. Агент должен сгенерировать **одну большую brand-kit картинку**, похожую на набор слайдов на одном холсте.

## Prompt для `gpt-image-2`

```text
Создай одну большую high-resolution brand-kit картинку для сайта/дизайн-системы "{name}".
Источник-референс: {source or "переданный скриншот или текущий AURADESIGN.md"}.

Картинка должна выглядеть как несколько аккуратных презентационных слайдов, разложенных на одном большом холсте.
Обязательно включи: цветовую палитру с HEX-подписями, примеры типографики, разбор hero-композиции, фоновые текстуры, состояния кнопок, стили карточек, поля форм, SVG/иконографику, spacing grid, motion notes, стиль изображений/ассетов, accessibility contrast pairs и mobile responsive preview.

Используй точную композицию и визуальный язык источника. Не придумывай новое направление бренда.
Если в источнике объект расположен в центре, а крупный заголовок находится за ним, покажи эту же логику слоев в hero breakdown.

Палитра: {palette}.
Шрифты: {font_list}.
Стиль: source-accurate, production design system, чистая editorial-раскладка, читаемые подписи, без emoji, без случайных stock images.
Соотношение сторон: 16:9 или шире.
Результат: одна отполированная brand-kit картинка.
```

## После генерации

1. Проверить, что brand-kit board соответствует источнику.
2. Если на board есть отдельный объект для hero, обязательно прогнать его через MCP KV `user-mcp-kv/recraft_remove_background` и записать URL в `AURA_ASSET_REGISTRY.json`.
3. Сохранить URL результата в отчет агента и в `AURA_SOURCE_ANALYSIS.md` при следующем обновлении.
"""


def build_color_psychology(name, colors):
    rows = []
    for color in colors:
        family, emotion, usage = color_psychology(color)
        rows.append(f"| `{color}` | {family} | {emotion} | {usage} |")

    table = "\n".join(rows) if rows else "| нет данных | нет данных | нет данных | сначала извлечь палитру из источника |"

    return f"""# AURA_COLOR_PSYCHOLOGY

Проект: **{name}**

## Важное правило

Этот документ содержит рекомендации. Они **не должны автоматически менять копию источника**. Если пользователь просит точное повторение, палитра источника сохраняется. Улучшения применяются только после отдельного подтверждения.

## Психология найденных цветов

| Цвет | Семейство | Эмоциональный эффект | Рекомендация |
| --- | --- | --- | --- |
{table}

## Как использовать анализ

- Если источник уже задан, сначала делается copy-in-copy.
- Если палитра конфликтует с задачей бизнеса, агент может предложить альтернативы.
- Если контраст плохой, агент обязан предложить безопасную пару `color/on-color`, но не ломать исходный стиль без разрешения.
- Для CTA лучше выбирать цвет с высокой заметностью и понятной эмоциональной ролью.
"""


def main():
    parser = argparse.ArgumentParser(description="Aura Designer deliverables builder")
    parser.add_argument("--contract", default="AURADESIGN.md", help="Путь к AURADESIGN.md")
    parser.add_argument("--source", default="", help="URL или описание источника")
    parser.add_argument("--output-dir", default=".", help="Папка для аналитических файлов")
    parser.add_argument("--html", default="index.html", help="Целевой HTML-файл")
    args = parser.parse_args()

    content = read_text(args.contract)
    name = extract_field(content, "name", "Aura Project")
    colors = extract_colors(content)
    fonts = extract_fonts(content)

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[Deliverables] Создание аналитических файлов для {name} ({stamp})")

    write_text(os.path.join(args.output_dir, "AURA_REPLICATION_TODO.md"), build_todo(args.source, args.html))
    write_text(os.path.join(args.output_dir, "AURA_SOURCE_ANALYSIS.md"), build_source_analysis(name, args.source, colors, fonts))
    write_text(os.path.join(args.output_dir, "AURA_BRAND_KIT_IMAGE_PROMPT.md"), build_brand_kit_prompt(name, args.source, colors, fonts))
    write_text(os.path.join(args.output_dir, "AURA_COLOR_PSYCHOLOGY.md"), build_color_psychology(name, colors))

    print("[OK] Deliverables созданы:")
    print(f"- {os.path.join(args.output_dir, 'AURA_REPLICATION_TODO.md')}")
    print(f"- {os.path.join(args.output_dir, 'AURA_SOURCE_ANALYSIS.md')}")
    print(f"- {os.path.join(args.output_dir, 'AURA_BRAND_KIT_IMAGE_PROMPT.md')}")
    print(f"- {os.path.join(args.output_dir, 'AURA_COLOR_PSYCHOLOGY.md')}")


if __name__ == "__main__":
    main()
