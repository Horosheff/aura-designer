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

    required = [
        "AURA_REPLICATION_TODO.md",
        "AURA_SOURCE_ANALYSIS.md",
        "AURA_BRAND_KIT_IMAGE_PROMPT.md",
        "AURA_COLOR_PSYCHOLOGY.md",
        "AURA_SOURCE_MAP.json",
        "AURA_COMPOSITION_LOCK.json",
        "AURA_COMPONENT_MAP.json",
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
        "- Проверено наличие ключевого headline/image в HTML.",
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
