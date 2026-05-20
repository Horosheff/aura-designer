---
name: aura-cyrillic-google-fonts
description: Подбирает многообразные пары Google Fonts с поддержкой кириллицы для Aura Designer. Используй при выборе типографики, Google Fonts, кириллицы, font pairing, заголовков и body-шрифтов в AURADESIGN.md или HTML.
---

# Aura Cyrillic Google Fonts

## Главный Закон

Все шрифтовые пары Aura должны поддерживать кириллицу, если страница, бренд, интерфейс или потенциальная аудитория используют русский язык. Не выбирай шрифт только потому, что он красив в латинице. Сначала проверь, что у него есть Cyrillic или Cyrillic Extended в Google Fonts.

## Алгоритм Подбора

1. Определи характер источника: мягкий, строгий, журнальный, техно, детский, люксовый, brutal, editorial, minimal, ретро.
2. Подбери display-шрифт для заголовков и body-шрифт для текста из списка ниже.
3. Проверь кириллицу у обеих гарнитур. Если у display-шрифта нет кириллицы, не используй его для русского текста; можно оставить только для латинского логотипа.
4. Подключай Google Fonts через один URL с `display=swap`, `preconnect` и только нужными весами.
5. Для жирных заголовков ставь `letter-spacing: -0.02em...-0.06em`; для light-serif и editorial чаще нужен нейтральный или слегка положительный трекинг.

## Большой Каталог Кириллических Пар

### Нейтральный SaaS / Стартап / Продукт

- `Manrope` + `Inter`: чистый продуктовый интерфейс, русская читабельность.
- `Manrope` + `Noto Sans`: максимально безопасная кириллица и интерфейсы.
- `Onest` + `Inter`: современный российский digital-стиль.
- `Onest` + `Manrope`: мягкий SaaS без западного шаблонного вида.
- `Wix Madefor Display` + `Wix Madefor Text`: аккуратная продуктовая система.
- `Golos Text` + `Golos Text`: государственные, сервисные, B2B-интерфейсы.
- `IBM Plex Sans` + `IBM Plex Sans`: технологичный, строгий, международный продукт.
- `Source Sans 3` + `Source Sans 3`: длинные тексты, документация, dashboards.
- `Roboto Flex` + `Roboto`: Android-like, утилитарный, безопасный UI.

### Мягкий Пастельный / Портфолио / Creator

- `Nunito Sans` + `Nunito Sans`: дружелюбный, мягкий, округлый.
- `Comfortaa` + `Nunito Sans`: мягкие заголовки и читаемый body.
- `Rubik` + `Nunito Sans`: плотный, дружелюбный, живой.
- `YS Text` недоступен в Google Fonts; вместо него используй `Golos Text` или `Onest`.
- `Mulish` + `Nunito Sans`: легкий lifestyle и портфолио.
- `Montserrat Alternates` + `Montserrat`: творческий, но с кириллицей.
- `Raleway` + `Open Sans`: воздушный creative-portfolio.
- `Jost` + `Manrope`: модный clean editorial с кириллицей.

### Editorial / Журнал / Премиум

- `Cormorant Garamond` + `Manrope`: русская editorial-элегантность.
- `Cormorant` + `Golos Text`: культурные проекты, галереи, афиши.
- `Oranienbaum` + `PT Sans`: классическая русская эстетика.
- `Playfair Display` + `Manrope`: премиальный контраст, если кириллица нужна в заголовках, проверь поддержку перед применением.
- `Lora` + `Source Sans 3`: длинные статьи, блоги, экспертные лонгриды.
- `Merriweather` + `Open Sans`: надежная читабельная связка для медиа.
- `PT Serif` + `PT Sans`: универсальная русская журнальная связка.
- `Vollkorn` + `Roboto`: серьезный текстовый бренд.

### Нео-Брутализм / Афиши / Сильный Graphic Design

- `Unbounded` + `Manrope`: тяжелые заголовки, современная кириллица.
- `Unbounded` + `Golos Text`: яркий русский web/brutal.
- `Russo One` + `Roboto`: спортивный, технологичный, громкий стиль.
- `Rubik Mono One` + `Rubik`: плакатный стиль и плотные блоки.
- `Montserrat Alternates` + `Golos Text`: нестандартные формы без потери читабельности.
- `Jost` + `Golos Text`: геометричный, но не шаблонный.
- `Oswald` + `Source Sans 3`: сжатые заголовки, афишный ритм.
- `Roboto Condensed` + `Roboto`: плотные интерфейсы и табличные блоки.

### Tech / AI / Web3 / Fintech

- `IBM Plex Mono` + `IBM Plex Sans`: код, fintech, AI-инструменты.
- `JetBrains Mono` + `Manrope`: developer-first продукты.
- `Roboto Mono` + `Roboto`: техничный, спокойный, надежный.
- `Space Grotesk` не всегда подходит под кириллицу; для русских заголовков замени на `Unbounded`, `Jost` или `Manrope`.
- `Exo 2` + `Open Sans`: технологичный футуризм с кириллицей.
- `Commissioner` + `Manrope`: современный digital/government tech.
- `Geologica` + `Golos Text`: геометричный технологичный русский интерфейс.
- `Fira Sans` + `Fira Mono`: open-source и технические продукты.

### Luxury / Beauty / Boutique

- `Cormorant Garamond` + `Manrope`: салон, студия, мода.
- `Poiret One` + `Montserrat`: тонкий fashion-акцент, осторожно с длинным текстом.
- `Tenor Sans` + `Open Sans`: мягкий premium lifestyle.
- `Prata` + `Roboto`: выразительный luxury display.
- `Forum` + `PT Sans`: русская культурная классика.
- `Lora` + `Mulish`: спокойный премиальный блог/brand-story.

### Детское / Pets / Organic

- `Nunito` + `Nunito Sans`: теплый, дружелюбный интерфейс.
- `Comfortaa` + `Open Sans`: округлые заголовки, читаемое тело.
- `Rubik` + `Rubik`: мягкая геометрия.
- `Pangolin` + `Nunito`: рукописный акцент с кириллицей, только для коротких заголовков.
- `Neucha` + `Open Sans`: hand-made, детское, иллюстративное.
- `Gabriela` + `Nunito Sans`: сказочный мягкий serif.

### Retro / Soviet / Archive / Culture

- `Russo One` + `PT Sans`: советский плакат, спорт, индустрия.
- `Oswald` + `PT Sans`: газетная плотность.
- `Oranienbaum` + `PT Serif`: исторический и музейный стиль.
- `Forum` + `PT Sans`: афиши, театр, культурные проекты.
- `Underdog` + `Open Sans`: неформальный рукописный акцент.

## Запреты

- Не используй `Clash Display`, `Satoshi`, `Neue Montreal`, `Avenir`, `Helvetica Neue` как Google Fonts для русских страниц: их нет в Google Fonts или кириллица не гарантирована.
- Не выбирай `Space Grotesk`, `Syne`, `Outfit`, `Plus Jakarta Sans` для русского текста без проверки кириллицы. Если кириллицы нет, замени на `Manrope`, `Onest`, `Golos Text`, `Jost`, `Geologica`, `Unbounded`.
- Не используй больше двух семейств на странице, кроме маленького mono-акцента.
