---
version: alpha
name: Aura Alpine Observatory
description: Строгий, интеллектуальный дизайн-контракт в стиле научной экспедиции XIX века. Стальные холодные линии, цвет состаренной бумаги, латунные фокусные акценты и нулевые скругления.
colors:
  primary: "#f6bb81"               # Старая латунь / Теплый приборный акцент
  primary-hover: "#ffdcbe"
  on-primary: "#0a1325"
  secondary: "#b7c9d8"             # Ледниковая сталь / Холодный каркас
  on-secondary: "#0a1325"
  background: "#0a1325"            # Глубокая обсерваторная синева (ночное небо)
  on-background: "#dae2fc"
  surface-lowest: "#ffffff"        # Цвет состаренной бумаги / Карта экспедиции
  surface-low: "#050e20"           # Стальной темный фон контейнера
  surface-container: "#171f32"     
  surface-high: "#2c3548"          
  outline: "#9d8e81"               # Латунные рамки приборов
  outline-variant: "#50453a"       
  error: "#ffb4ab"
  on-error: "#690005"
typography:
  display-lg:
    fontFamily: "Marcellus"
    fontSize: "48px"
    fontWeight: "400"
    lineHeight: "1.1"
    letterSpacing: "0.02em"
  headline-md:
    fontFamily: "Marcellus"
    fontSize: "24px"
    fontWeight: "400"
    lineHeight: "1.3"
    letterSpacing: "0.05em"
  body-md:
    fontFamily: "Newsreader"
    fontSize: "18px"
    fontWeight: "400"
    lineHeight: "1.6"
  label-sm:
    fontFamily: "IBM Plex Mono"
    fontSize: "11px"
    fontWeight: "500"
    lineHeight: "1.5"
    letterSpacing: "0.15em"
rounded:
  sm: "0px"
  DEFAULT: "0px"
  md: "0px"
  lg: "0px"
  xl: "0px"
  full: "0px"
spacing:
  base: "6px"
  xs: "4px"
  sm: "12px"
  md: "24px"
  lg: "48px"
  xl: "80px"
  gutter: "16px"
  margin: "32px"
components:
  button-primary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    typography: "{typography.label-sm}"
    padding: "{spacing.sm} {spacing.md}"
    height: "44px"
  card-interactive:
    backgroundColor: "{colors.surface-low}"
    borderColor: "{colors.outline-variant}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  input-field:
    backgroundColor: "{colors.surface-container}"
    borderColor: "{colors.outline}"
    rounded: "{rounded.DEFAULT}"
    padding: "{spacing.sm}"
---

## Philosophy & Vibe

Эстетика Aura Alpine Observatory переносит нас во времена Королевского географического общества и великих альпийских экспедиций XIX века. Визуальный характер: «Scientific Alpinism» — сочетание холодного звездного неба над вершинами и тактильных, исторических приборов на деревянном столе.

Никакой современной мягкости, никаких размытых теней или округлых кнопок. Полная доминация жестких математических сеток, тонких стальных линий разметки и латунных шкал.

## Color Guidance

- **Primary (#f6bb81):** Благородная старая латунь. Цвет гравированных приборов, линз телескопа и компасов. Используется строго для интерактивных элементов, фокусов ввода и важных отметок.
- **Secondary (#b7c9d8):** Цвет холодного ледника. Стальной серый оттенок для тонких линий разметки, второстепенного текста и каркасов таблиц.
- **Surface-Lowest (#ffffff):** Контрастный цвет состаренного пергамента. Используется в качестве акцентной подложки для больших блоков текста дневника, имитируя разложенную карту.

## Typography Hierarchy

- **Marcellus** — изысканный, классический шрифт, вещающий от имени истории. Используется строго для заголовков.
- **Newsreader** — канонический литературный serif для дневниковых записей, логов экспедиций и отчетов о погоде на высоте.
- **IBM Plex Mono** — голос вычислительной машины. Строго в верхнем регистре, с широким межбуквенным трекингом `letterSpacing: 0.15em`. Для координат, логов, данных высоты и пунктов меню.

## Layout & Grid

- Макет жестко выверен и подчинен чертежному стилю. Поля разделяются тонкими 1px рамками стального цвета.
- В углах крупных секций размещаются тонкие крестообразные маркеры юстировки (+), имитирующие прицел телескопа или сетку квадранта.
- Окружающий воздух используется не для «легкости», а для изоляции важных массивов данных.

## Elevation & Depth

- В системе полностью отсутствуют классические размытые тени — глубина строится по принципу бинарной подсветки и физических рамок.
- Наличие 1px стального или латунного контура определяет, является ли элемент активным.

## Shape Language

- **Строгое правило 0px скруглений:** Ни одного закруглённого угла во всей системе. Любой круглый или закругленный элемент считается критическим дефектом. Единственные допустимые углы — жесткие 90-градусные стыки или срезы под 45 градусов (фаски).

## Component States & Behaviors

- **Hover:** При наведении латунные рамки кнопок и карточек заполняются сплошным цветом латуни `primary`, а текст инвертируется в темно-синий.
- **Focus:** Поля ввода очерчиваются латунным контуром, а в углу поля всплывает крошечный маркер-координата.

## Do's and Don'ts

- Do используйте только чистые векторные SVG-иконки приборов (роза ветров, секстант, компас, астролябия).
- Do привязывайте шрифты к Newsreader и Marcellus для сохранения атмосферы викторианской науки.
- Don't используйте смайлики и эмодзи — это рушит исторический дух.
- Don't допускайте скруглений углов (border-radius) даже на кнопках или аватарах.
