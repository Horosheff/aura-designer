#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AuraDesign Agent - MCP Asset Gate
=================================
Этот модуль не генерирует изображения сам и не выдает fallback-картинки.

Жесткое правило Aura Designer:
все новые hero/case-study/person/object изображения создаются через MCP KV
`gpt-image-2`, а прозрачные PNG — через MCP KV `recraft_remove_background`.
"""

import sys
import os

def resolve_mcp_asset(explicit_url=""):
    """Возвращает только реальный URL результата MCP KV."""
    return (
        explicit_url
        or os.environ.get("AURA_MCP_TRANSPARENT_ASSET_URL", "")
        or os.environ.get("AURA_MCP_ASSET_URL", "")
    ).strip()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AuraDesign Agent MCP Asset Gate CLI")
    parser.add_argument("--niche", default="default", help="Ключевое слово ниши (weather, pets, saas, default)")
    parser.add_argument("--prompt", default="", help="Промпт, который родительский агент обязан передать в MCP KV gpt-image-2")
    parser.add_argument("--mcp-asset-url", default="", help="URL прозрачного ассета, уже полученный через MCP KV")
    
    args = parser.parse_args()
    
    print("[Asset] MCP Asset Gate AuraDesign запущен.")
    asset_url = resolve_mcp_asset(args.mcp_asset_url)
    if not asset_url:
        print(
            "[Asset][BLOCKED] Нет URL ассета из MCP KV. Сначала вызовите user-mcp-kv/gpt-image-2, "
            "затем user-mcp-kv/recraft_remove_background и передайте прозрачный PNG через "
            "--mcp-asset-url или AURA_MCP_TRANSPARENT_ASSET_URL.",
            file=sys.stderr,
        )
        sys.exit(2)

    print(f"RESULT_ASSET_URL={asset_url}")


if __name__ == "__main__":
    main()
