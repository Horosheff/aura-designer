#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aura Designer installer for Cursor / Claude Code / Codex.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


TARGETS = {
    "cursor": {
        "source": ROOT / ".cursor" / "agents",
        "project": Path(".cursor") / "agents",
        "global": Path.home() / ".cursor" / "agents",
    },
    "claude": {
        "source": ROOT / ".claude" / "agents",
        "project": Path(".claude") / "agents",
        "global": Path.home() / ".claude" / "agents",
    },
    "codex": {
        "source": ROOT / ".codex" / "agents",
        "project": Path(".codex") / "agents",
        "global": Path.home() / ".codex" / "agents",
    },
}


def copy_agents(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    copied = []
    for file in source.glob("*.md"):
        target = destination / file.name
        shutil.copy2(file, target)
        copied.append(target)
    return copied


def main():
    parser = argparse.ArgumentParser(description="Установщик Aura Designer")
    parser.add_argument("--target", choices=TARGETS.keys(), required=True, help="Куда установить: cursor, claude, codex")
    parser.add_argument("--scope", choices=["project", "global"], default="project", help="Установка в проект или глобально")
    parser.add_argument("--project-dir", default=".", help="Путь к проекту для scope=project")
    args = parser.parse_args()

    config = TARGETS[args.target]
    source = config["source"]
    if args.scope == "global":
        destination = config["global"]
    else:
        destination = Path(args.project_dir).resolve() / config["project"]

    copied = copy_agents(source, destination)
    print(f"[OK] Aura Designer установлен для {args.target} ({args.scope})")
    for file in copied:
        print(f"- {file}")


if __name__ == "__main__":
    main()
