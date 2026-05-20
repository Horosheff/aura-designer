#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AuraDesign Agent - Asset Coordinator Module (Anti-Slop Edition)
===============================================================
Обеспечивает стыковку с ИИ-генератором ассетов. Так как лучшая генерация 
и удаление фона происходят напрямую на стороне ИИ-агента через MCP (Kie.ai и Recraft AI),
этот модуль координирует получение ссылок на прозрачные PNG и предоставляет
премиальные, заранее выверенные безфоновые фоллбеки для автономной работы.
"""

import os
import sys

# Качественные безфоновые (прозрачные PNG) ассеты-фоллбеки по нишам для стабильной автономной работы
FALLBACK_TRANSPARENT_ASSETS = {
    "weather": "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000033471f7ae58711261f28d8d.png", # 3D Glass Weather Widget
    "pets": "https://tempfile.aiquickdraw.com/images/chatgpt/file_000000009c4871fd89659ba12323bdd7.png",    # Happy Golden Retriever
    "saas": "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000d2e071fd928759dd666866cf.png",    # SaaS Minimalist Dashboard
    "cosmic": "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000ceb071fd8302fcb47b4ae68c.png",  # Cosmic ring / Totality
    "alpinism": "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000f40471f8abe607450f3f6b38.png", # Mechanical High Fidelity device
    "bumaga": "https://tempfile.aiquickdraw.com/r/e693d4dd2cb169eb7929ba6e469730ff_1779311482_3qzc84uf.png", # Generated and background-removed premium 3D folder asset
    "default": "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000e75071fd9fd1f9c4b7258abd.png"  # Abstract Floating Shapes
}


def get_premium_asset(niche_keyword):
    """
    Основной метод извлечения премиального ассета.
    Автоматически подбирает наилучший фоллбек по ключевым словам ниши.
    Интеграция с MCP gpt-image-2 + recraft_remove_background выполняется ИИ-агентом напрямую.
    """
    niche_keyword = niche_keyword.lower()
    selected_asset = FALLBACK_TRANSPARENT_ASSETS["default"]
    niche_type = "default"
    
    if "weather" in niche_keyword or "glass" in niche_keyword or "forecast" in niche_keyword:
        selected_asset = FALLBACK_TRANSPARENT_ASSETS["weather"]
        niche_type = "weather"
    elif "pet" in niche_keyword or "paw" in niche_keyword or "dog" in niche_keyword or "animal" in niche_keyword:
        selected_asset = FALLBACK_TRANSPARENT_ASSETS["pets"]
        niche_type = "pets"
    elif "saas" in niche_keyword or "tech" in niche_keyword or "dashboard" in niche_keyword or "finance" in niche_keyword:
        selected_asset = FALLBACK_TRANSPARENT_ASSETS["saas"]
        niche_type = "saas"
    elif "cosmic" in niche_keyword or "totality" in niche_keyword or "eclipse" in niche_keyword:
        selected_asset = FALLBACK_TRANSPARENT_ASSETS["cosmic"]
        niche_type = "cosmic"
    elif "alpine" in niche_keyword or "observatory" in niche_keyword or "alpinism" in niche_keyword or "scientific" in niche_keyword:
        selected_asset = FALLBACK_TRANSPARENT_ASSETS["alpinism"]
        niche_type = "alpinism"
    elif "bumaga" in niche_keyword or "bureau" in niche_keyword or "бумага" in niche_keyword:
        selected_asset = FALLBACK_TRANSPARENT_ASSETS["bumaga"]
        niche_type = "bumaga"
        
    print(f"[Asset] Выбран оптимальный автономный ассет для ниши [{niche_type}]: {selected_asset}")
    return selected_asset


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AuraDesign Agent Asset Coordinator CLI")
    parser.add_argument("--niche", default="default", help="Ключевое слово ниши (weather, pets, saas, default)")
    parser.add_argument("--prompt", default="", help="Кастомный текстовый промпт для генерации картинки (обрабатывается ИИ-агентом)")
    
    args = parser.parse_args()
    
    print("[Asset] Координатор Ассетов AuraDesign запущен.")
    
    # ИИ-агент перехватывает этот вызов и подставляет реальный сгенерированный URL
    # Если запуск автономный - берётся качественный фоллбек по нише
    asset_url = get_premium_asset(args.niche)
    
    # Логируем результат для генератора
    print(f"RESULT_ASSET_URL={asset_url}")


if __name__ == "__main__":
    main()
