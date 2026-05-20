---

version: alpha
name: Aura BUMAGA Bureau
description: Сумасшедший креативный нео-брутализм с эстетикой бумажных слоев, яркими неоновыми плашками, толстыми черными границами и непрерывным интерактивом.
colors:
  primary: "#ff33a0"               # Насыщенный розовый BUMAGA (бумажный неоновый)
  primary-hover: "#e6228f"
  on-primary: "#ffffff"
  secondary: "#3bee33"             # Кислотно-зеленый лайм
  on-secondary: "#0c0e13"
  tertiary: "#0066ff"              # Электрический синий индиго
  background: "#ffffff"            # Светлая базовая основа
  on-background: "#0c0e13"
  surface-lowest: "#ffffff"  
  surface-low: "#0c0e13"           # Глубокий черный для темных секций
  surface-container: "#ffee11"     # Яркий неоновый желтый
  surface-high: "#ff7700"          # Сочный оранжевый
  outline: "#0c0e13"               # Жирные черные обводки брутализма
  outline-variant: "#e2e8f0"  
  error: "#ef4444"
  on-error: "#ffffff"
typography:
  display-lg:
    fontFamily: "Unbounded"
    fontSize: "44px"
    fontWeight: "900"
    lineHeight: "1.1"
    letterSpacing: "-0.03em"
  headline-md:
    fontFamily: "Unbounded"
    fontSize: "28px"
    fontWeight: "850"
    lineHeight: "1.2"
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: "Plus Jakarta Sans"
    fontSize: "16px"
    fontWeight: "500"
    lineHeight: "1.6"
  label-sm:
    fontFamily: "Unbounded"
    fontSize: "12px"
    fontWeight: "700"
    lineHeight: "1.2"
    letterSpacing: "0.05em"
rounded:
  sm: "4px"
  DEFAULT: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  full: "9999px"
spacing:
  base: "10px"
  xs: "5px"
  sm: "15px"
  md: "30px"
  lg: "50px"
  xl: "80px"
  gutter: "20px"
  margin: "30px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    typography: "{typography.label-sm}"
    padding: "{spacing.sm} {spacing.md}"
    height: "50px"
  card-interactive:
    backgroundColor: "{colors.surface-lowest}"
    borderColor: "{colors.outline}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  input-field:
    backgroundColor: "{colors.surface-lowest}"
    borderColor: "{colors.outline}"
    rounded: "{rounded.DEFAULT}"
padding: "{spacing.sm}"

---

## Philosophy & Vibe

Эстетика Aura BUMAGA Bureau — это манифест смелого, бескомпромиссного креатива и нео-брутализма. Рожденный из текстур резаной бумаги, стикеров, сигнальных лент и сочных фломастеров, этот стиль кричит о самобытности.

Основная эмоция: безудержная энергия, тактильность, игра и цифровой фан. Никакого скучного серого «воздуха». Пространство заполнено контрастными плашками, толстыми 2px или 3px черными обводками (Strokes), падающими жесткими плоскими тенями (Hard Shadows) без размытия и бесконечной чередой стикеров.

## Color Guidance

- **Primary (#ff33a0):** Фирменный розовый «BUMAGA». Используется для логотипа, ключевых заголовков, главных кнопок и рамок карточек команды.
- **Secondary (#3bee33):** Сигнальный кислотно-зеленый. Используется для плашек статусов, кругов с достижениями и фонов карточек кейсов.
- **Tertiary (#0066ff):** Электрический синий. Служит для выделения интерактивных капсул и фокусов.
- **Surface-Low (#0c0e13):** Глубокий черный уголь. Секции на черном фоне создают мощный контраст с белыми и неоновыми блоками, заставляя цвета взрываться яркостью.

## Typography Hierarchy

- **Unbounded** — сверхжирный, акцентный гротеск с невероятно широким характером. Все заголовки дисплеев и кнопок пишутся этим шрифтом с отрицательным трекингом для ощущения монолитной стены букв.
- **Plus Jakarta Sans** — современный открытый гротеск для комфортного чтения больших списков услуг и описаний.

## Layout & Grid

- Макет асимметричен, как коллаж на доске мудборда.
- Наличие перекрещивающихся по диагонали сигнальных лент-тикеров (Lanyards), непрерывно бегущих по экрану, разделяя ключевые секции.
- Все карточки и кнопки имеют толстую 2.5px черную обводку `#0c0e13`.

## Elevation & Depth

- Традиционные тени полностью запрещены.
- Глубина передается за счет **жесткого смещения (Hard Flat Shadow):** карточки и кнопки имеют черную плотную тень (смещение `4px 4px 0px #0c0e13` или `6px 6px 0px #0c0e13` без размытия), имитируя стопку вырезанных листов бумаги.

## Shape Language

Скругления крупные и акцентированные:

- Интерактивные стикеры и бейджи — `rounded.full` (капсулы).
- Кейсы и контент-панели — `rounded.xl` (32px), создающие дружелюбную форму.
- Кнопки — `rounded.md` (16px) с брутальным характером.

## Component States & Behaviors

- **Hover:** Кнопки и карточки при наведении вдавливаются (смещение `translate-x-[3px] translate-y-[3px]` и исчезновение плоской тени, создавая идеальное тактильное ощущение нажатия физической кнопки).
- **Stickers:** Маленькие векторные фигурки (звезды, монстрики, крестики) вращаются или пульсируют при наведении на них курсора.

## Do's and Don'ts

- Do используйте контрастные переходы между кипенно-белыми и глубоко-черными секциями.
- Do применяйте только чистые векторные анимированные SVG вместо смайликов (ретро-игры, молнии, стикеры).
- Don't используйте размытые тени и градиенты на карточках — только плоские заливки и жесткие тени.
- Don't используйте мелкие шрифты с засечками — только брутальный сверхжирный гротеск.