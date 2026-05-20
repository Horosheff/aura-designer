#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aura Designer - Contract Linter
===============================
Проверяет AURADESIGN.md на глубину, обязательные разделы и anti-slop правила.
"""

import argparse
import re
import sys


REQUIRED_SECTIONS = [
    "Source Replication Doctrine",
    "Composition Lock",
    "Philosophy",
    "Color Guidance",
    "Typography",
    "Layout",
    "Component",
    "Do's and Don'ts",
]

REQUIRED_COLOR_KEYS = [
    "primary",
    "on-primary",
    "background",
    "on-background",
    "surface-lowest",
    "surface-low",
    "outline",
]


def lint_contract(content):
    findings = []
    lines = content.splitlines()

    if len(lines) < 120:
        findings.append(("high", "Контракт слишком короткий. Для Aura нужен глубокий AURADESIGN.md, обычно 120+ строк."))

    if not content.strip().startswith("---"):
        findings.append(("critical", "Нет YAML frontmatter в начале файла."))

    for section in REQUIRED_SECTIONS:
        if section.lower() not in content.lower():
            findings.append(("high", f"Отсутствует обязательный раздел или группа: `{section}`"))

    for key in REQUIRED_COLOR_KEYS:
        if not re.search(rf"^\s*{re.escape(key)}\s*:", content, flags=re.MULTILINE):
            findings.append(("medium", f"Отсутствует цветовой токен `{key}`"))

    if "user-mcp-kv/gpt-image-2" not in content:
        findings.append(("high", "Нет жесткого правила генерации изображений через `user-mcp-kv/gpt-image-2`."))

    if "user-mcp-kv/recraft_remove_background" not in content:
        findings.append(("high", "Нет жесткого правила удаления фона через `user-mcp-kv/recraft_remove_background`."))

    if "если доступны" in content.lower() and ("gpt-image-2" in content or "recraft_remove_background" in content):
        findings.append(("medium", "MCP KV правила сформулированы мягко через `если доступны`; для Aura это должен быть обязательный блокер."))

    if "psychology" not in content.lower() and "психолог" not in content.lower():
        findings.append(("low", "Нет упоминания психологии цвета или отдельного анализа цвета."))

    if re.search(r"[😀-🙏🌀-🗿🚀-🛿☀-⛿✂-➿]", content):
        findings.append(("medium", "В контракте найдены emoji/symbol markers. Для Aura UI это запрещено."))

    if "lorem" in content.lower() or "placeholder" in content.lower():
        findings.append(("medium", "Найдены placeholder/lorem маркеры."))

    return findings


def main():
    parser = argparse.ArgumentParser(description="AuraDesign contract linter")
    parser.add_argument("--contract", default="AURADESIGN.md")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    with open(args.contract, "r", encoding="utf-8") as file:
        content = file.read()

    findings = lint_contract(content)
    status = "PASS" if not any(level == "critical" for level, _ in findings) else "FAIL"

    report_lines = [
        "# AURA_LINT_REPORT",
        "",
        f"Контракт: `{args.contract}`",
        f"Статус: **{status}**",
        "",
        "## Findings",
        "",
    ]

    if findings:
        for level, message in findings:
            report_lines.append(f"- **{level.upper()}**: {message}")
    else:
        report_lines.append("- Нарушений не найдено.")

    report = "\n".join(report_lines) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(report)

    print(report)
    if status == "FAIL":
        sys.exit(2)


if __name__ == "__main__":
    main()
