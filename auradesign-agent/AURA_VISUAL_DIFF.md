# AURA_VISUAL_DIFF

Источник: `assets/c__Users_mrrut_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_6cb7528a15e37b8afeae3991a0ad6b47-00891b14-2bfe-43dc-aa91-09743c073341.png`
HTML: `auradesign-agent/index.html`
Статус: **PENDING_BROWSER_CHECK**

## Назначение

Этот файл является visual-diff gate. Агент не должен писать "готово идеально", пока не сравнит источник и результат side-by-side.

## Обязательные Viewports

- [ ] 1440px desktop
- [ ] 768px tablet
- [ ] 375px mobile

## Зоны Сравнения

- [ ] Hero: позиция изображения, заголовок, слои, фон, CTA.
- [ ] Typography: похожесть шрифта, размер, вес, line-height, tracking, регистр.
- [ ] Shapes: кляксы, круги, blobs, капсулы, линии, cards, stickers, SVG.
- [ ] Borders/Shadows: отсутствие чужих stroke/shadow, соответствие источнику.
- [ ] Spacing: внешние поля, gap, вертикальный ритм, max-width.
- [ ] Color: палитра, opacity, контраст, фон.
- [ ] Assets: изображения, cutout, background removal, MCP URL.
- [ ] Mobile: отсутствие горизонтального скролла, сохранение композиционной логики.

## Оценка

| Зона | Отклонение | Решение |
| --- | --- | --- |
| Hero | `[0-100%]` | `[OK/FIX]` |
| Typography | `[0-100%]` | `[OK/FIX]` |
| Shapes | `[0-100%]` | `[OK/FIX]` |
| Spacing | `[0-100%]` | `[OK/FIX]` |
| Colors | `[0-100%]` | `[OK/FIX]` |

## Gate

- **PASS** только если нет критичных расхождений по hero, typography, shapes и assets.
- Если shape отличается типом (клякса заменена звездой, круг заменен ромбом), gate должен быть **FAIL**.
- Если добавлены обводки/тени, которых нет в источнике, gate должен быть **FAIL**.
