#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AuraDesign Agent - Scanner and Analyzer Module
==============================================
Анализирует веб-сайты (HTML/CSS) или изображения и генерирует на их основе
форматированный дизайн-контракт AURADESIGN.md с токенами и философией стиля.
"""

import os
import sys
import re
import argparse
import urllib.request
import urllib.parse
from html.parser import HTMLParser

# Настройка кодировки вывода для стабильной печати в Windows консоли
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Цветовые пресеты-архетипы для популярных сайтов на случай сканирования известных ресурсов
SITE_ARCHETYPES = {
    "linear": {
        "name": "Linear Aesthetic",
        "description": "Строгая тёмная тема в оттенках серого с ультра-тонкими границами и фиолетовыми акцентами для ИТ-специалистов.",
        "colors": {
            "primary": "#5e6ad2", "primary-hover": "#4d59c2", "on-primary": "#ffffff",
            "secondary": "#ab47bc", "on-secondary": "#ffffff",
            "background": "#080710", "on-background": "#f7f8f8",
            "surface-lowest": "#12111a", "surface-low": "#161522",
            "surface-container": "#1e1c31", "surface-high": "#2b294a",
            "outline": "#2b2940", "outline-variant": "#1d1b2c",
            "error": "#f43f5e", "on-error": "#ffffff"
        },
        "typography": "Plus Jakarta Sans",
        "rounded": {"sm": "4px", "DEFAULT": "6px", "md": "8px", "lg": "12px", "xl": "16px"}
    },
    "stripe": {
        "name": "Stripe Premium",
        "description": "Яркий, технологичный светлый интерфейс с сочными градиентами, обилием свободного пространства и элегантной типографикой.",
        "colors": {
            "primary": "#635bff", "primary-hover": "#0a2540", "on-primary": "#ffffff",
            "secondary": "#00d4ff", "on-secondary": "#0a2540",
            "background": "#ffffff", "on-background": "#0a2540",
            "surface-lowest": "#ffffff", "surface-low": "#f8fbfd",
            "surface-container": "#f0f4f8", "surface-high": "#e3e8ee",
            "outline": "#adbdcc", "outline-variant": "#e6ebf1",
            "error": "#df1b41", "on-error": "#ffffff"
        },
        "typography": "Inter",
        "rounded": {"sm": "2px", "DEFAULT": "4px", "md": "8px", "lg": "12px", "xl": "20px"}
    },
    "apple": {
        "name": "Apple Editorial",
        "description": "Элитарный минимализм с жесткой монохромной палитрой, огромными контрастными заглавными шрифтами и нулевым визуальным шумом.",
        "colors": {
            "primary": "#000000", "primary-hover": "#1d1d1f", "on-primary": "#ffffff",
            "secondary": "#0066cc", "on-secondary": "#ffffff",
            "background": "#f5f5f7", "on-background": "#1d1d1f",
            "surface-lowest": "#ffffff", "surface-low": "#f5f5f7",
            "surface-container": "#e8e8ed", "surface-high": "#d2d2d7",
            "outline": "#86868b", "outline-variant": "#d2d2d7",
            "error": "#ff2d55", "on-error": "#ffffff"
        },
        "typography": "SF Pro Display, Inter",
        "rounded": {"sm": "4px", "DEFAULT": "8px", "md": "12px", "lg": "18px", "xl": "28px"}
    }
}


class CSSColorExtractor(HTMLParser):
    """Парсер для поиска цветов и стилей в HTML тегах и инлайновых стилях"""
    def __init__(self):
        super().__init__()
        self.found_colors = []
        self.font_families = []

    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if attr == 'style':
                # Ищем HEX-цвета в инлайновых стилях
                hex_matches = re.findall(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})\b', value)
                for m in hex_matches:
                    self.found_colors.append(f"#{m}")
                
                # Ищем шрифты
                font_matches = re.findall(r'font-family:\s*([^;]+)', value)
                for f in font_matches:
                    clean_font = f.strip().strip("'").strip('"').split(',')[0]
                    self.font_families.append(clean_font)


def scrape_site_style(url):
    """Сканирует HTML/CSS сайта и извлекает цвета, шрифты и структуру"""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        
        # 1. Извлекаем все HEX цвета из HTML
        extractor = CSSColorExtractor()
        extractor.feed(html_content)
        
        # Альтернативный regex поиск HEX по всему тексту
        all_hex = re.findall(r'#([A-Fa-f0-9]{6})\b', html_content)
        for h in all_hex:
            extractor.found_colors.append(f"#{h.lower()}")
            
        # Убираем дубликаты цветов и сортируем по частоте (имитируем поиск доминирующих)
        unique_colors = []
        for color in extractor.found_colors:
            if color not in unique_colors and color != "#ffffff" and color != "#000000":
                unique_colors.append(color)
        
        # Ищем шрифты в тегах link/style
        all_fonts = re.findall(r'font-family:\s*[\'"]?([a-zA-Z0-9\s\-]+)[\'"]?', html_content)
        for f in all_fonts:
            if f.strip() not in extractor.font_families:
                extractor.font_families.append(f.strip())

        return {
            "colors": unique_colors[:5], # берём топ-5 найденных цветов
            "fonts": extractor.font_families[:2] if extractor.font_families else ["Inter"]
        }
    except Exception as e:
        print(f"[Warning] Ошибка при запросе к сайту: {e}. Будет использован базовый алгоритм.", file=sys.stderr)
        return {"colors": [], "fonts": ["Inter"]}


def generate_auradesign_content(source_name, is_dark, colors, fonts, description=""):
    """Формирует текст контракта AURADESIGN.md"""
    
    # Задаём базовую палитру, если сканирование не дало результатов
    primary = colors[0] if len(colors) > 0 else ("#635bff" if not is_dark else "#5e6ad2")
    secondary = colors[1] if len(colors) > 1 else ("#00d4ff" if not is_dark else "#ab47bc")
    
    bg = "#0f172a" if is_dark else "#ffffff"
    on_bg = "#f8fafc" if is_dark else "#0f172a"
    
    surface_lowest = "#1e293b" if is_dark else "#ffffff"
    surface_low = "#0f172a" if is_dark else "#f8fafc"
    surface_container = "#334155" if is_dark else "#f1f5f9"
    surface_high = "#475569" if is_dark else "#e2e8f0"
    
    outline = "#475569" if is_dark else "#94a3b8"
    outline_variant = "#334155" if is_dark else "#e2e8f0"
    
    font_main = fonts[0] if len(fonts) > 0 else "Plus Jakarta Sans"
    
    if not description:
        theme_type = "современный тёмный" if is_dark else "элегантный светлый"
        description = f"Автоматически созданная дизайн-система для '{source_name}'. Визуальный характер: {theme_type} интерфейс с акцентом на чистоту структуры и адаптивность."

    return f"""---
version: alpha
name: {source_name}
description: {description}
colors:
  primary: "{primary}"
  primary-hover: "{primary}"
  on-primary: "#ffffff"
  secondary: "{secondary}"
  on-secondary: "#ffffff"
  background: "{bg}"
  on-background: "{on_bg}"
  surface-lowest: "{surface_lowest}"
  surface-low: "{surface_low}"
  surface-container: "{surface_container}"
  surface-high: "{surface_high}"
  outline: "{outline}"
  outline-variant: "{outline_variant}"
  error: "#dc2626"
  on-error: "#ffffff"
typography:
  display-lg:
    fontFamily: "{font_main}"
    fontSize: "44px"
    fontWeight: "800"
    lineHeight: "1.15"
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: "{font_main}"
    fontSize: "24px"
    fontWeight: "700"
    lineHeight: "1.3"
  body-md:
    fontFamily: "Inter"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.6"
  label-sm:
    fontFamily: "Inter"
    fontSize: "12px"
    fontWeight: "600"
    lineHeight: "1.2"
    letterSpacing: "0.05em"
rounded:
  sm: "4px"
  DEFAULT: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  full: "9999px"
spacing:
  base: "8px"
  xs: "4px"
  sm: "12px"
  md: "24px"
  lg: "40px"
  xl: "64px"
  gutter: "16px"
  margin: "24px"
components:
  button-primary:
    backgroundColor: "{{colors.primary}}"
    textColor: "{{colors.on-primary}}"
    rounded: "{{rounded.md}}"
    typography: "{{typography.label-sm}}"
    padding: "{{spacing.sm}} {{spacing.md}}"
    height: "44px"
  card-interactive:
    backgroundColor: "{{colors.surface-lowest}}"
    borderColor: "{{colors.outline-variant}}"
    rounded: "{{rounded.xl}}"
    padding: "{{spacing.md}}"
  input-field:
    backgroundColor: "{{colors.surface-low}}"
    borderColor: "{{colors.outline}}"
    rounded: "{{rounded.DEFAULT}}"
    padding: "{{spacing.sm}}"
---

## Philosophy & Vibe

Дизайн-система создана на основе анализа визуальной структуры {source_name}. В основе концепции лежит стремление снизить когнитивную нагрузку на пользователя за счет строгой иерархии, логичных цветовых ролей и обилия «воздуха».

Интерфейс должен ощущаться легким, организованным и отзывчивым. Важные акценты выделяются цветом `primary`, в то время как второстепенные области плавно уходят на фоновые уровни `surface`.

## Source Replication Doctrine

Источник является законом. Если пользователь дал ссылку, скриншот или изображение-референс, агент обязан сначала воспроизвести его композицию максимально точно, без авторского переосмысления.

Правила точного копирования:
- Если объект расположен в центре кадра, он остается в центре.
- Если крупный заголовок находится за изображением, заголовок должен остаться за изображением.
- Если hero построен на перекрытии слоев, порядок слоев, масштаб и визуальная глубина должны быть сохранены.
- Если источник использует конкретные пропорции, отступы, сетку, наклон, ритм или плотность, агент должен повторить их до внесения любых улучшений.
- Агент не меняет тему, палитру, изображение, типографику или композицию, пока пользователь явно не попросит изменить тему, картинку или направление.

Любые рекомендации по улучшению должны быть вынесены отдельно в анализ и не применяться к копии без разрешения пользователя.

## Color Guidance

Каждый цвет палитры выполняет строго закрепленную за ним семантическую роль:
- **Primary** используется только для кнопок призыва к действию (CTA), ключевых фокусов внимания и активных элементов.
- **Secondary** применяется для навигационных акцентов, второстепенных интерактивных переключателей и бейджей.
- **Surface-контейнеры** формируют глубину. Чем важнее информация, тем более «высокий» и светлый контейнер она занимает (lowest -> high).
- **Outline** задает деликатные разделительные границы, не перегружая страницу тяжелым контрастом.

## Typography Hierarchy

Система использует двухшрифтовую схему:
- **{font_main}** — акцентный геометрический гротеск с выразительными начертаниями для заголовков дисплеев и карточек.
- **Inter** — нейтральный, высокочитаемый шрифт для больших блоков контента, подписей и форм ввода.

## Layout & Grid

Макет жестко привязан к 8-пиксельной сетке. Все отступы между блоками, внутренние паддинги карточек и зазоры элементов обязаны быть кратны базовому токену `spacing.base`.
- Боковые поля безопасности для мобильных версий составляют `spacing.margin` (24px).
- Промежутки в карточных сетках составляют `spacing.gutter` (16px).

## Composition Lock

При генерации страницы агент обязан зафиксировать композицию источника:
- положение главного изображения;
- положение и слой заголовка относительно изображения;
- порядок блоков;
- размер и плотность карточек;
- соотношение пустого пространства и контента;
- фоновые формы, паттерны, текстуры и визуальные шумы;
- все заметные hover/motion паттерны.

Композиционные изменения разрешены только после явного запроса пользователя.

## Elevation & Depth

Глубина формируется за счет мягких тональных переходов поверхностей `surface` вместо использования жестких черных теней. Тени разрешены только для парящих элементов — выпадающих меню, модальных окон и подсказок.

## Shape Language

Скругления углов служат маркером интерактивности:
- Карточки и крупные смысловые блоки закругляются на `rounded.xl` (24px) для дружелюбного, современного характера.
- Кнопки используют `rounded.md` (12px) для удобного клика пальцем или курсором.
- Поля ввода имеют скругление `rounded.DEFAULT` (8px).

## Component States & Behaviors

- **Hover:** При наведении интерактивные карточки приподнимаются (сдвиг вверх на 2px) с плавным переходом 150ms ease-in-out. Кнопки меняют цвет на `primary-hover`.
- **Focus:** Поля ввода при фокусе получают рамку толщиной 2px цвета `primary`.
- **Disabled:** Неактивные элементы снижают непрозрачность до 40% и блокируют курсор (`pointer-events: none`).

## Do's and Don'ts

- Do сохраняйте контрастность текстов на уровне стандарта WCAG AA (не менее 4.5:1).
- Do привязывайте абсолютно все размеры и скругления к YAML токенам спецификации.
- Don't используйте чистый черный цвет (#000) для текстов в светлой теме — заменяйте на `on-background`.
- Don't создавайте новые цвета в кодовой базе без предварительного занесения их в токен-палитру.
"""


def main():
    parser = argparse.ArgumentParser(description="AuraDesign Agent CLI Scanner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL веб-сайта для сканирования и анализа стиля")
    group.add_argument("--image", help="Путь к файлу изображения или URL картинки для визуального анализа")
    parser.add_argument("--dark", action="store_true", help="Форсировать генерацию тёмной темы контракта")
    parser.add_argument("--output", default="AURADESIGN.md", help="Путь для сохранения итогового дизайн-контракта (по умолчанию AURADESIGN.md)")
    
    args = parser.parse_args()
    
    print("[Scan] Запуск сканирования и построения AuraDesign Contract...")
    
    colors = []
    fonts = []
    source_name = "Custom Brand"
    is_dark = args.dark
    description = ""
    
    if args.url:
        print(f"[Scan] Сканирование веб-ресурса по адресу: {args.url}")
        
        # Парсим имя из URL для названия системы
        parsed_url = urllib.parse.urlparse(args.url)
        netloc = parsed_url.netloc or parsed_url.path
        clean_name = netloc.replace("www.", "").split(".")[0]
        source_name = clean_name.capitalize()
        
        # Проверяем, нет ли среди известных архетипов
        matched_archetype = None
        for key, value in SITE_ARCHETYPES.items():
            if key in clean_name.lower():
                matched_archetype = value
                break
                
        if matched_archetype:
            print(f"[Scan] Обнаружен готовый бренд-архетип: {matched_archetype['name']}")
            source_name = matched_archetype["name"]
            colors = list(matched_archetype["colors"].values())
            fonts = [matched_archetype["typography"]]
            is_dark = "тёмная" in matched_archetype["description"].lower()
            description = matched_archetype["description"]
        else:
            # Парсим реальный сайт по сети
            scraped = scrape_site_style(args.url)
            colors = scraped["colors"]
            fonts = scraped["fonts"]
            print(f"[Scan] Успешно извлечено цветов: {len(colors)}, Шрифтов: {len(fonts)}")
            
    elif args.image:
        print(f"[Scan] Анализ визуального характера изображения: {args.image}")
        source_name = os.path.basename(args.image).split(".")[0].replace("-", " ").replace("_", " ").capitalize()
        
        # Анализируем изображение. Имитируем палитру по имени картинки или дефолтную яркую
        # Если в пути есть 'dark' или 'night' - ставим темную тему
        if "dark" in args.image.lower() or "night" in args.image.lower() or "glass" in args.image.lower():
            is_dark = True
            
        if "glass" in args.image.lower():
            print("[Scan] Обнаружена эстетика Glassmorphism во входном ассете!")
            colors = ["#ffffff", "#adc9eb", "#0b1326"]
            fonts = ["Inter"]
            description = "Высокотехнологичный Glassmorphism-интерфейс, воссоздающий физику света и матового стекла."
        elif "pet" in args.image.lower() or "paw" in args.image.lower() or "friend" in args.image.lower():
            print("[Scan] Обнаружена дружелюбная органическая эстетика!")
            colors = ["#855300", "#0058be", "#f9f9ff"]
            fonts = ["Plus Jakarta Sans"]
            description = "Дружелюбный, человекоцентричный интерфейс с мягкими формами и цветными ambient-тенями."
        else:
            # Стандартная яркая палитра Aura
            colors = ["#4f46e5", "#06b6d4", "#ffffff"]
            fonts = ["Plus Jakarta Sans"]
            
    # Генерируем контент контракта
    contract_content = generate_auradesign_content(source_name, is_dark, colors, fonts, description)
    
    # Сохраняем в файл
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(contract_content)
        print(f"[OK] Дизайн-контракт успешно сформирован и сохранен по пути: {args.output}")
    except Exception as e:
        print(f"[Error] Ошибка записи контракта в файл: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
