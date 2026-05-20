---

version: alpha
name: Aura Glassmorphism
description: Высокотехнологичный премиальный интерфейс, воспроизводящий физику света, матового стекла и преломления на фоне сочных абстрактных градиентов.
colors:
  surface: "#0b1326"
  surface-bright: "#31394d"
  surface-container-low: "#131b2e"
  surface-container: "#171f33"
  surface-container-high: "#222a3d"
  primary: "#ffffff"
  on-primary: "#2f3131"
  background: "#0b1326"
  on-background: "#dae2fd"
  outline: "#8e9192"
  outline-variant: "#444748"
  error: "#ffb4ab"
  on-error: "#690005"
typography:
  display-lg:
    fontFamily: "Inter"
    fontSize: "44px"
    fontWeight: "700"
    lineHeight: "1.15"
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: "Inter"
    fontSize: "24px"
    fontWeight: "600"
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
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    typography: "{typography.label-sm}"
    padding: "{spacing.sm} {spacing.md}"
    height: "44px"
  card-interactive:
    backgroundColor: "rgba(255, 255, 255, 0.1)"
    borderColor: "rgba(255, 255, 255, 0.2)"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  input-field:
    backgroundColor: "rgba(255, 255, 255, 0.05)"
    borderColor: "rgba(255, 255, 255, 0.1)"
    rounded: "{rounded.DEFAULT}"
padding: "{spacing.sm}"

---

## Philosophy & Vibe

Эстетика Aura Glassmorphism воспроизводит эффект матовых стеклянных линз, парящих в жидком цифровом пространстве. Фон страницы всегда представляет собой сочный, динамичный, многоцветный абстрактный градиент (сочетание неонового фиолетового, глубокого синего и нежно-розового), который просвечивает сквозь интерфейс.

Интерфейс должен ощущаться легким, парящим и безупречно чистым. Роль украшательств выполняют размытия и преломления света, а не нарисованные рамки или сплошные цвета.

## Color Guidance

- **Primary (#ffffff):** Ослепительно белый цвет. Используется для текстов, иконок и фонов кнопок CTA. Контраст между белым текстом и цветным размытым фоном должен жестко контролироваться.
- **Surface Alpha:** Подложка контейнеров карточек никогда не бывает сплошной. Она формируется из белого цвета с альфа-каналом: `rgba(255,255,255,0.1)` для стандартных зон и `rgba(255,255,255,0.2)` для фокусных панелей.
- **Text Color:** Текст пишется серебристо-белым цветом (#ffffff или #dae2fd) для сохранения эффекта светимости.

## Typography Hierarchy

- **Inter** используется во всех ролях дисплеев и текстов. На полупрозрачных размытых фонах ИИ обязан принудительно увеличивать вес шрифта на одну ступень (например, Medium вместо Regular), чтобы компенсировать оптическое размытие и шум градиентов.
- Мелкому тексту может добавляться мягкая тень `text-shadow: 0px 2px 4px rgba(0,0,0,0.15)` для идеальной читаемости.

## Layout & Grid

- Карточки свободно группируются в «стеклянные контейнеры», парящие внутри безопасной зоны.
- Между блоками соблюдается просторный ритм `spacing.lg` (40px) или `spacing.xl` (64px) для видимости красивого фонового градиента.

## Elevation & Depth

Глубина — важнейший параметр, достигаемый через физику света:

- **Уровень 1 (Стандартная карточка):** `backdrop-filter: blur(20px)` и фон `rgba(255, 255, 255, 0.1)`.
- **Уровень 2 (Модальные окна/Фокус):** `backdrop-filter: blur(40px)` и фон `rgba(255, 255, 255, 0.2)`.
- **Светопреломление на гранях:** Каждый стеклянный контейнер обязан обладать тонкой 1px рамкой `rgba(255,255,255,0.2)`.

## Shape Language

Скругления мягкие и обтекаемые:

- Стеклянные карточки используют радиус `rounded.xl` (24px).
- Кнопки и поля ввода — `rounded.md` (12px).

## Component States & Behaviors

- **Hover:** При наведении карточки увеличивают степень размытия фона и прозрачность до `0.15` (плавный переход 200ms ease-in-out).
- **Disabled:** Заблокированные элементы снижают непрозрачность до 30%.

## Do's and Don'ts

- Do используйте только белые рамки с прозрачностью для краев карточек.
- Do увеличивайте вес шрифтов на размытых поверхностях для читаемости.
- Don't используйте сплошные серые или черные фоны для карточек контента.
- Don't добавляйте жесткие темные тени к стеклянным панелям.