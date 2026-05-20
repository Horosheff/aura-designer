---
version: alpha
name: Aura SaaS Premium
description: Ультра-минималистичный светлый SaaS-интерфейс с обилием воздуха, тонкими линиями и сочными фиолетовыми акцентами для высокой продуктивности.
colors:
  primary: "#4f46e5"               # Королевский индиго (CTA)
  primary-hover: "#4338ca"
  on-primary: "#ffffff"
  secondary: "#06b6d4"             # Неоновый голубой акцент
  on-secondary: "#ffffff"
  background: "#f8fafc"            # Светло-серый чистый фон
  on-background: "#0f172a"
  surface-lowest: "#ffffff"        # Парящие белые карточки
  surface-low: "#f1f5f9"           
  surface-container: "#e2e8f0"     
  surface-high: "#cbd5e1"          
  outline: "#94a3b8"               
  outline-variant: "#e2e8f0"       
  error: "#dc2626"
  on-error: "#ffffff"
typography:
  display-lg:
    fontFamily: "Satoshi"
    fontSize: "44px"
    fontWeight: "800"
    lineHeight: "1.15"
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: "Satoshi"
    fontSize: "24px"
    fontWeight: "700"
    lineHeight: "1.3"
  body-md:
    fontFamily: "Geist"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.6"
  label-sm:
    fontFamily: "Geist"
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
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    typography: "{typography.label-sm}"
    padding: "{spacing.sm} {spacing.md}"
    height: "44px"
  card-interactive:
    backgroundColor: "{colors.surface-lowest}"
    borderColor: "{colors.outline-variant}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  input-field:
    backgroundColor: "{colors.surface-low}"
    borderColor: "{colors.outline}"
    rounded: "{rounded.DEFAULT}"
    padding: "{spacing.sm}"
---

## Philosophy & Vibe

Бренд Aura SaaS Premium несёт в себе эстетику сдержанного европейского минимализма. Главная эмоция — это технологическое превосходство, спокойствие, высокий фокус внимания и абсолютная чистота интерфейса.

В дизайне критически важно поддерживать «воздушность» макета — расстояния между логическими секциями должны быть не менее `spacing.xl` (64px). Шрифтовой ритм строится на контрасте жирного геометрического гротеска Satoshi и спокойного Geist для мелкого наборного текста.

## Color Guidance

- **Primary (#4f46e5):** Наш королевский индиго. Он зарезервирован исключительно для главных призывов к действию (CTA), интерактивных ссылок, активных фильтров и контуров фокуса. Запрещено использовать его для декоративных фонов или второстепенных текстов.
- **Surface-Lowest (#ffffff):** Белоснежные парящие карточки. Они служат базовой подложкой для интерактивных элементов контента на сером фоне `background` (#f8fafc).
- **Outline-Variant (#e2e8f0):** Ультра-тонкие деликатные разделители. Вместо грязных тёмных теней карточки аккуратно отделяются друг от друга этой границей.

## Typography Hierarchy

- **Satoshi** используется только для дисплеев и заголовков (Display, Headline). Особо крупные шрифты пишутся с отрицательным межбуквенным интервалом `letterSpacing: -0.02em` для плотности и собранности характера.
- **Geist** применяется для всего остального: основного текста, подписей к полям ввода, текстов ошибок и подсказок.

## Layout & Grid

- Макет страниц строго адаптивен и привязан к 4-колоночной сетке на мобильных устройствах и 12-колоночной — на десктопах.
- Промежутки в сетке карточек составляют ровно `spacing.gutter` (16px).
- Боковые безопасные зоны контента — `spacing.margin` (24px).

## Elevation & Depth

Глубина пространства строится за счет тональных уровней серой палитры. Никаких тяжелых чёрных размытых теней. Тени разрешены только для оверлейных выпадающих списков, поповеров и модальных окон (размытие 30px, прозрачность тени цвета бренда не более 6%).

## Shape Language

Скругления служат чётким маркером функциональных блоков:
- Интерактивные карточки контента имеют мягкий закруглённый угол `rounded.xl` (24px).
- Кнопки призыва к действию и выпадающие списки используют `rounded.md` (12px) для удобного клика.
- Поля ввода имеют скругление `rounded.DEFAULT` (8px).

## Component States & Behaviors

- **Hover:** При наведении интерактивные карточки контента мягко сдвигаются на 2px вверх с плавным переходом 150ms ease-in-out, а кнопки меняют фон на `primary-hover`.
- **Focus:** Инпуты при получении фокуса подсвечиваются 2px рамкой цвета `primary` с внутренним отступом.
- **Disabled:** Неактивные кнопки снижают непрозрачность до 40%, а курсор мыши меняется на `not-allowed`.

## Do's and Don'ts

- Do сохраняйте контрастность шрифтов не ниже стандарта WCAG AA (не менее 4.5:1).
- Do делайте все внешние отступы блоков кратными базовому шагу `spacing.base`.
- Don't смешивайте острые и круглые углы в одной секции — это ломает единство стиля.
- Don't используйте тени для карточек контента, если включена светлая тема.
- Don't используйте смайлики и эмодзи — заменяйте их чистыми векторными SVG.
- Don't используйте выдуманные статистические данные и круглые числа-пустышки (например, "99.9% uptime").
