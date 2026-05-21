# AURA_FONT_MATCH

Проект: **Language You+ Design System**
Источник: `assets/c__Users_mrrut_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_4c0d6218605807c704ded04f41921622-06e4fdca-3505-4a11-92a7-099c617cd735.png`

## Назначение

Этот файл фиксирует подбор Google Fonts с поддержкой кириллицы. Если проект может содержать русский текст, оба шрифта пары должны иметь Cyrillic/Cyrillic Extended. Полный каталог и правила находятся в `.cursor/skills/aura-cyrillic-google-fonts/SKILL.md`.

## Найденные шрифты источника

- `Plus Jakarta Sans` / Геометрический плотный гротеск (сжат по горизонтали, tracking-tight)
- `Inter` / Нейтральный высокочитаемый гротеск

## Выбранная Пара

- **Display:** `Onest` (Google Fonts)
- **Body:** `Inter` (Google Fonts)
- **Почему:** Шрифт `Onest` разработан специально для повышения читаемости цифровых интерфейсов, обладает потрясающей плотностью букв и современным ритмом. При установке отрицательного межбуквенного интервала `tracking-tight` он идеально воспроизводит жирный акцентный характер заголовков на скриншоте. Шрифт `Inter` используется для body, так как он обеспечивает превосходное графическое соответствие и идеальную читаемость.
- **Cyrillic check:** `OK` (Оба шрифта на 100% поддерживают кириллическое начертание во всех весах от Regular до ExtraBold).

## Ссылка на подключение

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Onest:wght@700;800;900&display=swap" rel="stylesheet">
```

## Запреты

- Не использовать шрифт без кириллицы для русского текста.
- Не использовать `Inter` как автоматический display для любой ниши.
- Не использовать `Satoshi`, `Neue Montreal`, `Helvetica Neue`, `Avenir`, `Clash Display` как Google Fonts для русских страниц.
