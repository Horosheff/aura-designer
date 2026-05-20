---

version: alpha
name: Aura Pets & Friendly
description: Человекоцентричный, теплый и оптимистичный дизайн-контракт для зооуслуг, детских центров и семейных брендов. Мягкие формы, цветные дышащие тени и сочный золотисто-оранжевый акцент.
colors:
  primary: "#855300"               # Золотистый теплый оранжевый
  primary-hover: "#653e00"
  on-primary: "#ffffff"
  secondary: "#0058be"             # Небесно-синий акцент
  on-secondary: "#ffffff"
  background: "#f9f9ff"            # Мягкий светлый фон с голубым отливом
  on-background: "#151c27"
  surface-lowest: "#ffffff"        # Чисто-белые карточки контента
  surface-low: "#f0f3ff"           # Тональные разделители
  surface-container: "#e7eefe"  
  surface-high: "#e2e8f8"  
  outline: "#867461"  
  outline-variant: "#d8c3ad"  
  error: "#ba1a1a"  
  on-error: "#ffffff"
typography:
  display-lg:
    fontFamily: "Plus Jakarta Sans"
    fontSize: "44px"
    fontWeight: "800"
    lineHeight: "1.15"
    letterSpacing: "-0.02em"
  headline-md:
    fontFamily: "Plus Jakarta Sans"
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

Дизайн-система Aura Pets & Friendly разработана для создания максимально дружелюбного, открытого и оптимистичного визуального пространства. Характер бренда: надежный, жизнерадостный, заботливый и активный.

Интерфейс строится на обилии свободного пространства, очень крупных заголовках скругленного шрифта Plus Jakarta Sans и полном отсутствии резких черных контуров. Основная задача — вызвать у пользователя улыбку и глубокое чувство доверия.

## Color Guidance

- **Primary (#855300):** Золотисто-оранжевый оттенок шерсти любимого питомца. Используется для главных кнопок призыва, акцентов внимания и важных заголовков.
- **Secondary (#0058be):** Небесно-синий оттенок. Применяется для блоков доверия, календарей, графиков и вспомогательной навигации.
- **Deep Charcoal (#151c27):** Темно-космический оттенок для всех текстов, обеспечивающий максимальную контрастность и деловой, профессиональный вид.

## Typography Hierarchy

- **Plus Jakarta Sans** — наш фирменный шрифт с дружелюбными округлыми окончаниями штрихов. Обязателен для всех заголовков, цифр статистики и названий карточек.
- **Inter** — используется для основного чтения и форм ввода, обеспечивая идеальный баланс читаемости.

## Layout & Grid

- Макет свободный, просторный. Разделы отделяются крупным шагом `spacing.lg` (40px) или `spacing.xl` (64px) для исключения перегруженности.
- Поля безопасности экрана составляют `spacing.margin` (24px).

## Elevation & Depth

- Основные фоны используют мягкий светлый тон `background` (#f9f9ff).
- Карточки контента парят на чисто-белой поверхности `surface-lowest`, выделяясь мягкими цветными ambient-тенями.
- **Дышащие цветные тени (Ambient Tinting):** В тени карточек подмешивается акцентный оранжевый или синий цвет бренда (размытие 20–40px, непрозрачность цвета в тени всего 4–8%).

## Shape Language

Формы мягкие, органичные и обтекаемые:

- Карточки питомцев и профили специалистов используют ультра-мягкий радиус `rounded.xl` (24px).
- Интерактивные кнопки — `rounded.lg` (16px) для осязаемого ощущения кликабельности.
- Поля ввода форм — `rounded.DEFAULT` (8px).

## Component States & Behaviors

- **Hover:** Кнопки и карточки плавно приподнимаются при наведении на 3px, увеличивая радиус и плотность цветных теней (переход 150ms ease-in-out).
- **Focus:** Инпуты получают мягкий оранжевый контур при наборе.

## Do's and Don'ts

- Do используйте цветные ambient-тени вместо стандартных пыльных серых.
- Do пишите все заголовки дружелюбным шрифтом Plus Jakarta Sans.
- Don't используйте острые углы (меньше 8px) для кнопок и карточек.
- Don't прижимайте элементы плотно друг к другу — сохраняйте воздух.