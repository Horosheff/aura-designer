#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AuraDesign Agent - Main CLI Interface
=====================================
Главная консольная утилита управления экосистемой AuraDesign.
Объединяет сканирование, source-map анализ, управление ассетами и генерацию сайтов.
"""

import os
import sys
import argparse
import subprocess

# Настройка кодировки вывода для стабильной печати в Windows консоли
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ASCII_ART = r"""
   _                       ____            _             
  / \  _   _ _ __ __ _    |  _ \  ___  ___(_) __ _ _ __  
 / _ \| | | | '__/ _` |   | | | |/ _ \/ __| |/ _` | '_ \ 
/ ___ \ |_| | | | (_| |   | |_| |  __/\__ \ | (_| | | | |
/_/   \_\__,_/_|  \__,_|___|____/ \___||___/_|\__, |_| |_|
                      |_____|                 |___/      
              * Intelligent AI Design System *
"""

FALLBACK_CONTRACT = "AURADESIGN.md"
FALLBACK_HTML = "index.html"


def run_script(script_name, args_list):
    """Безопасно запускает дочерний скрипт внутри папки агента"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    cmd = [sys.executable, script_path] + args_list
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", env=env)
        if res.returncode != 0:
            print(f"[Error] Ошибка выполнения {script_name}:\n{res.stderr}", file=sys.stderr)
            return False, res.stdout
        return True, res.stdout
    except Exception as e:
        print(f"[Error] Ошибка запуска {script_name}: {e}", file=sys.stderr)
        return False, ""


def handle_scan(args):
    """Обработчик команды scan"""
    print("[Scan] Запуск интеллектуального сканера...")
    scanner_args = []
    if args.url:
        scanner_args += ["--url", args.url]
    elif args.image:
        scanner_args += ["--image", args.image]
        
    if args.dark:
        scanner_args.append("--dark")
        
    contract_path = args.output or FALLBACK_CONTRACT
    scanner_args += ["--output", contract_path]
    
    success, output = run_script("aura_scanner.py", scanner_args)
    if success:
        print(output.strip())
        print("[OK] Контракт успешно подготовлен!")
        source = args.url or args.image or ""
        deliverables_args = [
            "--contract", contract_path,
            "--source", source,
            "--output-dir", os.path.dirname(contract_path) or ".",
        ]
        deliverables_success, deliverables_output = run_script("aura_deliverables.py", deliverables_args)
        if deliverables_success and deliverables_output.strip():
            print(deliverables_output.strip())
    else:
        sys.exit(1)


def handle_analyze(args):
    """Создает машинные карты источника для copy-in-copy режима"""
    analyzer_args = ["--output-dir", args.output_dir or "."]
    if args.url:
        analyzer_args += ["--url", args.url]
    elif args.image:
        analyzer_args += ["--image", args.image]

    success, output = run_script("aura_source_analyzer.py", analyzer_args)
    if success:
        print(output.strip())
    else:
        sys.exit(1)


def handle_preset(args):
    """Пресеты удалены: они провоцировали style bleeding."""
    print("[Preset][DEPRECATED] Папка пресетов удалена намеренно.")
    print("[Preset][DEPRECATED] Aura Designer работает от источника: scan/analyze -> AURADESIGN.md -> replicate.")
    print("[Preset][DEPRECATED] Используйте `scan` для нового контракта или `analyze` + `replicate` для copy-in-copy.")
    sys.exit(2)


def handle_generate(args):
    """Обработчик команды generate"""
    print("[Generate] Старт генерации интерфейса...")
    
    contract_path = args.contract or FALLBACK_CONTRACT
    if not os.path.exists(contract_path):
        print(f"[Generate][BLOCKED] Контракт не найден: {contract_path}", file=sys.stderr)
        print("[Generate][BLOCKED] Пресеты удалены, автоподмена шаблоном запрещена. Сначала создайте AURADESIGN.md через `scan` или вручную.", file=sys.stderr)
        sys.exit(1)

    # 1. Получаем только реальный MCP KV ассет. Фоллбеки запрещены.
    print("[Generate] Проверка MCP KV ассета...")
    asset_args = ["--niche", args.niche]
    if args.prompt:
        asset_args += ["--prompt", args.prompt]
    if getattr(args, "asset_url", None):
        asset_args += ["--mcp-asset-url", args.asset_url]
        
    success, asset_output = run_script("aura_asset_manager.py", asset_args)
    
    asset_url = ""
    if success:
        # Извлекаем RESULT_ASSET_URL из логов
        for line in asset_output.split("\n"):
            if line.startswith("RESULT_ASSET_URL="):
                asset_url = line.split("=")[1].strip()
                break
                
    if not asset_url:
        print("[Generate][BLOCKED] Ссылка на MCP KV ассет не получена. Нельзя собирать страницу с картинкой-заглушкой.", file=sys.stderr)
        sys.exit(2)
        
    # 2. Передаём ассет генератору и собираем страницу
    print("[Generate] Генерация и сборка адаптивного HTML/CSS кода...")
    generator_args = ["--contract", contract_path, "--output", args.output or FALLBACK_HTML]
    if asset_url:
        generator_args += ["--hero-image", asset_url]
        
    success_gen, gen_output = run_script("aura_generator.py", generator_args)
    if success_gen:
        print(gen_output.strip())
        print(f"[OK] Сайт полностью собран! Файл сохранен по пути: {args.output or FALLBACK_HTML}")
    else:
        sys.exit(1)


def handle_replicate(args):
    """Генерирует страницу по AURA_SOURCE_MAP.json без архетипной вольности"""
    replicator_args = [
        "--source-map", args.source_map or "AURA_SOURCE_MAP.json",
        "--contract", args.contract or FALLBACK_CONTRACT,
        "--output", args.output or FALLBACK_HTML,
    ]
    if args.asset_url:
        replicator_args += ["--asset-url", args.asset_url]

    success, output = run_script("aura_replicator.py", replicator_args)
    if success:
        print(output.strip())
    else:
        sys.exit(1)


def handle_deliverables(args):
    """Создает обязательные аналитические файлы вокруг AURADESIGN.md"""
    contract_path = args.contract or FALLBACK_CONTRACT
    if not os.path.exists(contract_path):
        print(f"[Error] Контракт не найден: {contract_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or (os.path.dirname(contract_path) or ".")
    deliverables_args = [
        "--contract", contract_path,
        "--source", args.source or "",
        "--output-dir", output_dir,
        "--html", args.html or FALLBACK_HTML,
    ]
    success, output = run_script("aura_deliverables.py", deliverables_args)
    if success:
        print(output.strip())
    else:
        sys.exit(1)


def handle_lint(args):
    """Проверяет AURADESIGN.md на глубину и обязательные правила"""
    lint_args = ["--contract", args.contract or FALLBACK_CONTRACT]
    if args.output:
        lint_args += ["--output", args.output]
    success, output = run_script("aura_linter.py", lint_args)
    print(output.strip())
    if not success:
        sys.exit(1)


def handle_qa(args):
    """Создает структурный QA-отчет по source-map и HTML"""
    qa_args = [
        "--source-map", args.source_map or "AURA_SOURCE_MAP.json",
        "--html", args.html or FALLBACK_HTML,
        "--output", args.output or "AURA_VISUAL_QA.md",
        "--output-dir", args.output_dir or ".",
    ]
    success, output = run_script("aura_visual_qa.py", qa_args)
    print(output.strip())
    if not success:
        sys.exit(1)


def handle_pipeline(args):
    """Обработчик сквозного конвейера pipeline"""
    print("[Pipeline] Запуск сквозного конвейера AuraDesign Pipeline...")
    
    # 1. Сканируем сайт и генерируем контракт
    print("\n--- ЭТАП 1: Сканирование сайта и построение дизайн-контракта ---")
    scan_args = argparse.Namespace(url=args.url, image=None, dark=args.dark, output=FALLBACK_CONTRACT)
    handle_scan(scan_args)

    # 1.5. Строим машинные карты источника для режима copy-in-copy
    print("\n--- ЭТАП 1.5: Анализ источника и построение source maps ---")
    analyze_args = argparse.Namespace(url=args.url, image=None, output_dir=os.path.dirname(args.output or FALLBACK_HTML) or ".")
    handle_analyze(analyze_args)
    
    # 2. Определяем нишу по названию сайта для подбора ассетов
    niche = "saas"
    if args.url:
        url_lower = args.url.lower()
        if "weather" in url_lower:
            niche = "weather"
        elif "pet" in url_lower or "dog" in url_lower or "animal" in url_lower:
            niche = "pets"
        elif "finance" in url_lower or "crypto" in url_lower or "wallet" in url_lower:
            niche = "fintech"
            
    # 3. Собираем source-accurate реплику
    print("\n--- ЭТАП 2: Copy-in-copy сборка HTML по source map ---")
    output_dir = os.path.dirname(args.output or FALLBACK_HTML) or "."
    replica_args = argparse.Namespace(
        source_map=os.path.join(output_dir, "AURA_SOURCE_MAP.json"),
        contract=FALLBACK_CONTRACT,
        output=args.output or FALLBACK_HTML,
        asset_url=None,
    )
    handle_replicate(replica_args)

    # 4. Создаем карту репликации, brand-kit prompt и психологию цвета
    print("\n--- ЭТАП 3: Аналитические deliverables и brand-kit бриф ---")
    deliverables_args = argparse.Namespace(
        contract=FALLBACK_CONTRACT,
        source=args.url,
        output_dir=output_dir,
        html=args.output or FALLBACK_HTML,
    )
    handle_deliverables(deliverables_args)

    # 5. Структурный QA-отчет
    print("\n--- ЭТАП 4: QA source-accurate результата ---")
    qa_args = argparse.Namespace(
        source_map=os.path.join(output_dir, "AURA_SOURCE_MAP.json"),
        html=args.output or FALLBACK_HTML,
        output=os.path.join(output_dir, "AURA_VISUAL_QA.md"),
        output_dir=output_dir,
    )
    handle_qa(qa_args)
    
    print("\n[OK] Сквозной пайплайн успешно выполнен!")


def main():
    print(ASCII_ART)
    
    parser = argparse.ArgumentParser(description="AuraDesign Agent - CLI Управление")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")
    
    # Команда scan
    scan_parser = subparsers.add_parser("scan", help="Сканирует веб-ресурс или изображение для создания контракта")
    scan_group = scan_parser.add_mutually_exclusive_group(required=True)
    scan_group.add_argument("--url", help="URL веб-сайта для анализа стиля")
    scan_group.add_argument("--image", help="Путь к картинке для визуального анализа")
    scan_parser.add_argument("--dark", action="store_true", help="Сгенерировать тёмную тему")
    scan_parser.add_argument("--output", help="Файл сохранения контракта (по умолчанию AURADESIGN.md)")

    # Команда analyze
    analyze_parser = subparsers.add_parser("analyze", help="Создает AURA_SOURCE_MAP.json, AURA_COMPOSITION_LOCK.json и AURA_COMPONENT_MAP.json")
    analyze_group = analyze_parser.add_mutually_exclusive_group(required=True)
    analyze_group.add_argument("--url", help="URL источника")
    analyze_group.add_argument("--image", help="Путь или URL изображения-референса")
    analyze_parser.add_argument("--output-dir", help="Папка для source-map файлов")
    
    # Команда preset (deprecated)
    preset_parser = subparsers.add_parser("preset", help="DEPRECATED: пресеты удалены, используйте scan/analyze/replicate")
    preset_parser.add_argument("niche", help="Имя старого пресета (команда больше не используется)")
    preset_parser.add_argument("--output", help="Файл сохранения контракта (по умолчанию AURADESIGN.md)")
    
    # Команда generate
    generate_parser = subparsers.add_parser("generate", help="Сборка сайта на основе контракта")
    generate_parser.add_argument("--contract", help="Файл дизайн-контракта (по умолчанию AURADESIGN.md)")
    generate_parser.add_argument("--niche", default="saas", help="Ниша подбора ассета (saas, fintech, glassmorphism, pets, cosmic, alpinism, bumaga)")
    generate_parser.add_argument("--prompt", help="Кастомный ИИ-промпт для генерации картинки")
    generate_parser.add_argument("--asset-url", help="URL прозрачного ассета, полученный через MCP KV recraft_remove_background")
    generate_parser.add_argument("--output", help="Файл сохранения сайта (по умолчанию index.html)")

    # Команда replicate
    replicate_parser = subparsers.add_parser("replicate", help="Copy-in-copy генерация по AURA_SOURCE_MAP.json")
    replicate_parser.add_argument("--source-map", help="Путь к AURA_SOURCE_MAP.json")
    replicate_parser.add_argument("--contract", help="Файл дизайн-контракта")
    replicate_parser.add_argument("--output", help="Файл сохранения HTML")
    replicate_parser.add_argument("--asset-url", help="Принудительный URL hero-ассета")

    # Команда deliverables
    deliverables_parser = subparsers.add_parser("deliverables", help="Создает todo, source analysis, brand-kit prompt и психологию цвета")
    deliverables_parser.add_argument("--contract", help="Файл дизайн-контракта (по умолчанию AURADESIGN.md)")
    deliverables_parser.add_argument("--source", help="URL, изображение или описание источника")
    deliverables_parser.add_argument("--output-dir", help="Папка для аналитических файлов")
    deliverables_parser.add_argument("--html", help="Целевой HTML-файл")

    # Команда lint
    lint_parser = subparsers.add_parser("lint", help="Проверяет AURADESIGN.md на обязательные разделы и anti-slop правила")
    lint_parser.add_argument("--contract", help="Файл дизайн-контракта")
    lint_parser.add_argument("--output", help="Файл отчета")

    # Команда qa
    qa_parser = subparsers.add_parser("qa", help="Создает AURA_VISUAL_QA.md по source-map и HTML")
    qa_parser.add_argument("--source-map", help="Путь к AURA_SOURCE_MAP.json")
    qa_parser.add_argument("--html", help="HTML для проверки")
    qa_parser.add_argument("--output", help="Файл QA-отчета")
    qa_parser.add_argument("--output-dir", help="Папка обязательных deliverables")
    
    # Команда pipeline
    pipeline_parser = subparsers.add_parser("pipeline", help="Сквозной пайплайн: сканирование -> контракт -> ассеты -> сайт")
    pipeline_parser.add_argument("--url", required=True, help="URL сайта для репликации")
    pipeline_parser.add_argument("--dark", action="store_true", help="Сгенерировать тёмную тему")
    pipeline_parser.add_argument("--output", help="Файл сохранения готового сайта (по умолчанию index.html)")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        handle_scan(args)
    elif args.command == "analyze":
        handle_analyze(args)
    elif args.command == "preset":
        handle_preset(args)
    elif args.command == "generate":
        handle_generate(args)
    elif args.command == "replicate":
        handle_replicate(args)
    elif args.command == "deliverables":
        handle_deliverables(args)
    elif args.command == "lint":
        handle_lint(args)
    elif args.command == "qa":
        handle_qa(args)
    elif args.command == "pipeline":
        handle_pipeline(args)


if __name__ == "__main__":
    main()
