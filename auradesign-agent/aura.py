#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AuraDesign Agent - Main CLI Interface
=====================================
Главная консольная утилита управления экосистемой AuraDesign.
Объединяет сканирование, пресеты, управление ассетами и генерацию сайтов.
"""

import os
import sys
import shutil
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

PRESETS_DIR = "presets"
FALLBACK_CONTRACT = "AURADESIGN.md"
FALLBACK_HTML = "index.html"


def run_script(script_name, args_list):
    """Безопасно запускает дочерний скрипт внутри папки агента"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    cmd = [sys.executable, script_path] + args_list
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
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
    else:
        sys.exit(1)


def handle_preset(args):
    """Обработчик команды preset"""
    print(f"[Preset] Импорт пресета для ниши [{args.niche}]...")
    preset_filename = f"{args.niche.lower()}.md"
    preset_path = os.path.join(os.path.dirname(__file__), PRESETS_DIR, preset_filename)
    
    if not os.path.exists(preset_path):
        available_presets = [f.split('.')[0] for f in os.listdir(os.path.join(os.path.dirname(__file__), PRESETS_DIR)) if f.endswith('.md')]
        print(f"[Error] Пресет '{args.niche}' не найден!", file=sys.stderr)
        print(f"[Preset] Доступные пресеты: {', '.join(available_presets)}", file=sys.stderr)
        sys.exit(1)
        
    output_path = args.output or FALLBACK_CONTRACT
    try:
        shutil.copy(preset_path, output_path)
        print(f"[OK] Пресет успешно скопирован в: {output_path}")
        print("[Preset] Теперь вы можете отредактировать токены или сразу запустить генерацию сайта.")
    except Exception as e:
        print(f"[Error] Ошибка копирования пресета: {e}", file=sys.stderr)
        sys.exit(1)


def handle_generate(args):
    """Обработчик команды generate"""
    print("[Generate] Старт генерации интерфейса...")
    
    contract_path = args.contract or FALLBACK_CONTRACT
    if not os.path.exists(contract_path):
        print(f"[Generate] Контракт {contract_path} не найден. Пробуем скопировать пресет 'saas' по умолчанию...")
        # Копируем пресет saas как базовый
        default_preset = os.path.join(os.path.dirname(__file__), PRESETS_DIR, "saas.md")
        if os.path.exists(default_preset):
            shutil.copy(default_preset, contract_path)
            print(f"[OK] Скопирован пресет по умолчанию 'saas' -> {contract_path}")
        else:
            print("[Error] Ошибка: Нет файлов спецификации для сборки!", file=sys.stderr)
            sys.exit(1)

    # 1. Сначала подбираем/генерируем безфоновый ассет через Asset Manager
    print("[Generate] Поиск и оптимизация графических ассетов...")
    asset_args = ["--niche", args.niche]
    if args.prompt:
        asset_args += ["--prompt", args.prompt]
        
    success, asset_output = run_script("aura_asset_manager.py", asset_args)
    
    asset_url = ""
    if success:
        # Извлекаем RESULT_ASSET_URL из логов
        for line in asset_output.split("\n"):
            if line.startswith("RESULT_ASSET_URL="):
                asset_url = line.split("=")[1].strip()
                break
                
    if not asset_url:
        print("[Generate] Предупреждение: Ссылка на ассет не получена. Будет использован стандартный плейсхолдер.")
        
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


def handle_pipeline(args):
    """Обработчик сквозного конвейера pipeline"""
    print("[Pipeline] Запуск сквозного конвейера AuraDesign Pipeline...")
    
    # 1. Сканируем сайт и генерируем контракт
    print("\n--- ЭТАП 1: Сканирование сайта и построение дизайн-контракта ---")
    scan_args = argparse.Namespace(url=args.url, image=None, dark=args.dark, output=FALLBACK_CONTRACT)
    handle_scan(scan_args)
    
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
            
    # 3. Генерируем ассеты и собираем сайт
    print("\n--- ЭТАП 2: Подбор ассетов и сборка финального HTML ---")
    gen_args = argparse.Namespace(contract=FALLBACK_CONTRACT, niche=niche, prompt=None, output=args.output or FALLBACK_HTML)
    handle_generate(gen_args)
    
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
    
    # Команда preset
    preset_parser = subparsers.add_parser("preset", help="Копирует готовый пресет ниши в файл контракта")
    preset_parser.add_argument("niche", help="Имя ниши (saas, fintech, glassmorphism, pets, cosmic, alpinism, bumaga)")
    preset_parser.add_argument("--output", help="Файл сохранения контракта (по умолчанию AURADESIGN.md)")
    
    # Команда generate
    generate_parser = subparsers.add_parser("generate", help="Сборка сайта на основе контракта")
    generate_parser.add_argument("--contract", help="Файл дизайн-контракта (по умолчанию AURADESIGN.md)")
    generate_parser.add_argument("--niche", default="saas", help="Ниша подбора ассета (saas, fintech, glassmorphism, pets, cosmic, alpinism, bumaga)")
    generate_parser.add_argument("--prompt", help="Кастомный ИИ-промпт для генерации картинки")
    generate_parser.add_argument("--output", help="Файл сохранения сайта (по умолчанию index.html)")
    
    # Команда pipeline
    pipeline_parser = subparsers.add_parser("pipeline", help="Сквозной пайплайн: сканирование -> контракт -> ассеты -> сайт")
    pipeline_parser.add_argument("--url", required=True, help="URL сайта для репликации")
    pipeline_parser.add_argument("--dark", action="store_true", help="Сгенерировать тёмную тему")
    pipeline_parser.add_argument("--output", help="Файл сохранения готового сайта (по умолчанию index.html)")
    
    args = parser.parse_args()
    
    if args.command == "scan":
        handle_scan(args)
    elif args.command == "preset":
        handle_preset(args)
    elif args.command == "generate":
        handle_generate(args)
    elif args.command == "pipeline":
        handle_pipeline(args)


if __name__ == "__main__":
    main()
