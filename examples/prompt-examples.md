# Примеры промптов для Aura Designer

## Генерация по ссылке

```text
/aura-designer просканируй https://example.com, создай глубокий AURADESIGN.md, AURA_REPLICATION_TODO.md, AURA_SOURCE_ANALYSIS.md, AURA_BRAND_KIT_IMAGE_PROMPT.md и AURA_COLOR_PSYCHOLOGY.md. Сначала повтори источник copy-in-copy, без смены темы и композиции.
```

## Полный режим репликации через CLI

```bash
python "auradesign-agent/aura.py" analyze --url "https://example.com" --output-dir "."
python "auradesign-agent/aura.py" scan --url "https://example.com" --output "AURADESIGN.md"
python "auradesign-agent/aura.py" replicate --source-map "AURA_SOURCE_MAP.json" --contract "AURADESIGN.md" --output "index.html"
python "auradesign-agent/aura.py" qa --source-map "AURA_SOURCE_MAP.json" --html "index.html" --output-dir "."
```

## Генерация по скриншоту

```text
/aura-designer используй этот скриншот как визуальный источник. Если изображение в центре и заголовок за ним, повтори это точно. Вытащи палитру, сетку, типографику, motion rules и компоненты в AURADESIGN.md, затем пересобери страницу.
```

## Brand-kit картинка

```text
/aura-designer создай brand-kit image через gpt-image-2: одна большая картинка с мини-слайдами палитры, шрифтов, фонов, компонентов, hero-композиции, ассетов, сетки и mobile preview. Сохрани prompt в AURA_BRAND_KIT_IMAGE_PROMPT.md.
```

## Психология цвета

```text
/aura-designer создай AURA_COLOR_PSYCHOLOGY.md: объясни психологию палитры источника и предложи возможные улучшения, но не применяй их без моего разрешения.
```

## Улучшение существующей страницы

```text
/aura-designer улучши этот hero-блок. Исправь иерархию, контраст CTA, адаптив и размещение сгенерированного изображения, сохрани текущий стек.
```

## Финальное ревью

```text
/aura-design-reviewer проверь сгенерированную страницу. В первую очередь ищи баги контраста, прозрачные кнопки, сломанные изображения, слишком короткий AURADESIGN.md, mobile overflow и визуальную несогласованность.
```
