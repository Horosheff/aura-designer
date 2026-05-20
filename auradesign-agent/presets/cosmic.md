---
version: alpha
name: Aura Cosmic Totality
description: Мистический тёмный премиум-дизайн в стиле космического затмения. Матовые плиты обсидиана, яркое янтарно-золотое свечение солнечной короны и строгая геометрия созвездий.
colors:
  primary: "#ffd700"               # Янтарно-золотая солнечная корона
  primary-hover: "#ffe16d"
  on-primary: "#0c0e13"
  secondary: "#00e3fd"             # Небесно-голубой свет затмения
  on-secondary: "#0c0e13"
  background: "#0c0e13"            # Глубокий межгалактический чёрный
  on-background: "#e3e1e9"
  surface-lowest: "#0d0e13"        # Obsidian base
  surface-low: "#121318"           
  surface-container: "#1e1f25"     
  surface-high: "#292a2f"          
  outline: "#999077"               
  outline-variant: "#4d4732"       
  error: "#ffb4ab"
  on-error: "#690005"
typography:
  display-lg:
    fontFamily: "Space Grotesk"
    fontSize: "44px"
    fontWeight: "700"
    lineHeight: "1.15"
    letterSpacing: "-0.04em"
  headline-md:
    fontFamily: "Space Grotesk"
    fontSize: "24px"
    fontWeight: "600"
    lineHeight: "1.3"
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: "Satoshi"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.6"
  label-sm:
    fontFamily: "Space Grotesk"
    fontSize: "12px"
    fontWeight: "500"
    lineHeight: "1.2"
    letterSpacing: "0.1em"
rounded:
  sm: "2px"
  DEFAULT: "4px"
  md: "8px"
  lg: "12px"
  xl: "20px"
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
    backgroundColor: "rgba(30, 31, 37, 0.4)"
    borderColor: "{colors.outline-variant}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  input-field:
    backgroundColor: "{colors.surface-lowest}"
    borderColor: "{colors.outline}"
    rounded: "{rounded.DEFAULT}"
    padding: "{spacing.sm}"
---

## Philosophy & Vibe

Эстетика Aura Cosmic Totality вдохновлена величием и мистицизмом полного солнечного затмения. Визуальный характер: «Obsidian & Corona» — парящие плиты матового обсидиана на фоне глубокого вакуума, подсвеченные сочным золотисто-янтарным и ледяным голубым свечением.

Для поддержания космической атмосферы критически важно соблюдать простор и геометрическую выверенность. Все элементы должны быть визуально отделены друг от друга большими зонами воздуха. Никакого визуального мусора.

## Color Guidance

- **Primary (#ffd700):** Насыщенный цвет солнечной короны. Используется для главного CTA, ключевых индикаторов и акцентного фонового свечения. Текст на золотых кнопках всегда пишется цветом `on-primary` (#0c0e13) для безупречной читаемости.
- **Secondary (#00e3fd):** Ледяной неоновый голубой. Используется для подсветки активных навигационных ссылок, второстепенных кнопок и контуров интерактивных карточек на ховере.
- **Background (#0c0e13):** Глубочайший черный цвет безжизненного космоса, на фоне которого разворачивается световой спектакль.

## Typography Hierarchy

- **Space Grotesk** — акцентный геометрический гротеск с научно-фантастическим характером. Заголовки пишутся с отрицательным трекингом `letterSpacing: -0.04em` для создания монолитного, массивного ощущения.
- **Satoshi** — изящный, современный гротеск для комфортного чтения больших блоков описаний.

## Layout & Grid

- Макет жестко центрирован, напоминая идеально круглую орбиту планет.
- Карточки распределяются асимметрично, ломая стандартные скучные 3-колоночные сетки.
- Разделительные линии — ультратонкие, цвета пыльного золота `outline-variant` (#4d4732).

## Elevation & Depth

Глубина воссоздается за счет светодиодной контрастной подсветки (Ambient Backlight):
- Карточки обсидиана парят на фоне глубокого космоса за счет тонкого прозрачного свечения цвета короны (размытие 30px, непрозрачность цвета не более 5%).
- Модальные слои получают более яркую янтарную подсветку.

## Shape Language

Скругления сдержанные и выверенные:
- Карточки контента имеют скругление `rounded.xl` (20px).
- Кнопки используют `rounded.md` (8px).
- Поля ввода имеют скругление `rounded.DEFAULT` (4px).

## Component States & Behaviors

- **Hover:** При наведении обсидиановые карточки плавно подсвечиваются ледяным синим цветом `secondary` по контуру и увеличивают глубину задней подсветки.
- **Focus:** Активные формы подсвечиваются золотой рамкой с мягким свечением.

## Do's and Don'ts

- Do используйте радиальные градиенты для симуляции космических туманностей и затмения на фоне.
- Do применяйте только чистые векторные SVG-иконки, отражающие орбиты, фазы луны и созвездия.
- Don't используйте смайлы и эмодзи — это рушит премиальность темы.
- Don't используйте серые размытые тени. Тени должны быть либо цветными (неон), либо отсутствовать вовсе.
