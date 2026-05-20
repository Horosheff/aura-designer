#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aura Designer - Visual QA
=========================
Проверяет, насколько результат готов к source-accurate replica workflow.
Без внешних зависимостей выполняет структурный QA; в Cursor sub-agent этот
отчет должен дополняться screenshot/browser проверкой.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request


if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def read_text(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_file(path, label, findings):
    if not os.path.exists(path):
        findings.append(("critical", f"Не найден обязательный файл: `{label}` ({path})"))
        return False
    return True


def extract_image_sources(html):
    return re.findall(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", html, flags=re.IGNORECASE)


def check_image_source(src, html_path, findings):
    parsed = urllib.parse.urlparse(src)
    if parsed.scheme in {"http", "https"}:
        request = urllib.request.Request(src, method="GET", headers={"User-Agent": "AuraDesignerQA/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.status >= 400:
                    findings.append(("critical", f"Изображение недоступно: `{src}` вернуло HTTP {response.status}"))
        except Exception as exc:
            findings.append(("critical", f"Изображение недоступно: `{src}` ({exc})"))
        return

    if parsed.scheme == "data":
        return

    base_dir = os.path.dirname(os.path.abspath(html_path)) or "."
    local_path = os.path.normpath(os.path.join(base_dir, src))
    if not os.path.exists(local_path):
        findings.append(("critical", f"Локальное изображение из HTML не найдено: `{src}` -> `{local_path}`"))


def check_asset_registry(output_dir, html, findings):
    registry_path = os.path.join(output_dir, "AURA_ASSET_REGISTRY.json")
    generated_image_markers = ["tempfile.aiquickdraw.com", "gpt-image-2", "recraft_remove_background"]
    html_uses_generated = any(marker in html for marker in generated_image_markers)
    if html_uses_generated and not os.path.exists(registry_path):
        findings.append(("critical", "HTML использует сгенерированные изображения, но нет `AURA_ASSET_REGISTRY.json` с MCP KV URL."))
        return

    if not os.path.exists(registry_path):
        return

    try:
        registry = read_json(registry_path)
    except Exception as exc:
        findings.append(("critical", f"`AURA_ASSET_REGISTRY.json` не читается: {exc}"))
        return

    for asset in registry.get("assets", []):
        if asset.get("generationTool") != "user-mcp-kv/gpt-image-2":
            findings.append(("critical", f"Ассет `{asset.get('id', 'unknown')}` создан не через `user-mcp-kv/gpt-image-2`."))
        if asset.get("mustUseInHtml") and asset.get("transparentImageUrl") not in html:
            findings.append(("critical", f"MCP ассет `{asset.get('id', 'unknown')}` не подключен в HTML."))


def check_hero_cutout_overlap(html, findings):
    """Контролирует, что обрезанный hero-person asset спрятан под следующим блоком."""
    has_person_cutout = "Duong Minh Thanh Profile" in html or "hero foreground people" in html
    if not has_person_cutout:
        return

    if "overflow-hidden pt-" in html:
        findings.append(("critical", "Hero-person asset находится внутри `overflow-hidden` hero. Нижний край может обрезаться видимой линией. Используйте `overflow-y-visible`."))

    if "translate-y-" not in html:
        findings.append(("critical", "Hero-person asset не сдвинут вниз через `translate-y-*`; низ фигуры должен уходить под следующий блок."))

    if "mt-[-" not in html:
        findings.append(("critical", "Второй блок не перекрывает hero через отрицательный margin. Обрезка ног/низа ассета будет видна."))

    if "z-30" not in html and "z-40" not in html:
        findings.append(("critical", "Нет явного верхнего z-index у второго блока/оверлеев для маскировки нижнего края hero-person asset."))


def check_visual_gates(output_dir, findings):
    visual_diff_path = os.path.join(output_dir, "AURA_VISUAL_DIFF.md")
    reviewer_path = os.path.join(output_dir, "AURA_REVIEWER_PASS.md")

    if os.path.exists(visual_diff_path):
        visual_diff = read_text(visual_diff_path)
        if "PENDING_BROWSER_CHECK" in visual_diff:
            findings.append(("medium", "`AURA_VISUAL_DIFF.md` создан, но browser side-by-side проверка еще не заполнена."))
        if "Gate" not in visual_diff:
            findings.append(("medium", "`AURA_VISUAL_DIFF.md` не содержит секцию Gate."))

    if os.path.exists(reviewer_path):
        reviewer = read_text(reviewer_path)
        if "PENDING_REVIEWER" in reviewer:
            findings.append(("medium", "`AURA_REVIEWER_PASS.md` создан, но `aura-design-reviewer` еще не поставил PASS/FAIL."))
        if "Verdict" not in reviewer:
            findings.append(("medium", "`AURA_REVIEWER_PASS.md` не содержит итоговый Verdict."))


def build_report(source_map_path, html_path, output_dir):
    findings = []
    source_map = read_json(source_map_path)
    html = read_text(html_path) if os.path.exists(html_path) else ""
    source = source_map.get("source", {})
    composition = source.get("composition", {})
    hero = composition.get("hero", {})

    if not html:
        findings.append(("critical", f"HTML-файл не найден или пустой: `{html_path}`"))

    h1 = hero.get("headline")
    if h1 and h1 not in html:
        findings.append(("high", f"Главный заголовок источника не найден в HTML: `{h1}`"))

    primary_image = hero.get("primaryImage") or {}
    image_src = primary_image.get("src")
    if image_src and image_src not in html:
        findings.append(("high", "Главное изображение источника не найдено в HTML. Нужно сохранить source image или заменить только после разрешения пользователя."))

    if "placeholder" in html.lower() or "lorem" in html.lower():
        findings.append(("medium", "В HTML обнаружены placeholder/lorem маркеры. Для Aura это запрещено."))

    if re.search(r"[😀-🙏🌀-🗿🚀-🛿☀-⛿✂-➿]", html):
        findings.append(("medium", "В HTML найдены emoji/symbol markers. UI должен использовать SVG/CSS/generative assets."))

    for src in extract_image_sources(html):
        check_image_source(src, html_path, findings)
    check_asset_registry(output_dir, html, findings)
    check_hero_cutout_overlap(html, findings)
    check_visual_gates(output_dir, findings)

    required = [
        "AURA_REPLICATION_TODO.md",
        "AURA_SOURCE_ANALYSIS.md",
        "AURA_FONT_MATCH.md",
        "AURA_BRAND_KIT_IMAGE_PROMPT.md",
        "AURA_COLOR_PSYCHOLOGY.md",
        "AURA_VISUAL_DIFF.md",
        "AURA_REVIEWER_PASS.md",
        "AURA_SOURCE_MAP.json",
        "AURA_COMPOSITION_LOCK.json",
        "AURA_COMPONENT_MAP.json",
        "AURA_SHAPE_MAP.json",
    ]
    for filename in required:
        check_file(os.path.join(output_dir, filename), filename, findings)

    if hero.get("mustPreserveLayering") and "z-index" not in html and "z-" not in html:
        findings.append(("medium", "Источник требует сохранения слоев, но в HTML не найден явный z-index/layering."))

    status = "PASS" if not any(level == "critical" for level, _ in findings) else "FAIL"
    lines = [
        "# AURA_VISUAL_QA",
        "",
        f"Статус: **{status}**",
        f"Source map: `{source_map_path}`",
        f"HTML: `{html_path}`",
        "",
        "## Проверки",
        "",
        "- Проверена структура source-map.",
        "- Проверено наличие обязательных deliverables.",
        "- Проверено наличие `AURA_SHAPE_MAP.json` и `AURA_FONT_MATCH.md`.",
        "- Проверены visual-diff gate и reviewer-pass артефакты.",
        "- Проверено наличие ключевого headline/image в HTML.",
        "- Проверена доступность всех `<img src>` из HTML.",
        "- Проверен `AURA_ASSET_REGISTRY.json` для MCP KV ассетов.",
        "- Проверен overlap hero-person asset: низ фигуры должен уходить под второй блок, а не обрываться на синем фоне.",
        "- Проверены placeholder/lorem/emoji markers.",
        "- Screenshot diff требует запуска в Cursor/browser среде.",
        "",
        "## Findings",
        "",
    ]

    if findings:
        for level, message in findings:
            lines.append(f"- **{level.upper()}**: {message}")
    else:
        lines.append("- Критических структурных проблем не найдено.")

    lines.extend([
        "",
        "## Что нужно для pixel-perfect QA",
        "",
        "- Сделать screenshot источника и результата на 1440px, 768px, 375px.",
        "- Заполнить `AURA_VISUAL_DIFF.md` по зонам Hero/Typography/Shapes/Spacing/Colors.",
        "- Запустить `aura-design-reviewer` и заполнить `AURA_REVIEWER_PASS.md`.",
        "- Проверить координаты hero image и headline side-by-side.",
        "- Проверить масштаб, z-index, интервалы, сетку, цвета и mobile overflow.",
    ])
    return "\n".join(lines) + "\n", status


def main():
    parser = argparse.ArgumentParser(description="Aura Designer Visual QA")
    parser.add_argument("--source-map", default="AURA_SOURCE_MAP.json")
    parser.add_argument("--html", default="index.html")
    parser.add_argument("--output", default="AURA_VISUAL_QA.md")
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    report, status = build_report(args.source_map, args.html, args.output_dir)
    with open(args.output, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"[QA] Статус: {status}")
    print(f"[OK] Отчет сохранен: {args.output}")
    if status == "FAIL":
        sys.exit(2)


if __name__ == "__main__":
    main()
