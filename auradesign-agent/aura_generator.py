#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AuraDesign Agent - Generator Module (Anti-Slop Edition)
======================================================
Считывает дизайн-контракт AURADESIGN.md, распознает визуальный архетип
и компилирует премиальную, интерактивную и полностью адаптивную страницу.
Категорически исключает использование эмодзи, заменяя их высокохудожественными
inline SVGs. Внедряет точные токены, физику слоев и микро-движения.
"""

import os
import sys
import re

# =========================================================================
# ВЕКТОРНЫЕ SVGS ДЛЯ КАЖДОГО ВИЗУАЛЬНОГО АРХЕТИПА (Заменяют дешевые эмодзи)
# =========================================================================

SVG_ICONS = {
    "saas": {
        "logo": """<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/></svg>""",
        "feature_1": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 012.008 1.24l.885 1.77a2.25 2.25 0 002.007 1.24h1.98a2.25 2.25 0 002.007-1.24l.885-1.77a2.25 2.25 0 012.007-1.24h3.86m-18 0h18a2.25 2.25 0 012.25 2.25v4.5A2.25 2.25 0 0119.5 21h-15A2.25 2.25 0 012.25 18.75v-4.5A2.25 2.25 0 012.25 13.5zm0-3h18A2.25 2.25 0 0022.5 8.25v-4.5A2.25 2.25 0 0019.5 1.5h-15A2.25 2.25 0 002.25 3.75v4.5A2.25 2.25 0 002.25 10.5z" />
        </svg>""", # Модульная архитектура
        "feature_2": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
        </svg>""", # Молниеносная скорость
        "feature_3": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>""" # Точность валидации
    },
    "fintech": {
        "logo": """<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>""",
        "feature_1": """<svg class="h-8 w-8 text-brand-primary animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
        </svg>""", # Безопасность / Криптография
        "feature_2": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18remL9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12V21h19.5" />
        </svg>""", # Свечной график котировок
        "feature_3": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 00-3.7-3.7 48.656 48.656 0 00-7.324 0 4.006 4.006 0 00-3.7 3.7C4.547 9.547 4.5 10.768 4.5 12s.047 2.453.138 3.662a4.006 4.006 0 003.7 3.7 48.656 48.656 0 007.324 0 4.006 4.006 0 003.7-3.7c.092-1.209.138-2.43.138-3.662z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 10.5l3 3 3-3" />
        </svg>""" # Быстрый обмен активов
    },
    "glassmorphism": {
        "logo": """<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v15.714a3 3 0 003 3h5.25a3 3 0 003-3V3.104a3 3 0 00-3-3h-5.25a3 3 0 00-3 3zM2.25 3.104v15.714a3 3 0 003 3h1.5a3 3 0 003-3V3.104a3 3 0 00-3-3h-1.5a3 3 0 00-3 3z"/></svg>""",
        "feature_1": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 21l8.188-5.096m-8.188 0l1.812-10.9L17.188 10.1l-1.188 5.804" />
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-dasharray="2 2" />
        </svg>""", # Оптическая линза / Призма
        "feature_2": """<svg class="h-8 w-8 text-brand-primary animate-spin" style="animation-duration: 20s" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1.5m0 15V21m-9-9h1.5m15 0H21m-15.364-6.364l1.06 1.06m8.607 8.607l1.06 1.06m-10.667 0l1.06-1.06m8.607-8.607l1.06-1.06" />
        </svg>""", # Свет / Дифракция
        "feature_3": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 010 12.728M16.463 8.288a5.25 5.25 0 010 7.424M6.75 8.25l4.72-4.72a.75.75 0 011.28.53v15.88a.75.75 0 01-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 012.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75z" />
        </svg>""" # Волна преломления
    },
    "pets": {
        "logo": """<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.01 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>""",
        "feature_1": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 111.086.797l-.041.02m-1.086-.797A1.5 1.5 0 1113.5 12h-2.25V9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
        </svg>""", # Золотая лапа заботы
        "feature_2": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
        </svg>""", # Любящее сердце
        "feature_3": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499c.172-.46 1.04-.46 1.212 0l2.125 5.641a.563.563 0 00.475.345l6.096.336c.496.027.697.64.31.954l-4.57 3.719a.563.563 0 00-.176.54l1.243 5.92c.11.527-.47.954-.925.645l-5.32-3.61a.563.563 0 00-.596 0l-5.32 3.61c-.454.31-1.034-.117-.925-.645l1.243-5.92a.563.563 0 00-.176-.54l-4.57-3.719c-.387-.313-.186-.927.31-.954l6.096-.336a.563.563 0 00.475-.345L11.48 3.5z" />
        </svg>""" # Звездные отзывы
    },
    "cosmic": {
        "logo": """<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="9" stroke="currentColor"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18M3 12h18"/></svg>""",
        "feature_1": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <ellipse cx="12" cy="12" rx="9" ry="3" stroke="currentColor" transform="rotate(-30 12 12)" />
            <circle cx="12" cy="12" r="4" fill="currentColor" />
        </svg>""", # Орбиты планет
        "feature_2": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3a9 9 0 109 9c0-1.232-.046-2.453-.138-3.662A9 9 0 0012 3z" fill="currentColor" fill-opacity="0.1" />
            <circle cx="12" cy="12" r="9" stroke="currentColor" />
        </svg>""", # Лунные фазы
        "feature_3": """<svg class="h-8 w-8 text-brand-primary animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="6" stroke="currentColor" />
            <path stroke-linecap="round" d="M12 2v2m0 14v2m-8-8h2m14 0h2m-13.364-5.364l1.414 1.414m8.486 8.486l1.414 1.414m-11.314 0l1.414-1.414m8.486-8.486l1.414-1.414" />
        </svg>""" # Солнечная корона
    },
    "alpinism": {
        "logo": """<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3L2 21h20L12 3zM12 8l5 9H7l5-9z"/></svg>""",
        "feature_1": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <circle cx="12" cy="12" r="10" stroke="currentColor"/>
            <path d="M12 2v20M2 12h20M12 6l3 6-3 6-3-6 3-6z" stroke="currentColor" fill="none" />
        </svg>""", # Роза ветров / Компас
        "feature_2": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <path d="M3 21h18M12 3l9 18H3L12 3z" stroke="currentColor" />
            <circle cx="12" cy="10" r="1" stroke="currentColor" />
            <path d="M12 10l-4 6h8l-4-6z" stroke="currentColor" fill="none" />
        </svg>""", # Секстант
        "feature_3": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <circle cx="12" cy="12" r="8" stroke="currentColor"/>
            <path d="M12 12l4-4M12 12v-6" stroke="currentColor" stroke-linecap="round" />
            <rect x="11" y="11" width="2" height="2" rx="1" fill="currentColor" />
        </svg>""" # Барометр прибора
    },
    "bumaga": {
        "logo": """<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/></svg>""",
        "feature_1": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>""", # Розовый стикер смайла
        "feature_2": """<svg class="h-8 w-8 text-brand-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>""", # Молния креатива
        "feature_3": """<svg class="h-8 w-8 text-brand-primary animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499c.172-.46 1.04-.46 1.212 0l2.125 5.641a.563.563 0 00.475.345l6.096.336c.496.027.697.64.31.954l-4.57 3.719a.563.563 0 00-.176.54l1.243 5.92c.11.527-.47.954-.925.645l-5.32-3.61a.563.563 0 00-.596 0l-5.32 3.61c-.454.31-1.034-.117-.925-.645l1.243-5.92a.563.563 0 00-.176-.54l-4.57-3.719c-.387-.313-.186-.927.31-.954l6.096-.336a.563.563 0 00.475-.345L11.48 3.5z" />
        </svg>""" # Взрывная звезда
    }
}


def parse_yaml_front_matter(content):
    """Парсер Front Matter без сторонних библиотек"""
    lines = content.split('\n')
    yaml_lines = []
    in_yaml = False
    
    for line in lines:
        if line.strip() == '---':
            if not in_yaml:
                in_yaml = True
                continue
            else:
                break
        if in_yaml:
            yaml_lines.append(line)
            
    tokens = {}
    current_key_path = []
    
    for line in yaml_lines:
        if not line.strip() or line.strip().startswith('#'):
            continue
            
        indent = len(line) - len(line.lstrip())
        level = indent // 2
        current_key_path = current_key_path[:level]
        
        parts = line.strip().split(':', 1)
        key = parts[0].strip()
        val_raw = parts[1].strip() if len(parts) > 1 else ""
        
        # Clean inline comments
        val = val_raw
        if val:
            if (val.startswith('"') and '"' in val[1:]) or (val.startswith("'") and "'" in val[1:]):
                quote_char = val[0]
                closing_idx = val.find(quote_char, 1)
                if closing_idx != -1:
                    val = val[:closing_idx + 1]
            elif '#' in val:
                if val.startswith('#'):
                    words = val.split()
                    val = words[0]
                else:
                    val = val.split('#', 1)[0].strip()
                    
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
            
        parent = tokens
        for p in current_key_path:
            parent = parent[p]
            
        if val == "":
            parent[key] = {}
            current_key_path.append(key)
        else:
            parent[key] = val
            
    return tokens


def resolve_token_references(tokens):
    """Разрешение ссылок типа {colors.primary}"""
    def get_by_path(dct, path_str):
        parts = path_str.split('.')
        curr = dct
        for p in parts:
            if isinstance(curr, dict) and p in curr:
                curr = curr[p]
            else:
                return None
        return curr

    def resolve_value(val):
        if not isinstance(val, str):
            return val
        
        matches = re.findall(r'\{([a-zA-Z0-9\._\-]+)\}', val)
        if not matches:
            return val
            
        resolved_val = val
        for match in matches:
            token_val = get_by_path(tokens, match)
            if token_val:
                token_val = resolve_value(token_val)
                resolved_val = resolved_val.replace(f"{{{match}}}", str(token_val))
                
        return resolved_val

    def resolve_dict(dct):
        for k, v in dct.items():
            if isinstance(v, dict):
                resolve_dict(v)
            else:
                dct[k] = resolve_value(v)

    resolve_dict(tokens)
    return tokens


def get_token(tokens, path, default=""):
    """Безопасное извлечение токена"""
    parts = path.split('.')
    curr = tokens
    for p in parts:
        if isinstance(curr, dict) and p in curr:
            curr = curr[p]
        else:
            return default
    return curr


def get_rgb_channels(hex_color):
    """Конвертация HEX в RGB"""
    hex_color = str(hex_color).lstrip('#')
    if len(hex_color) == 3:
        hex_color = "".join([c*2 for c in hex_color])
    if len(hex_color) != 6:
        return "79, 70, 229"
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r}, {g}, {b}"
    except ValueError:
        return "79, 70, 229"


def generate_html_page(tokens, hero_image_url=""):
    """Генерирует HTML страницу с учетом токенов и выбранного архетипа"""
    tokens = resolve_token_references(tokens)
    
    sys_name = get_token(tokens, 'name', 'AuraDesign System')
    sys_desc = get_token(tokens, 'description', 'Премиальный современный адаптивный сайт.')
    
    # Пытаемся автоматически определить архетип по имени системы
    sys_name_lower = sys_name.lower()
    archetype = "saas"
    
    if "fintech" in sys_name_lower or "slate" in sys_name_lower:
        archetype = "fintech"
    elif "glassmorphism" in sys_name_lower or "glass" in sys_name_lower or "атмосферное" in sys_name_lower:
        archetype = "glassmorphism"
    elif "pet" in sys_name_lower or "paw" in sys_name_lower or "friend" in sys_name_lower or "животн" in sys_name_lower:
        archetype = "pets"
    elif "cosmic" in sys_name_lower or "totality" in sys_name_lower or "затмени" in sys_name_lower:
        archetype = "cosmic"
    elif "alpine" in sys_name_lower or "observatory" in sys_name_lower or "альпий" in sys_name_lower:
        archetype = "alpinism"
    elif "bumaga" in sys_name_lower or "bureau" in sys_name_lower or "бумага" in sys_name_lower or "workspacestorage" in sys_name_lower or "users" in sys_name_lower:
        archetype = "bumaga"
        
    print(f"[Generate] Архетип страницы определен как [{archetype.upper()}] на основе '{sys_name}'")
    
    # Цвета
    c_primary = get_token(tokens, 'colors.primary', '#4f46e5')
    c_primary_hover = get_token(tokens, 'colors.primary-hover', c_primary)
    c_on_primary = get_token(tokens, 'colors.on-primary', '#ffffff')
    c_secondary = get_token(tokens, 'colors.secondary', '#06b6d4')
    c_on_secondary = get_token(tokens, 'colors.on-secondary', '#ffffff')
    c_tertiary = get_token(tokens, 'colors.tertiary', '#0066ff')
    c_on_tertiary = get_token(tokens, 'colors.on-tertiary', '#ffffff')
    c_background = get_token(tokens, 'colors.background', '#f8fafc')
    c_on_background = get_token(tokens, 'colors.on-background', '#0f172a')
    
    c_surface_lowest = get_token(tokens, 'colors.surface-lowest', '#ffffff')
    c_surface_low = get_token(tokens, 'colors.surface-low', '#f1f5f9')
    c_surface_container = get_token(tokens, 'colors.surface-container', '#e2e8f0')
    c_surface_high = get_token(tokens, 'colors.surface-high', '#cbd5e1')
    
    c_outline = get_token(tokens, 'colors.outline', '#94a3b8')
    c_outline_variant = get_token(tokens, 'colors.outline-variant', '#e2e8f0')
    
    # Радиусы
    r_sm = get_token(tokens, 'rounded.sm', '4px')
    r_default = get_token(tokens, 'rounded.DEFAULT', '8px')
    r_md = get_token(tokens, 'rounded.md', '12px')
    r_lg = get_token(tokens, 'rounded.lg', '16px')
    r_xl = get_token(tokens, 'rounded.xl', '24px')
    
    # Шрифты
    font_main = get_token(tokens, 'typography.display-lg.fontFamily', 'Satoshi')
    font_body = get_token(tokens, 'typography.body-md.fontFamily', 'Geist')
    
    # Загрузка веб-шрифтов (если кастомные)
    custom_fonts_link = ""
    font_main_clean = font_main.replace(" ", "+")
    font_body_clean = font_body.replace(" ", "+")
    
    if archetype == "alpinism":
        custom_fonts_link = f"""<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">"""
    elif archetype == "cosmic":
        custom_fonts_link = f"""<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Satoshi:wght@400;500;700&display=swap" rel="stylesheet">"""
    elif archetype == "bumaga":
        custom_fonts_link = f"""<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;500;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">"""
    else:
        custom_fonts_link = f"""<link href="https://fonts.googleapis.com/css2?family={font_main_clean}:wght@500;600;700;800&family={font_body_clean}:wght@300;400;500;600&display=swap" rel="stylesheet">"""

    # Установка дефолтного ИИ ассета
    if not hero_image_url:
        if archetype == "pets":
            hero_image_url = "https://tempfile.aiquickdraw.com/images/chatgpt/file_000000009c4871fd89659ba12323bdd7.png" # Happy Dog
        elif archetype == "glassmorphism":
            hero_image_url = "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000033471f7ae58711261f28d8d.png" # Glass weather widget
        elif archetype == "alpinism":
            hero_image_url = "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000e75071fd9fd1f9c4b7258abd.png" # Astrolabe or similar abstract
        elif archetype == "cosmic":
            hero_image_url = "https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000ceb071fd8302fcb47b4ae68c.png" # Cosmic ring
        elif archetype == "bumaga":
            hero_image_url = "https://tempfile.aiquickdraw.com/r/e693d4dd2cb169eb7929ba6e469730ff_1779311482_3qzc84uf.png" # Generated and background-removed premium 3D folder asset
        else:
            hero_image_url = "https://tempfile.aiquickdraw.com/images/chatgpt/file_000000004ed0720c830c95b8588d0d9b.png" # Minimal dashboard

    # Специфические CSS эффекты для разных архетипов
    extra_styles = ""
    ambient_shadows_class = ""
    
    if archetype == "glassmorphism":
        extra_styles = f"""
        body {{
            background: radial-gradient(circle at 80% 20%, rgba({get_rgb_channels(c_secondary)}, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 10% 80%, rgba({get_rgb_channels(c_primary)}, 0.12) 0%, transparent 50%),
                        {c_background};
        }}
        .glass-panel {{
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }}
        .glass-panel-elevated {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 16px 48px 0 rgba(0, 0, 0, 0.4);
        }}
        """
    elif archetype == "pets":
        extra_styles = f"""
        .shadow-ambient-warm {{
            box-shadow: 0 20px 40px -10px rgba({get_rgb_channels(c_primary)}, 0.06), 0 10px 20px -5px rgba({get_rgb_channels(c_primary)}, 0.04);
        }}
        .shadow-ambient-warm:hover {{
            box-shadow: 0 30px 50px -12px rgba({get_rgb_channels(c_primary)}, 0.12), 0 15px 25px -8px rgba({get_rgb_channels(c_primary)}, 0.08);
        }}
        .shadow-ambient-blue {{
            box-shadow: 0 20px 40px -10px rgba({get_rgb_channels(c_secondary)}, 0.06), 0 10px 20px -5px rgba({get_rgb_channels(c_secondary)}, 0.04);
        }}
        """
    elif archetype == "cosmic":
        extra_styles = f"""
        body {{
            background: radial-gradient(circle at 50% -20%, rgba({get_rgb_channels(c_primary)}, 0.08) 0%, transparent 60%),
                        radial-gradient(circle at 90% 80%, rgba({get_rgb_channels(c_secondary)}, 0.05) 0%, transparent 50%),
                        {c_background};
        }}
        .obsidian-card {{
            background: {c_surface_lowest};
            border: 1px solid {c_outline_variant};
            box-shadow: 0 20px 50px -15px rgba({get_rgb_channels(c_primary)}, 0.03);
            transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .obsidian-card:hover {{
            border-color: {c_secondary};
            box-shadow: 0 30px 60px -10px rgba({get_rgb_channels(c_secondary)}, 0.08);
            transform: translateY(-2px);
        }}
        """
    elif archetype == "alpinism":
        extra_styles = f"""
        .alpine-grid {{
            background-image: radial-gradient({c_outline_variant} 1px, transparent 1px);
            background-size: 24px 24px;
        }}
        .scientific-border {{
            border: 1px solid {c_outline_variant};
            position: relative;
        }}
        .scientific-border::before, .scientific-border::after {{
            content: '+';
            position: absolute;
            color: {c_outline};
            font-family: 'IBM Plex Mono', monospace;
            font-size: 14px;
            font-weight: 300;
        }}
        .scientific-border-tl::before {{ top: -8px; left: -6px; }}
        .scientific-border-tr::after {{ top: -8px; right: -6px; }}
        """
    elif archetype == "bumaga":
        extra_styles = f"""
        body {{
            background-color: {c_background};
            color: {c_on_background};
        }}
        /* Neo-brutalist buttons override */
        .btn-primary {{
            background-color: var(--brand-primary) !important;
            color: var(--brand-on-primary) !important;
            border: 3px solid #0c0e13 !important;
            border-radius: var(--radius-md) !important;
            box-shadow: 4px 4px 0px #0c0e13 !important;
            transition: all 100ms ease-out !important;
        }}
        .btn-primary:hover {{
            background-color: var(--brand-primary-hover) !important;
            transform: translate(2px, 2px) !important;
            box-shadow: 2px 2px 0px #0c0e13 !important;
        }}
        .btn-primary:active {{
            transform: translate(4px, 4px) !important;
            box-shadow: 0px 0px 0px #0c0e13 !important;
        }}
        
        .card-interactive {{
            background-color: {c_surface_lowest} !important;
            border: 3px solid #0c0e13 !important;
            border-radius: var(--radius-xl) !important;
            box-shadow: 6px 6px 0px #0c0e13 !important;
            transition: all 150ms ease-out !important;
        }}
        .card-interactive:hover {{
            transform: translate(3px, 3px) !important;
            box-shadow: 3px 3px 0px #0c0e13 !important;
            border-color: #0c0e13 !important;
        }}
        
        /* Ticker ticker animations */
        @keyframes ticker-slide {{
            0% {{ transform: translate3d(0, 0, 0); }}
            100% {{ transform: translate3d(-50%, 0, 0); }}
        }}
        .ticker-wrap {{
            overflow: hidden;
            white-space: nowrap;
        }}
        .ticker-content {{
            display: inline-block;
            animation: ticker-slide 25s linear infinite;
        }}
        """

    # Построение модульной структуры контента под выбранную нишу
    content_blocks = ""
    
    if archetype == "saas":
        content_blocks = f"""
        <!-- SaaS Bento Grid -->
        <section id="features" class="py-24 border-y border-brand-outline-variant bg-brand-surface-low">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="text-center max-w-2xl mx-auto space-y-4">
                    <span class="text-xs font-bold text-brand-primary uppercase tracking-widest block">Технология Продуктивности</span>
                    <h2 class="text-3xl md:text-5xl font-extrabold text-brand-on-background tracking-tight font-display">Нерушимые Стандарты Разработки</h2>
                    <p class="text-brand-on-background/70 text-sm">Устранение рутинных ручных ошибок за счет использования строгой машиночитаемой спецификации.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="card-interactive p-8 space-y-6">
                        <div class="w-12 h-12 rounded-2xl bg-brand-primary/10 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["saas"]["feature_1"]}
                        </div>
                        <h3 class="text-xl font-bold text-brand-on-background font-display">Модульный слой</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Полное разделение семантических стилей и кодовой базы. Логические контейнеры и переменные выверены с математической точностью.
                        </p>
                    </div>
                    <div class="card-interactive p-8 space-y-6">
                        <div class="w-12 h-12 rounded-2xl bg-brand-primary/10 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["saas"]["feature_2"]}
                        </div>
                        <h3 class="text-xl font-bold text-brand-on-background font-display">Максимальная скорость</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Генерация готовых к выкладке веб-компонентов из текстовой декларации занимает менее минуты, минуя макеты в графических редакторах.
                        </p>
                    </div>
                    <div class="card-interactive p-8 space-y-6">
                        <div class="w-12 h-12 rounded-2xl bg-brand-primary/10 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["saas"]["feature_3"]}
                        </div>
                        <h3 class="text-xl font-bold text-brand-on-background font-display">Гарантия качества</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Каждый токен проходит проверку на коэффициент контрастности по стандарту WCAG AA, предупреждая проблемы с доступностью.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """
    elif archetype == "fintech":
        content_blocks = f"""
        <!-- FinTech Telemetry Dashboard -->
        <section id="features" class="py-24 border-y border-brand-outline-variant bg-brand-surface-low">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="flex flex-col md:flex-row md:items-end justify-between border-b border-brand-outline-variant pb-8 gap-4">
                    <div>
                        <span class="text-xs font-bold text-brand-primary uppercase tracking-widest block font-mono">[ REAL-TIME ANALYTICS ]</span>
                        <h2 class="text-3xl md:text-5xl font-extrabold text-brand-on-background tracking-tight font-display">Торговый Терминал Core</h2>
                    </div>
                    <p class="text-brand-on-background/60 text-xs font-mono max-w-sm">Сводный статус сетевой активности и транзакций криптоактивов.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="card-interactive p-6 space-y-6 bg-brand-surface-lowest">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-mono text-brand-on-background/50">SECURE_VAULT_v2</span>
                            {SVG_ICONS["fintech"]["feature_1"]}
                        </div>
                        <div class="space-y-1">
                            <span class="text-xs text-brand-on-background/60 block font-mono">Аппаратное шифрование</span>
                            <h3 class="text-2xl font-bold text-brand-on-background font-display tracking-tight">Мульти-подпись HS-256</h3>
                        </div>
                        <p class="text-brand-on-background/70 text-xs leading-relaxed font-mono">
                            Ключи транзакций изолированы на уровне микроядра, предотвращая утечку данных при компрометации веб-слоя.
                        </p>
                    </div>
                    
                    <div class="card-interactive p-6 space-y-6 bg-brand-surface-lowest">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-mono text-brand-on-background/50">INDEX_TREND_24H</span>
                            {SVG_ICONS["fintech"]["feature_2"]}
                        </div>
                        <div class="space-y-1">
                            <span class="text-xs text-brand-on-background/60 block font-mono">Индекс волатильности</span>
                            <h3 class="text-2xl font-bold text-brand-primary font-display tracking-tight">+ [metric] активных зон</h3>
                        </div>
                        <p class="text-brand-on-background/70 text-xs leading-relaxed font-mono">
                            Автоматический замер колебания цен и динамическая перебалансировка ликвидности пула в реальном времени.
                        </p>
                    </div>

                    <div class="card-interactive p-6 space-y-6 bg-brand-surface-lowest">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-mono text-brand-on-background/50">SWAP_ROUTING</span>
                            {SVG_ICONS["fintech"]["feature_3"]}
                        </div>
                        <div class="space-y-1">
                            <span class="text-xs text-brand-on-background/60 block font-mono">Оптимальный курс обмена</span>
                            <h3 class="text-2xl font-bold text-brand-on-background font-display tracking-tight">Aura Route Engine</h3>
                        </div>
                        <p class="text-brand-on-background/70 text-xs leading-relaxed font-mono">
                            Прямая интеграция с крупнейшими AMM протоколами гарантирует совершение сделок по лучшим ценам в сети.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """
    elif archetype == "glassmorphism":
        content_blocks = f"""
        <!-- Atmospheric Glass Bento -->
        <section id="features" class="py-24 border-y border-brand-outline-variant bg-transparent">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="text-center max-w-2xl mx-auto space-y-4">
                    <span class="text-xs font-bold text-brand-on-background/60 uppercase tracking-widest block">Физика света на экране</span>
                    <h2 class="text-3xl md:text-5xl font-extrabold text-brand-primary tracking-tight font-display">Матовое преломление граней</h2>
                    <p class="text-brand-on-background/70 text-sm">Стиль воссоздает эффект стеклянных линз, парящих в жидком пространстве благодаря размытию фона.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="glass-panel p-8 rounded-3xl space-y-6 transition-all duration-300 hover:scale-[1.02]">
                        <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-white">
                            {SVG_ICONS["glassmorphism"]["feature_1"]}
                        </div>
                        <h3 class="text-xl font-bold text-white font-display">Эффект линзы</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Backdrop-filter с силой размытия 20px позволяет фоновым градиентам аккуратно просвечивать, формируя премиальное ощущение глубины.
                        </p>
                    </div>

                    <div class="glass-panel p-8 rounded-3xl space-y-6 transition-all duration-300 hover:scale-[1.02]">
                        <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-white">
                            {SVG_ICONS["glassmorphism"]["feature_2"]}
                        </div>
                        <h3 class="text-xl font-bold text-white font-display">Световой Кант</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Каждый стеклянный блок очерчен тончайшим 1px белым контуром с прозрачностью 15%, имитирующим световой блик на ребре стекла.
                        </p>
                    </div>

                    <div class="glass-panel p-8 rounded-3xl space-y-6 transition-all duration-300 hover:scale-[1.02]">
                        <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-white">
                            {SVG_ICONS["glassmorphism"]["feature_3"]}
                        </div>
                        <h3 class="text-xl font-bold text-white font-display">Компенсация шума</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Для сохранения читаемости на размытом фоне шрифты принудительно утолщены, а для мелкого текста включена легкая тень букв.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """
    elif archetype == "pets":
        content_blocks = f"""
        <!-- Pets and Friendly Grid -->
        <section id="features" class="py-24 border-y border-brand-outline-variant bg-brand-surface-low">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="text-center max-w-2xl mx-auto space-y-4">
                    <span class="text-xs font-bold text-brand-primary uppercase tracking-widest block">Забота и Тепло</span>
                    <h2 class="text-3xl md:text-5xl font-extrabold text-brand-on-background tracking-tight font-display">Округлая Жизнерадостная Среда</h2>
                    <p class="text-brand-on-background/70 text-sm">Создаем атмосферу глубокого доверия с помощью «дышащих» цветных теней и обтекаемых форм.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="bg-brand-surface-lowest p-8 rounded-3xl shadow-ambient-warm border border-brand-outline-variant space-y-6 transition-all duration-300 hover:translate-y-[-4px]">
                        <div class="w-12 h-12 rounded-2xl bg-brand-primary/10 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["pets"]["feature_1"]}
                        </div>
                        <h3 class="text-xl font-bold text-brand-on-background font-display">Мягкие формы</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Увеличенные радиусы скруглений карточек (24px) полностью исключают резкость из интерфейса, делая его визуально безопасным.
                        </p>
                    </div>

                    <div class="bg-brand-surface-lowest p-8 rounded-3xl shadow-ambient-blue border border-brand-outline-variant space-y-6 transition-all duration-300 hover:translate-y-[-4px]">
                        <div class="w-12 h-12 rounded-2xl bg-brand-secondary/10 flex items-center justify-center text-brand-secondary">
                            {SVG_ICONS["pets"]["feature_2"]}
                        </div>
                        <h3 class="text-xl font-bold text-brand-on-background font-display">Цветные тени</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            В тени наших карточек аккуратно замешиваются оранжевые и синие тона бренда, создавая волшебный эффект светимости.
                        </p>
                    </div>

                    <div class="bg-brand-surface-lowest p-8 rounded-3xl shadow-ambient-warm border border-brand-outline-variant space-y-6 transition-all duration-300 hover:translate-y-[-4px]">
                        <div class="w-12 h-12 rounded-2xl bg-brand-primary/10 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["pets"]["feature_3"]}
                        </div>
                        <h3 class="text-xl font-bold text-brand-on-background font-display">Звездные отзывы</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Любимые питомцы заслуживают лучшего ухода. Все специалисты верифицированы и имеют наивысшие рейтинги удовлетворенности владельцев.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """
    elif archetype == "cosmic":
        content_blocks = f"""
        <!-- Cosmic Eclipse Elements -->
        <section id="features" class="py-24 border-y border-brand-outline-variant bg-transparent">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="text-center max-w-2xl mx-auto space-y-4">
                    <span class="text-xs font-bold text-brand-primary uppercase tracking-widest block font-mono">[ SOL_OBSERVATION ]</span>
                    <h2 class="text-3xl md:text-5xl font-extrabold text-brand-on-background tracking-tight font-display">Величие Затмения в Каждой Детали</h2>
                    <p class="text-brand-on-background/70 text-sm">Ультра-премиальный дизайн на основе парящих обсидиановых плит с глубоким янтарным свечением короны.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="obsidian-card p-8 rounded-3xl space-y-6">
                        <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["cosmic"]["feature_1"]}
                        </div>
                        <h3 class="text-xl font-bold text-white font-display">Орбитальная симметрия</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Строгое математическое выравнивание элементов напоминает траектории планет, обеспечивая непревзойденную гармонию композиции.
                        </p>
                    </div>

                    <div class="obsidian-card p-8 rounded-3xl space-y-6">
                        <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["cosmic"]["feature_2"]}
                        </div>
                        <h3 class="text-xl font-bold text-white font-display">Лунная тень</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Глубокие темные подложки поглощают свет, концентрируя внимание пользователя исключительно на ярких золотых акцентах короны.
                        </p>
                    </div>

                    <div class="obsidian-card p-8 rounded-3xl space-y-6">
                        <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-brand-primary">
                            {SVG_ICONS["cosmic"]["feature_3"]}
                        </div>
                        <h3 class="text-xl font-bold text-white font-display">Свечение короны</h3>
                        <p class="text-brand-on-background/70 text-sm leading-relaxed">
                            Вторичная подсветка карточек создает объемный эффект, словно свет вырывается из-за края плотной обсидиановой плиты.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """
    elif archetype == "alpinism":
        content_blocks = f"""
        <!-- Scientific Alpinism Instruments -->
        <section id="features" class="py-24 border-y border-brand-outline-variant bg-brand-surface-low alpine-grid">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="scientific-border p-8 border-brand-outline-variant bg-brand-surface-low max-w-4xl mx-auto space-y-12">
                    <div class="scientific-border-tl"></div><div class="scientific-border-tr"></div>
                    
                    <div class="text-center max-w-2xl mx-auto space-y-4">
                        <span class="text-xs font-medium text-brand-primary uppercase tracking-widest block font-mono">[ COORDINATES: 45° 50' N, 6° 51' E ]</span>
                        <h2 class="text-3xl md:text-4xl font-normal text-brand-on-background font-display tracking-wider">ПРИБОРНЫЙ НАБОР ЭКСПЕДИЦИИ</h2>
                        <div class="w-24 h-[1px] bg-brand-primary mx-auto my-3"></div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4 text-left">
                        <div class="border border-brand-outline-variant p-6 space-y-4">
                            <div class="flex items-center justify-between pb-2 border-b border-brand-outline-variant/30">
                                <span class="text-[10px] font-mono text-brand-on-background/50">INSTR_01 / ORIENT</span>
                                {SVG_ICONS["alpinism"]["feature_1"]}
                            </div>
                            <h3 class="text-lg font-normal text-brand-primary font-display">Роза Ветров</h3>
                            <p class="text-brand-on-background/70 text-xs leading-relaxed font-serif">
                                Использование классических географических ориентиров викторианской эпохи гарантирует точное наведение по сторонам света.
                            </p>
                        </div>

                        <div class="border border-brand-outline-variant p-6 space-y-4">
                            <div class="flex items-center justify-between pb-2 border-b border-brand-outline-variant/30">
                                <span class="text-[10px] font-mono text-brand-on-background/50">INSTR_02 / ALT</span>
                                {SVG_ICONS["alpinism"]["feature_2"]}
                            </div>
                            <h3 class="text-lg font-normal text-brand-primary font-display">Секстант Меридиана</h3>
                            <p class="text-brand-on-background/70 text-xs leading-relaxed font-serif">
                                Определение высоты светил над горизонтом с точностью до угловой секунды для точного позиционирования наблюдателя.
                            </p>
                        </div>

                        <div class="border border-brand-outline-variant p-6 space-y-4">
                            <div class="flex items-center justify-between pb-2 border-b border-brand-outline-variant/30">
                                <span class="text-[10px] font-mono text-brand-on-background/50">INSTR_03 / BARO</span>
                                {SVG_ICONS["alpinism"]["feature_3"]}
                            </div>
                            <h3 class="text-lg font-normal text-brand-primary font-display">Телеметрия Давлений</h3>
                            <p class="text-brand-on-background/70 text-xs leading-relaxed font-serif">
                                Мониторинг атмосферного столба ледника предупреждает о приближении грозового фронта за три часа до начала бури.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """
    elif archetype == "bumaga":
        content_blocks = f"""
        <!-- Блок "ДЕЛАЕМ ВСЕ, ЧТОБЫ ВАС..." (Тёмная плита с парящими стикерами) -->
        <section class="py-24 bg-[#0c0e13] border-b-4 border-black relative overflow-hidden" style="background-image: radial-gradient(rgba(255,255,255,0.05) 1.5px, transparent 1.5px); background-size: 16px 16px;">
            <div class="max-w-7xl mx-auto px-6 text-center space-y-12">
                <span class="text-xs font-black uppercase tracking-widest text-[#3bee33] font-display">[ BUREAU_CAPSULES ]</span>
                <h2 class="text-4xl md:text-6xl font-black text-white font-display tracking-tight leading-none uppercase">
                    ДЕЛАЕМ ВСЕ, ЧТОБЫ ВАС
                </h2>
                
                <div class="relative min-h-[300px] max-w-4xl mx-auto mt-8 select-none">
                    <!-- Blue Triangle SVG Floating -->
                    <div class="absolute top-2 left-10 text-[#0066ff] animate-pulse">
                        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24"><path d="M12 3l10 16H2L12 3z"/></svg>
                    </div>
                    <!-- Green Spiral Circle Floating -->
                    <div class="absolute bottom-4 left-16 text-[#3bee33] animate-spin" style="animation-duration: 10s">
                        <svg class="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="8"/><path d="M12 8a4 4 0 11-4 4"/></svg>
                    </div>
                    <!-- Retro Yellow Heart Floating -->
                    <div class="absolute bottom-6 right-20 text-[#ffee11] animate-bounce">
                        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                    </div>
                    <!-- Pink Star Floating -->
                    <div class="absolute top-10 right-12 text-[#ff33a0] animate-pulse">
                        <svg class="w-12 h-12" fill="currentColor" viewBox="0 0 24 24"><path d="M12 .587l3.668 7.431 8.2 1.192-5.934 5.787 1.4 8.168L12 18.896l-7.334 3.857 1.4-8.168L.132 9.21l8.2-1.192z"/></svg>
                    </div>

                    <!-- Overlapping capsule text cards (Desktop responsive flex grid) -->
                    <div class="flex flex-wrap justify-center gap-6 pt-12 relative z-10 max-w-3xl mx-auto">
                        <!-- ЛЮБИЛИ -->
                        <div class="px-8 py-4 bg-[#ff33a0] text-white text-xl md:text-3xl font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#000] rotate-[-3deg] hover:rotate-0 hover:translate-y-1 hover:shadow-[2px_2px_0px_#000] transition-all cursor-pointer font-display uppercase">
                            ЛЮБИЛИ
                        </div>
                        <!-- ЗАМЕЧАЛИ -->
                        <div class="px-8 py-4 bg-[#0066ff] text-white text-xl md:text-3xl font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#000] rotate-[4deg] hover:rotate-0 hover:translate-y-1 hover:shadow-[2px_2px_0px_#000] transition-all cursor-pointer font-display uppercase">
                            ЗАМЕЧАЛИ
                        </div>
                        <!-- ЗАХОТЕЛИ -->
                        <div class="px-8 py-4 bg-[#3bee33] text-black text-xl md:text-3xl font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#000] rotate-[-5deg] hover:rotate-0 hover:translate-y-1 hover:shadow-[2px_2px_0px_#000] transition-all cursor-pointer font-display uppercase">
                            ЗАХОТЕЛИ
                        </div>
                        <!-- ОБСУЖДАЛИ -->
                        <div class="px-8 py-4 bg-[#ff7700] text-white text-xl md:text-3xl font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#000] rotate-[3deg] hover:rotate-0 hover:translate-y-1 hover:shadow-[2px_2px_0px_#000] transition-all cursor-pointer font-display uppercase">
                            ОБСУЖДАЛИ
                        </div>
                        <!-- ВЫБИРАЛИ -->
                        <div class="px-8 py-4 bg-[#ffee11] text-black text-xl md:text-3xl font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#000] rotate-[-2deg] hover:rotate-0 hover:translate-y-1 hover:shadow-[2px_2px_0px_#000] transition-all cursor-pointer font-display uppercase">
                            ВЫБИРАЛИ
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Блок "ТОНКО ЧУВСТВУЕМ БРЕНДЫ" (Светлая бумажная основа) -->
        <section class="py-24 bg-[#f8fafc] border-b-4 border-black relative">
            <div class="max-w-7xl mx-auto px-6 text-center space-y-12">
                <span class="text-xs font-black text-brand-primary uppercase tracking-widest font-display block">[ BRAND_EMPATHY ]</span>
                <h2 class="text-4xl md:text-6xl font-black text-black font-display tracking-tight uppercase leading-none">
                    ТОНКО ЧУВСТВУЕМ БРЕНДЫ
                </h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8 pt-8 max-w-5xl mx-auto">
                    <div class="p-8 bg-brand-secondary text-black border-4 border-black rounded-[24px] shadow-[6px_6px_0px_#0c0e13] transform rotate-[-1.5deg] hover:rotate-0 transition-all animate-float" style="animation-duration: 4.5s">
                        <span class="block text-4xl md:text-5xl font-black font-display mb-2">20+</span>
                        <span class="text-sm font-bold uppercase tracking-wider font-mono">УСПЕШНЫХ ПРОЕКТОВ</span>
                    </div>
                    <div class="p-8 bg-brand-primary text-white border-4 border-black rounded-[24px] shadow-[6px_6px_0px_#0c0e13] transform rotate-[1deg] hover:rotate-0 transition-all animate-float" style="animation-duration: 5s">
                        <span class="block text-4xl md:text-5xl font-black font-display mb-2">15</span>
                        <span class="text-sm font-bold uppercase tracking-wider font-mono">ЧЕЛОВЕК В КОМАНДЕ</span>
                    </div>
                    <div class="p-8 bg-brand-container text-black border-4 border-black rounded-[24px] shadow-[6px_6px_0px_#0c0e13] transform rotate-[-1deg] hover:rotate-0 transition-all animate-float" style="animation-duration: 5.5s">
                        <span class="block text-4xl md:text-5xl font-black font-display mb-2">5 ЛЕТ</span>
                        <span class="text-sm font-bold uppercase tracking-wider font-mono">НА РЫНКЕ SMM</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Пересекающиеся диагональные сигнальные ленты-тикеры -->
        <div class="relative w-full h-44 bg-white border-y-4 border-black overflow-hidden z-20 flex items-center justify-center" style="background-image: radial-gradient(rgba(0,0,0,0.06) 1px, transparent 1px); background-size: 16px 16px;">
            <!-- Желтая сигнальная лента -->
            <div class="absolute w-[140%] h-14 bg-[#ffee11] border-y-4 border-black flex items-center ticker-wrap rotate-[-3deg] shadow-[0_8px_0px_rgba(0,0,0,1)] z-10">
                <div class="ticker-content text-base font-black text-black font-display tracking-wider uppercase py-2">
                    Скрепка • Золотой Кубок • WURTH • FIFA • АК БАРС • Караван • Скрепка • Золотой Кубок • WURTH • FIFA • АК БАРС • Караван • Скрепка • Золотой Кубок • WURTH • FIFA • АК БАРС • Караван
                </div>
            </div>
            <!-- Розовая сигнальная лента -->
            <div class="absolute w-[140%] h-14 bg-[#ff33a0] border-y-4 border-black flex items-center ticker-wrap rotate-[2deg] shadow-[0_8px_0px_rgba(0,0,0,1)] z-20">
                <div class="ticker-content text-base font-black text-white font-display tracking-wider uppercase py-2" style="animation-direction: reverse; animation-duration: 22s;">
                    BUMAGA DIGITAL • SMM AGENCY • PRODUCTION TEAM • BRAND STRATEGY • EVENT MAKERS • BUMAGA DIGITAL • SMM AGENCY • PRODUCTION TEAM • BRAND STRATEGY • EVENT MAKERS
                </div>
            </div>
        </div>

        <!-- Раздел КЕЙСЫ -->
        <section id="features" class="py-24 bg-white relative border-b-4 border-black">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="text-center space-y-4">
                    <span class="text-xs font-black text-brand-primary uppercase tracking-widest block font-display">[ CASES_GALLERY ]</span>
                    <h2 class="text-4xl md:text-5xl font-black text-black tracking-tight font-display uppercase leading-none">НАШИ КЕЙСЫ</h2>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                    <!-- Кейс 1 -->
                    <div class="card-interactive p-0 rounded-t-[32px] overflow-hidden flex flex-col justify-between" style="min-height: 380px;">
                        <div class="bg-[#3bee33] h-52 border-b-3 border-black relative flex items-center justify-center p-4">
                            <div class="absolute inset-3 border-3 border-dashed border-black/20 rounded-2xl"></div>
                            <img src="https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000e75071fd9fd1f9c4b7258abd.png" class="absolute w-28 h-28 object-contain z-10 animate-float" style="animation-duration: 5s">
                            <span class="absolute bottom-2 text-xs font-black text-black uppercase font-display bg-white px-3 py-1 border-2 border-black rounded-lg shadow-[2px_2px_0px_#000] rotate-[-2deg] z-20">Караван</span>
                        </div>
                        <div class="p-6 bg-white border-t border-black flex-grow flex items-center justify-center">
                            <h4 class="text-sm font-black text-black font-display tracking-tight text-center uppercase">Редизайн упаковки и мерча</h4>
                        </div>
                    </div>
                    
                    <!-- Кейс 2 -->
                    <div class="card-interactive p-0 rounded-t-[32px] overflow-hidden flex flex-col justify-between" style="min-height: 380px;">
                        <div class="bg-[#ff33a0] h-52 border-b-3 border-black relative flex items-center justify-center p-4">
                            <div class="absolute inset-3 border-3 border-dashed border-black/20 rounded-2xl"></div>
                            <img src="https://tempfile.aiquickdraw.com/images/chatgpt/file_0000000033471f7ae58711261f28d8d.png" class="absolute w-28 h-28 object-contain z-10 animate-float" style="animation-duration: 4s">
                            <span class="absolute bottom-2 text-xs font-black text-white uppercase font-display bg-black px-3 py-1 border-2 border-[#ffee11] rounded-lg shadow-[2px_2px_0px_#fff] rotate-[3deg] z-20">Игристые Вина</span>
                        </div>
                        <div class="p-6 bg-white border-t border-black flex-grow flex items-center justify-center">
                            <h4 class="text-sm font-black text-black font-display tracking-tight text-center uppercase">Креативный новогодний SMM</h4>
                        </div>
                    </div>

                    <!-- Кейс 3 -->
                    <div class="card-interactive p-0 rounded-t-[32px] overflow-hidden flex flex-col justify-between" style="min-height: 380px;">
                        <div class="bg-[#ffee11] h-52 border-b-3 border-black relative flex items-center justify-center p-4">
                            <div class="absolute inset-3 border-3 border-dashed border-black/20 rounded-2xl"></div>
                            <img src="https://tempfile.aiquickdraw.com/images/chatgpt/file_000000009c4871fd89659ba12323bdd7.png" class="absolute w-28 h-28 object-contain z-10 animate-float" style="animation-duration: 6s">
                            <span class="absolute bottom-2 text-xs font-black text-black uppercase font-display bg-white px-3 py-1 border-2 border-black rounded-lg shadow-[2px_2px_0px_#000] rotate-[-1deg] z-20">Тысяча Озёр</span>
                        </div>
                        <div class="p-6 bg-white border-t border-black flex-grow flex items-center justify-center">
                            <h4 class="text-sm font-black text-black font-display tracking-tight text-center uppercase">Фермерский брендинг и SMM</h4>
                        </div>
                    </div>

                    <!-- Кейс 4 -->
                    <div class="card-interactive p-0 rounded-t-[32px] overflow-hidden flex flex-col justify-between" style="min-height: 380px;">
                        <div class="bg-[#0066ff] h-52 border-b-3 border-black relative flex items-center justify-center p-4">
                            <div class="absolute inset-3 border-3 border-dashed border-black/20 rounded-2xl"></div>
                            <img src="https://tempfile.aiquickdraw.com/images/chatgpt/file_00000000d2e071fd928759dd666866cf.png" class="absolute w-28 h-28 object-contain z-10 animate-float" style="animation-duration: 5s">
                            <span class="absolute bottom-2 text-xs font-black text-white uppercase font-display bg-black px-3 py-1 border-2 border-[#3bee33] rounded-lg shadow-[2px_2px_0px_#fff] rotate-[2deg] z-20">Серпак</span>
                        </div>
                        <div class="p-6 bg-white border-t border-black flex-grow flex items-center justify-center">
                            <h4 class="text-sm font-black text-black font-display tracking-tight text-center uppercase">Рекламная кампания и спецпроект</h4>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Блок КЛАССНЫЙ SMM С ЧИСТОГО ЛИСТА -->
        <section class="py-24 bg-[#0c0e13] border-b-4 border-black text-white" style="background-image: radial-gradient(rgba(255,255,255,0.03) 1.5px, transparent 1.5px); background-size: 16px 16px;">
            <div class="max-w-7xl mx-auto px-6 text-center space-y-8">
                <span class="text-xs font-black bg-brand-primary/10 text-brand-primary px-3 py-1 border-2 border-brand-primary rounded-full uppercase tracking-widest inline-block font-display">
                    [ НАШИ УСЛУГИ ]
                </span>
                <h2 class="text-3xl md:text-5xl font-black text-white tracking-tight font-display uppercase leading-none">
                    КЛАССНЫЙ SMM С ЧИСТОГО ЛИСТА
                </h2>
                
                <div class="flex flex-wrap justify-center gap-4 pt-6 max-w-4xl mx-auto select-none">
                    <span class="px-5 py-3 bg-[#1c1e23] text-white text-xs md:text-sm font-black border-2 border-black rounded-lg shadow-[3px_3px_0px_#000] uppercase font-display flex items-center"><span class="mr-2 text-brand-secondary">✦</span>SMM СТРАТЕГИЯ</span>
                    <span class="px-5 py-3 bg-[#1c1e23] text-white text-xs md:text-sm font-black border-2 border-black rounded-lg shadow-[3px_3px_0px_#000] uppercase font-display flex items-center"><span class="mr-2 text-brand-primary">✦</span>ВИДЕО PRODUCTION</span>
                    <span class="px-5 py-3 bg-[#1c1e23] text-white text-xs md:text-sm font-black border-2 border-black rounded-lg shadow-[3px_3px_0px_#000] uppercase font-display flex items-center"><span class="mr-2 text-brand-container">✦</span>PR & КРЕАТИВ</span>
                    <span class="px-5 py-3 bg-[#1c1e23] text-white text-xs md:text-sm font-black border-2 border-black rounded-lg shadow-[3px_3px_0px_#000] uppercase font-display flex items-center"><span class="mr-2 text-brand-high">✦</span>ТАРГЕТ & РЕКЛАМА</span>
                    <span class="px-5 py-3 bg-[#1c1e23] text-white text-xs md:text-sm font-black border-2 border-black rounded-lg shadow-[3px_3px_0px_#000] uppercase font-display flex items-center"><span class="mr-2 text-brand-secondary">✦</span>EVENTS</span>
                    <span class="px-5 py-3 bg-[#1c1e23] text-white text-xs md:text-sm font-black border-2 border-black rounded-lg shadow-[3px_3px_0px_#000] uppercase font-display flex items-center"><span class="mr-2 text-brand-primary">✦</span>КРЕАТИВНЫЕ СПЕЦПРОЕКТЫ</span>
                </div>
            </div>
        </section>

        <!-- Блок НАША КОМАНДА -->
        <section id="about" class="py-24 bg-white relative border-b-4 border-black">
            <div class="max-w-7xl mx-auto px-6 space-y-12">
                <div class="text-center space-y-4">
                    <span class="text-xs font-black text-brand-primary uppercase tracking-widest block font-display">[ OUR_TEAM ]</span>
                    <h2 class="text-4xl md:text-5xl font-black text-black tracking-tight font-display uppercase leading-none">НАША КОМАНДА</h2>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                    <!-- Участник 1 -->
                    <div class="border-4 border-black p-4 bg-[#f8fafc] rounded-3xl shadow-[6px_6px_0px_#0c0e13] flex flex-col space-y-4">
                        <div class="w-full aspect-square bg-[#0c0e13] border-3 border-black rounded-2xl overflow-hidden relative flex items-center justify-center">
                            <div class="absolute inset-0 bg-[#ffee11] flex items-center justify-center text-black font-black text-3xl font-display rotate-[-3deg] border-2 border-black">SASHA</div>
                        </div>
                        <div class="text-center space-y-1">
                            <h4 class="text-lg font-black text-black uppercase font-display">Саша</h4>
                            <span class="text-xs font-bold text-[#ff33a0] uppercase block font-mono">CEO / FOUNDER</span>
                        </div>
                    </div>
                    
                    <!-- Участник 2 -->
                    <div class="border-4 border-black p-4 bg-[#f8fafc] rounded-3xl shadow-[6px_6px_0px_#0c0e13] flex flex-col space-y-4">
                        <div class="w-full aspect-square bg-[#0c0e13] border-3 border-black rounded-2xl overflow-hidden relative flex items-center justify-center">
                            <div class="absolute inset-0 bg-[#ff33a0] flex items-center justify-center text-white font-black text-3xl font-display rotate-[2deg] border-2 border-black">NATASHA</div>
                        </div>
                        <div class="text-center space-y-1">
                            <h4 class="text-lg font-black text-black uppercase font-display">Наташа</h4>
                            <span class="text-xs font-bold text-[#ff33a0] uppercase block font-mono">ART DIRECTOR</span>
                        </div>
                    </div>

                    <!-- Участник 3 -->
                    <div class="border-4 border-black p-4 bg-[#f8fafc] rounded-3xl shadow-[6px_6px_0px_#0c0e13] flex flex-col space-y-4">
                        <div class="w-full aspect-square bg-[#0c0e13] border-3 border-black rounded-2xl overflow-hidden relative flex items-center justify-center">
                            <div class="absolute inset-0 bg-[#3bee33] flex items-center justify-center text-black font-black text-3xl font-display rotate-[-1deg] border-2 border-black">IRA</div>
                        </div>
                        <div class="text-center space-y-1">
                            <h4 class="text-lg font-black text-black uppercase font-display">Ира</h4>
                            <span class="text-xs font-bold text-[#ff33a0] uppercase block font-mono">SMM LEAD</span>
                        </div>
                    </div>

                    <!-- Участник 4 -->
                    <div class="border-4 border-black p-4 bg-[#f8fafc] rounded-3xl shadow-[6px_6px_0px_#0c0e13] flex flex-col space-y-4">
                        <div class="w-full aspect-square bg-[#0c0e13] border-3 border-black rounded-2xl overflow-hidden relative flex items-center justify-center">
                            <div class="absolute inset-0 bg-[#0066ff] flex items-center justify-center text-white font-black text-3xl font-display rotate-[3deg] border-2 border-black">DANILA</div>
                        </div>
                        <div class="text-center space-y-1">
                            <h4 class="text-lg font-black text-black uppercase font-display">Данила</h4>
                            <span class="text-xs font-bold text-[#ff33a0] uppercase block font-mono">VIDEO PRODUCER</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """

    # Динамические тексты шапки и Hero в зависимости от архетипа
    if archetype == "bumaga":
        nav_links = """
                <a href="#features" class="hover:text-brand-primary transition-all">Кейсы</a>
                <a href="#about" class="hover:text-brand-primary transition-all">Команда</a>
                <a href="#demo" class="hover:text-brand-primary transition-all font-bold">Бриф</a>
        """
        sys_name = "DIGITAL БЮРО BUMAGA"
        sys_desc = "Делаем все, чтобы ваши цифровые бренды любили, замечали и выбирали. Креативный SMM, яркий видео-продакшн, спецпроекты и долгосрочные бренд-стратегии с бумажной душой."
        header_cta = "Обсудить бриф"
        hero_badge = "[ DIGITAL BUREAU BUMAGA ]"
        hero_title = "Креативное бюро с бумажной душой"
        hero_btn_1 = "Начать проект"
        hero_btn_2 = "Смотреть кейсы"
        
        demo_title = "ОБСУДИТЬ ПРОЕКТ С БЮРО"
        demo_desc = "Заполните краткий бриф, и мы вернемся к вам с готовой концепцией."
        form_title = "Бриф на проект"
        form_btn = "Отправить бриф в BUMAGA"
        verif_title = "Тактильный отклик интерфейса"
        verif_desc = "Попробуйте нажать на кнопки и навести курсор на карточки ниже, чтобы прочувствовать плоские тени и пружинистую физику нео-брутализма."
    else:
        nav_links = """
                <a href="#features" class="hover:text-brand-primary transition-all">Спецификация</a>
                <a href="#about" class="hover:text-brand-primary transition-all">Приборы</a>
                <a href="#demo" class="hover:text-brand-primary transition-all">Дашборд</a>
                <a href="#faq" class="hover:text-brand-primary transition-all">Телеметрия</a>
        """
        header_cta = "Запуск системы"
        hero_badge = "[ AuraDesign Engine v2.0 ] font-mono"
        hero_title = "Машинный разум в границах эстетики"
        hero_btn_1 = "Начать сопряжение"
        hero_btn_2 = "Изучить приборы"
        
        demo_title = "Экспериментальный стенд ИИ"
        demo_desc = "Интерактивный пульсар для верификации и подгонки токенов."
        form_title = "Параметрический запрос"
        form_btn = "Запустить компиляцию контракта"
        verif_title = "Верификатор состояний в реальном времени"
        verif_desc = "Каждый интерактивный компонент ниже наследует переменные спецификации `AURADESIGN.md`. Проверьте визуальный отклик."

    # Шаблон HTML с Tailwind Config и CSS переменными
    if archetype == "bumaga":
        html_template = f"""<!DOCTYPE html>
<html lang="ru" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIGITAL БЮРО BUMAGA — Интеллектуальный веб-интерфейс</title>
    
    <!-- Подключаем необходимые шрифты -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    {custom_fonts_link}
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        display: ['"Unbounded"', 'sans-serif'],
                        mono: ['"IBM Plex Mono"', 'monospace'],
                        serif: ['"Georgia"', 'serif']
                    }},
                    colors: {{
                        brand: {{
                            primary: '{c_primary}',
                            'primary-hover': '{c_primary_hover}',
                            'on-primary': '{c_on_primary}',
                            secondary: '{c_secondary}',
                            'on-secondary': '{c_on_secondary}',
                            tertiary: '{c_tertiary}',
                            'on-tertiary': '{c_on_tertiary}',
                            background: '{c_background}',
                            'on-background': '{c_on_background}',
                            'surface-lowest': '{c_surface_lowest}',
                            'surface-low': '{c_surface_low}',
                            'surface-container': '{c_surface_container}',
                            'surface-high': '{c_surface_high}',
                            outline: '{c_outline}',
                            'outline-variant': '{c_outline_variant}',
                            container: '{c_surface_container}',
                            high: '{c_surface_high}',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        /* CSS Переменные AuraDesign */
        :root {{
            --radius-sm: {r_sm};
            --radius-default: {r_default};
            --radius-md: {r_md};
            --radius-lg: {r_lg};
            --radius-xl: {r_xl};
            
            --brand-primary: {c_primary};
            --brand-primary-hover: {c_primary_hover};
            --brand-on-primary: {c_on_primary};
            --brand-tertiary: {c_tertiary};
            --brand-on-tertiary: {c_on_tertiary};
            --brand-background: {c_background};
            --brand-on-background: {c_on_background};
        }}

        /* Custom scrollbar none */
        .scrollbar-none::-webkit-scrollbar {{
            display: none;
        }}
        .scrollbar-none {{
            -ms-overflow-style: none;
            scrollbar-width: none;
        }}

        {extra_styles}
    </style>
</head>
<body class="min-h-screen bg-[#f8fafc] font-sans overflow-x-hidden relative" style="background-image: radial-gradient(rgba(0,0,0,0.06) 1.5px, transparent 1.5px); background-size: 24px 24px;">

    <!-- Top Navigation Bar -->
    <header class="sticky top-0 bg-white/95 backdrop-blur-md border-b-4 border-black z-40">
        <div class="max-w-7xl mx-auto px-6 h-24 flex items-center justify-between">
            <!-- Logo -->
            <a href="#" class="flex items-center space-x-3">
                <div class="w-12 h-12 rounded-xl bg-brand-primary border-3 border-black flex items-center justify-center text-white shadow-[3px_3px_0px_#000]">
                    {SVG_ICONS["bumaga"]["logo"]}
                </div>
                <span class="text-lg font-black text-black tracking-tight font-display">BUMAGA</span>
            </a>
            <!-- Links -->
            <nav class="hidden md:flex items-center space-x-10 text-sm font-black font-display uppercase tracking-tight text-black">
                <a href="#features" class="hover:text-brand-primary transition-all">Кейсы</a>
                <a href="#about" class="hover:text-brand-primary transition-all">Команда</a>
                <a href="#contacts" class="hover:text-brand-primary transition-all font-bold">Контакты</a>
                <a href="#demo" class="hover:text-brand-primary transition-all font-bold">Бриф</a>
            </nav>
            <!-- CTA -->
            <a href="#demo" class="btn-primary px-6 py-3 text-xs font-black rounded-xl uppercase font-display inline-block">
                Обсудить бриф
            </a>
        </div>
    </header>

    <!-- Vertical Page Content -->
    <main class="w-full">
        <!-- Hero Section -->
        <section class="relative min-h-[85vh] bg-[#f8fafc] border-b-4 border-black overflow-hidden flex items-center py-20 lg:py-32" style="background-image: linear-gradient(#e2e8f0 1.5px, transparent 1.5px), linear-gradient(90deg, #e2e8f0 1.5px, transparent 1.5px); background-size: 36px 32px;">
            <!-- Floating Decorative Paper Scrap Stickers -->
            <div class="absolute top-10 left-8 bg-[#3bee33] text-black font-display font-black text-xs px-3 py-1.5 rounded border-2 border-black shadow-[3px_3px_0px_#000] rotate-[-8deg] hidden md:block animate-bounce select-none z-10" style="animation-duration: 4s;">
                [ BUMAGA.DIGITAL ]
            </div>
            <div class="absolute bottom-16 left-12 bg-[#ffee11] text-black font-display font-black text-xs px-3 py-1.5 rounded border-2 border-black shadow-[3px_3px_0px_#000] rotate-[12deg] hidden md:block select-none z-10">
                [ EMOTIONAL SMM ]
            </div>
            <div class="absolute top-20 right-16 bg-[#ff7700] text-white font-display font-black text-xs px-3 py-1.5 rounded border-2 border-black shadow-[3px_3px_0px_#000] rotate-[6deg] hidden md:block animate-bounce select-none z-10" style="animation-duration: 6s;">
                [ 15+ CREATIVES ]
            </div>

            <!-- Main Layout Container -->
            <div class="max-w-7xl mx-auto px-6 w-full grid grid-cols-1 lg:grid-cols-12 gap-16 items-center relative z-20">
                <!-- Text Column -->
                <div class="lg:col-span-7 space-y-8 text-left">
                    <div class="inline-block px-4 py-2 bg-[#ff33a0]/10 border-3 border-[#ff33a0] text-[#ff33a0] text-xs font-black rounded-lg uppercase tracking-wider font-display rotate-[-1.5deg] shadow-[3px_3px_0px_#000]">
                        ✦ {hero_badge} ✦
                    </div>
                    
                    <h1 class="text-5xl md:text-8xl font-black text-black font-display uppercase tracking-tight leading-[0.95] relative">
                        <span class="block relative z-10">КРЕАТИВНОЕ</span>
                        <span class="block text-[#ff33a0] font-extrabold translate-x-1.5 rotate-[-1.5deg] relative z-20">БЮРО</span>
                        <span class="block text-black relative z-30">BUMAGA</span>
                    </h1>
                    
                    <p class="text-black text-lg md:text-xl font-sans font-black leading-relaxed max-w-2xl bg-white p-5 rounded-2xl border-3 border-black shadow-[6px_6px_0px_#0c0e13]">
                        {sys_desc}
                    </p>
                    
                    <div class="flex flex-wrap gap-6 pt-4">
                        <a href="#demo" class="btn-primary px-10 py-5 text-base font-black shadow-sm font-display uppercase inline-block transform hover:translate-x-[3px] hover:translate-y-[3px] hover:shadow-[0px_0px_0px_#0c0e13]">
                            {hero_btn_1}
                        </a>
                        <a href="#features" class="px-10 py-5 bg-[#3bee33] text-black text-base font-black rounded-[var(--radius-md)] border-3 border-black shadow-[6px_6px_0px_#0c0e13] hover:translate-x-[3px] hover:translate-y-[3px] hover:shadow-[0px_0px_0px_#0c0e13] transition-all font-display uppercase inline-block">
                            {hero_btn_2}
                        </a>
                    </div>
                </div>

                <!-- Image Column -->
                <div class="lg:col-span-5 flex justify-center relative">
                    <!-- Layered Card Collage -->
                    <div class="relative w-full max-w-[420px] aspect-square rounded-[32px] border-4 border-black bg-white shadow-[16px_16px_0px_#0c0e13] p-6 relative group overflow-hidden flex items-center justify-center transform rotate-[1deg] hover:rotate-0 transition-all">
                        <div class="absolute inset-0 bg-gradient-to-tr from-[#ff33a0]/10 to-[#3bee33]/10 pointer-events-none"></div>
                        <img src="{hero_image_url}" class="w-[90%] h-[90%] object-contain animate-float" alt="AuraDesign Central Asset">
                        
                        <!-- Floating paper scrap over image -->
                        <div class="absolute bottom-4 left-4 bg-white text-black text-[10px] font-mono font-bold border-2 border-black px-2 py-1 rounded shadow-[2px_2px_0px_#000] rotate-[-3deg]">
                            FILE_ID: BUMAGA_3D_ASSET
                        </div>
                    </div>
                </div>
            </div>
        </section>

        {content_blocks}

        <!-- Блок КОНТАКТЫ (CONTACT CLUSTER) -->
        <section id="contacts" class="py-24 bg-[#ffee11]/15 border-b-4 border-black relative overflow-hidden">
            <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-16 items-center">
                <div class="lg:col-span-6 space-y-6">
                    <span class="text-xs font-black text-[#ff33a0] uppercase tracking-widest block font-display">[ CONTACT_CLUSTER ]</span>
                    <h2 class="text-4xl md:text-5xl font-black text-black font-display uppercase leading-none tracking-tight">ОТВЕТИМ НА ВСЕ ВАШИ ВОПРОСЫ</h2>
                    <p class="text-black/70 text-base md:text-lg font-sans font-medium">
                        Мы всегда на связи в мессенджерах и соцсетях. Кликните на любую капсулу, чтобы начать диалог и получить сочную идею для вашего бренда!
                    </p>
                </div>
                <div class="lg:col-span-6 flex justify-center">
                    <div class="flex flex-col gap-6 w-full max-w-[380px] relative select-none">
                        <!-- Capsule 1 (VK) -->
                        <a href="https://vk.com" target="_blank" class="h-16 bg-[#0066ff] text-white flex items-center justify-center font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#0c0e13] transform rotate-[-3deg] hover:rotate-0 hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[4px_4px_0px_#0c0e13] transition-all cursor-pointer font-display uppercase text-lg">
                            ВКонтакте
                        </a>
                        <!-- Capsule 2 (Instagram) -->
                        <a href="https://instagram.com" target="_blank" class="h-16 bg-[#ff33a0] text-white flex items-center justify-center font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#0c0e13] transform rotate-[2deg] hover:rotate-0 hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[4px_4px_0px_#0c0e13] transition-all cursor-pointer font-display uppercase text-lg">
                            Instagram
                        </a>
                        <!-- Capsule 3 (Telegram) -->
                        <a href="https://t.me" target="_blank" class="h-16 bg-[#3bee33] text-black flex items-center justify-center font-black rounded-full border-4 border-black shadow-[6px_6px_0px_#0c0e13] transform rotate-[-1.5deg] hover:rotate-0 hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[4px_4px_0px_#0c0e13] transition-all cursor-pointer font-display uppercase text-lg">
                            Telegram
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- Зигзаг разделитель -->
        <div class="w-full bg-white h-4 flex overflow-hidden">
            <svg class="w-full h-full text-[#0c0e13] fill-current" viewBox="0 0 100 10" preserveAspectRatio="none">
                <polygon points="0,0 2.5,10 5,0 7.5,10 10,0 12.5,10 15,0 17.5,10 20,0 22.5,10 25,0 27.5,10 30,0 32.5,10 35,0 37.5,10 40,0 42.5,10 45,0 47.5,10 50,0 52.5,10 55,0 57.5,10 60,0 62.5,10 65,0 67.5,10 70,0 72.5,10 75,0 77.5,10 80,0 82.5,10 85,0 87.5,10 90,0 92.5,10 95,0 97.5,10 100,0 100,10 0,10"/>
            </svg>
        </div>

        <!-- СЕКЦИЯ С ФОРМОЙ И КАРТОЧКАМИ ДЕМОНСТРАЦИИ -->
        <section id="demo" class="py-24 bg-[#0c0e13] text-white relative overflow-hidden" style="background-image: radial-gradient(rgba(255,255,255,0.03) 1.5px, transparent 1.5px); background-size: 16px 16px;">
            <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-16 items-start">
                <div class="lg:col-span-5 space-y-6">
                    <span class="text-xs font-black text-brand-secondary uppercase tracking-widest block font-display">[ TESTBENCH_CONTROL ]</span>
                    <h2 class="text-4xl md:text-5xl font-black text-white font-display uppercase leading-none tracking-tight">{demo_title}</h2>
                    <p class="text-white/60 text-base font-sans font-medium">{demo_desc}</p>
                    
                    <!-- Интерактивный интерактор состояний -->
                    <div class="card-interactive p-8 space-y-6 relative overflow-hidden bg-white border-4 border-black shadow-[8px_8px_0px_var(--brand-primary)] text-black">
                        <h3 class="text-lg font-black text-black font-display uppercase tracking-tight">{verif_title}</h3>
                        <p class="text-black/70 text-sm font-sans font-medium">{verif_desc}</p>
                        
                        <div class="grid grid-cols-1 gap-6 pt-2">
                            <div class="p-6 bg-brand-surface-low border-3 border-black rounded-2xl space-y-4 relative">
                                <span class="text-xs text-black/50 font-bold uppercase tracking-widest block font-mono">BUTTON_STATES</span>
                                <div class="flex flex-wrap gap-3">
                                    <button class="px-6 py-3 bg-brand-primary text-white text-xs font-black rounded-xl border-3 border-black shadow-[4px_4px_0px_#000] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[3px_3px_0px_#000] transition-all uppercase font-display">Активна</button>
                                    <button class="px-6 py-3 bg-brand-primary text-white text-xs font-black rounded-xl border-3 border-black opacity-30 cursor-not-allowed uppercase font-display" disabled>Блокирована</button>
                                </div>
                            </div>
                            <div class="p-6 bg-brand-surface-low border-3 border-black rounded-2xl space-y-4 relative">
                                <span class="text-xs text-black/50 font-bold uppercase tracking-widest block font-mono">AURA_INDICATORS</span>
                                <div class="flex flex-wrap gap-3">
                                    <span class="px-4 py-2 bg-brand-secondary text-black text-xs font-black rounded-full border-3 border-black uppercase font-display">STATE_ACTIVE</span>
                                    <span class="px-4 py-2 bg-brand-primary text-white text-xs font-black rounded-full border-3 border-black uppercase font-display">STATE_PENDING</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Форма -->
                <div class="lg:col-span-7 w-full">
                    <div class="card-interactive p-8 md:p-12 space-y-6 relative bg-white border-4 border-black shadow-[10px_10px_0px_#fff] text-black">
                        <h3 class="text-2xl font-black text-black font-display uppercase tracking-tight">{form_title}</h3>
                        
                        <form onsubmit="alert('Запрос получен! BUMAGA уже готовит сочную концепцию.'); return false;" class="space-y-6">
                            <div class="space-y-2">
                                <label class="block text-xs font-black text-black font-mono">BRAND_NAME:</label>
                                <input type="text" placeholder="Bumaga Client" required class="w-full px-4 py-3 bg-brand-surface-lowest border-3 border-black rounded-xl text-sm focus:outline-none focus:border-brand-primary text-black font-medium">
                            </div>
                            <div class="space-y-2">
                                <label class="block text-xs font-black text-black font-mono">VISUAL_ARCHETYPE:</label>
                                <select class="w-full px-4 py-3 bg-brand-surface-lowest border-3 border-black rounded-xl text-sm focus:outline-none focus:border-brand-primary text-black font-medium">
                                    <option>SaaS Premium (Light Minimalist)</option>
                                    <option>FinTech Slate (Dark Monospace)</option>
                                    <option>Atmospheric Glass (Glassmorphism)</option>
                                    <option>Friendly Organic (Paws & Paths)</option>
                                    <option>Cosmic Totality (Solar Eclipse)</option>
                                    <option>Scientific Alpinism (Victorian Navy)</option>
                                    <option selected>BUMAGA Creative (Neo-Brutalist)</option>
                                </select>
                            </div>
                            <div class="space-y-2">
                                <label class="block text-xs font-black text-black font-mono">EMAIL_ADDRESS:</label>
                                <input type="email" placeholder="client@bumaga-bureau.ru" required class="w-full px-4 py-3 bg-brand-surface-lowest border-3 border-black rounded-xl text-sm focus:outline-none focus:border-brand-primary text-black font-medium">
                            </div>
                            
                            <button type="submit" class="w-full py-4 btn-primary text-sm font-black font-display shadow-sm uppercase">
                                {form_btn}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </section>

        <!-- Зигзаг разделитель -->
        <div class="w-full bg-[#0c0e13] h-4 flex overflow-hidden">
            <svg class="w-full h-full text-white fill-current" viewBox="0 0 100 10" preserveAspectRatio="none">
                <polygon points="0,0 2.5,10 5,0 7.5,10 10,0 12.5,10 15,0 17.5,10 20,0 22.5,10 25,0 27.5,10 30,0 32.5,10 35,0 37.5,10 40,0 42.5,10 45,0 47.5,10 50,0 52.5,10 55,0 57.5,10 60,0 62.5,10 65,0 67.5,10 70,0 72.5,10 75,0 77.5,10 80,0 82.5,10 85,0 87.5,10 90,0 92.5,10 95,0 97.5,10 100,0 100,10 0,10"/>
            </svg>
        </div>
    </main>

    <!-- ПОДВАЛ (FOOTER) -->
    <footer class="bg-[#0c0e13] text-white border-t-4 border-black py-16">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-12">
            <div class="space-y-4">
                <span class="text-3xl font-black text-brand-primary tracking-tight font-display">{sys_name}</span>
                <p class="text-sm text-white/60 leading-relaxed font-sans font-medium max-w-md">
                    Интеллектуальная дизайн-система на основе независимого контракта Aura. Никакого визуального мусора, клише и эмодзи.
                </p>
            </div>
            <div class="flex flex-col md:items-end justify-between gap-6">
                <div class="flex space-x-6 text-sm font-bold font-mono">
                    <a href="#features" class="hover:text-brand-primary transition-all uppercase">Кейсы</a>
                    <a href="#about" class="hover:text-brand-primary transition-all uppercase">Команда</a>
                    <a href="#demo" class="hover:text-brand-primary transition-all uppercase">Бриф</a>
                </div>
                <div class="border-t border-white/10 pt-4 w-full md:w-auto flex flex-col md:items-end text-xs text-white/40 font-mono gap-1">
                    <span>© 2026 {sys_name} • Все права защищены.</span>
                    <span class="uppercase tracking-widest font-semibold text-[10px]">Сверстано AuraDesign Agent</span>
                </div>
            </div>
        </div>
    </footer>

</body>
</html>"""
        return html_template

    # Шаблон HTML с Tailwind Config и CSS переменными
    html_template = f"""<!DOCTYPE html>
<html lang="ru" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sys_name} — Интеллектуальный веб-интерфейс</title>
    
    <!-- Подключаем необходимые шрифты -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    {custom_fonts_link}
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"{"Inter" if archetype in ["pets", "glassmorphism"] else "Geist"}"', 'sans-serif'],
                        display: ['"{font_main}"', 'sans-serif'],
                        mono: ['"{"IBM Plex Mono" if archetype == "alpinism" else "Geist Mono"}"', 'monospace'],
                        serif: ['"{"Newsreader" if archetype == "alpinism" else "Georgia"}"', 'serif']
                    }},
                    colors: {{
                        brand: {{
                            primary: '{c_primary}',
                            'primary-hover': '{c_primary_hover}',
                            'on-primary': '{c_on_primary}',
                            secondary: '{c_secondary}',
                            'on-secondary': '{c_on_secondary}',
                            tertiary: '{c_tertiary}',
                            'on-tertiary': '{c_on_tertiary}',
                            background: '{c_background}',
                            'on-background': '{c_on_background}',
                            'surface-lowest': '{c_surface_lowest}',
                            'surface-low': '{c_surface_low}',
                            'surface-container': '{c_surface_container}',
                            'surface-high': '{c_surface_high}',
                            outline: '{c_outline}',
                            'outline-variant': '{c_outline_variant}',
                            container: '{c_surface_container}',
                            high: '{c_surface_high}',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        /* CSS Переменные AuraDesign */
        :root {{
            --radius-sm: {r_sm};
            --radius-default: {r_default};
            --radius-md: {r_md};
            --radius-lg: {r_lg};
            --radius-xl: {r_xl};
            
            --brand-primary: {c_primary};
            --brand-primary-hover: {c_primary_hover};
            --brand-on-primary: {c_on_primary};
            --brand-tertiary: {c_tertiary};
            --brand-on-tertiary: {c_on_tertiary};
            --brand-background: {c_background};
            --brand-on-background: {c_on_background};
        }}

        body {{
            background-color: var(--brand-background);
            color: var(--brand-on-background);
            { "background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px); background-size: 32px 32px;" if archetype == "fintech" else "" }
        }}

        /* Кастомный стиль кнопок AuraDesign */
        .btn-primary {{
            background-color: var(--brand-primary);
            color: var(--brand-on-primary);
            border-radius: var(--radius-md);
            border: 1px solid var(--brand-primary);
            transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .btn-primary:hover {{
            background-color: var(--brand-primary-hover);
            transform: translateY(-1px);
        }}
        
        .card-interactive {{
            background-color: {c_surface_lowest if archetype != "glassmorphism" else "rgba(255,255,255,0.03)"};
            border: 1px solid {c_outline_variant};
            border-radius: var(--radius-xl);
            transition: all 250ms cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .card-interactive:hover {{
            transform: translateY(-3px);
            border-color: {c_outline};
            box-shadow: 0 20px 40px -10px rgba({get_rgb_channels(c_primary)}, 0.05);
        }}

        /* Анимация левитации ассета */
        @keyframes float-asset {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        .animate-float {{
            animation: float-asset 6s infinite ease-in-out;
        }}

        {extra_styles}
    </style>
</head>
<body class="min-h-screen font-sans antialiased flex flex-col justify-between overflow-x-hidden">

    <!-- ШАПКА САЙТА -->
    <header class="sticky top-0 bg-brand-background/80 backdrop-blur-md border-b-4 border-black z-40">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="#" class="flex items-center space-x-3 group">
                <div class="w-10 h-10 rounded-[var(--radius-default)] bg-brand-primary border-3 border-black flex items-center justify-center text-brand-on-primary shadow-[2px_2px_0px_#000] group-hover:scale-105 transition-all">
                    {SVG_ICONS[archetype if archetype in SVG_ICONS else "saas"]["logo"]}
                </div>
                <span class="text-xl font-extrabold text-brand-on-background tracking-tight font-display">{sys_name}</span>
            </a>
            
            <nav class="hidden md:flex items-center space-x-8 text-sm font-semibold text-brand-on-background/80 font-display">
                {nav_links}
            </nav>

            <div>
                <a href="#demo" class="btn-primary px-5 py-2.5 text-xs font-bold font-display shadow-sm inline-block">{header_cta}</a>
            </div>
        </div>
    </header>

    <!-- ГЛАВНЫЙ БЛОК (HERO SECTION) -->
    <section class="max-w-7xl mx-auto w-full px-6 py-12 md:py-24 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center relative">
        <div class="lg:col-span-7 space-y-6 z-10">
            <span class="inline-block px-3.5 py-1 bg-brand-primary/10 text-brand-primary rounded-full text-xs font-bold uppercase tracking-wider {hero_badge}">
                {hero_badge}
            </span>
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-brand-on-background leading-tight tracking-tight font-display uppercase">
                {hero_title}
            </h1>
            <p class="text-brand-on-background/70 text-base md:text-lg leading-relaxed max-w-xl font-serif">
                {sys_desc} Каждый вектор, скругление и цветовой переход собраны по строгому дизайн-контракту без использования устаревших эмодзи.
            </p>
            <div class="pt-4 flex flex-wrap gap-4">
                <a href="#demo" class="btn-primary px-7 py-4 text-sm font-bold shadow-sm inline-block font-display">{hero_btn_1}</a>
                <a href="#features" class="px-7 py-4 bg-brand-surface-low hover:bg-brand-surface-container text-brand-on-background rounded-[var(--radius-default)] text-sm font-bold transition-all inline-block font-display border-3 border-black shadow-[3px_3px_0px_#000]">{hero_btn_2}</a>
            </div>
        </div>
        
        <!-- Ассет с ИИ-иллюстрацией без фона -->
        <div class="lg:col-span-5 flex justify-center relative">
            <div class="absolute -inset-8 bg-gradient-to-tr from-brand-primary/10 to-brand-secondary/10 rounded-full blur-3xl opacity-40 pointer-events-none"></div>
            <div class="w-full max-w-[380px] aspect-square rounded-[var(--radius-xl)] border border-brand-outline-variant bg-brand-surface-lowest/10 backdrop-blur-sm p-4 shadow-sm relative group overflow-hidden">
                <img src="{hero_image_url}" class="w-full h-full object-cover rounded-[var(--radius-lg)] animate-float" alt="AuraDesign Central Asset">
            </div>
        </div>
    </section>

    {content_blocks}

    <!-- СЕКЦИЯ С ФОРМОЙ И КАРТОЧКАМИ ДЕМОНСТРАЦИИ -->
    <section id="demo" class="max-w-7xl mx-auto w-full px-6 py-20 space-y-12">
        <div class="flex flex-col md:flex-row md:items-end justify-between border-b border-brand-outline-variant pb-6 gap-4">
            <div>
                <span class="text-xs font-bold text-brand-primary uppercase tracking-widest block font-mono">[ TESTBENCH_CONTROL ]</span>
                <h2 class="text-3xl md:text-4xl font-extrabold text-brand-on-background font-display tracking-tight">{demo_title}</h2>
            </div>
            <p class="text-brand-on-background/60 text-xs font-mono max-w-sm">{demo_desc}</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Форма -->
            <div class="lg:col-span-5 {'card-interactive' if archetype == 'bumaga' else 'bg-brand-surface-lowest border border-brand-outline-variant'} p-8 rounded-[var(--radius-xl)] space-y-4 shadow-sm relative">
                <h3 class="text-lg font-bold text-brand-on-background font-display tracking-tight">{form_title}</h3>
                
                <form onsubmit="alert('Запрос получен! BUMAGA уже готовит сочную концепцию.'); return false;" class="space-y-4">
                    <div class="space-y-1">
                        <label class="block text-xs font-bold text-brand-on-background/70 font-mono">BRAND_NAME:</label>
                        <input type="text" placeholder="Bumaga Client" required class="w-full px-3 py-2.5 bg-brand-surface-low border border-brand-outline rounded-[var(--radius-default)] text-xs focus:outline-none focus:border-brand-primary text-brand-on-background border-2 border-black">
                    </div>
                    <div class="space-y-1">
                        <label class="block text-xs font-bold text-brand-on-background/70 font-mono">VISUAL_ARCHETYPE:</label>
                        <select class="w-full px-3 py-2.5 bg-brand-surface-low border border-brand-outline rounded-[var(--radius-default)] text-xs focus:outline-none focus:border-brand-primary text-brand-on-background border-2 border-black">
                            <option>SaaS Premium (Light Minimalist)</option>
                            <option>FinTech Slate (Dark Monospace)</option>
                            <option>Atmospheric Glass (Glassmorphism)</option>
                            <option>Friendly Organic (Paws & Paths)</option>
                            <option>Cosmic Totality (Solar Eclipse)</option>
                            <option>Scientific Alpinism (Victorian Navy)</option>
                            <option selected>BUMAGA Creative (Neo-Brutalist)</option>
                        </select>
                    </div>
                    <div class="space-y-1">
                        <label class="block text-xs font-bold text-brand-on-background/70 font-mono">EMAIL_ADDRESS:</label>
                        <input type="email" placeholder="client@bumaga-bureau.ru" required class="w-full px-3 py-2.5 bg-brand-surface-low border border-brand-outline rounded-[var(--radius-default)] text-xs focus:outline-none focus:border-brand-primary text-brand-on-background border-2 border-black">
                    </div>
                    
                    <button type="submit" class="w-full py-3.5 btn-primary text-xs font-bold font-display shadow-sm">
                        {form_btn}
                    </button>
                </form>
            </div>

            <!-- Интерактивный интерактор состояний -->
            <div class="lg:col-span-7 {'card-interactive' if archetype == 'bumaga' else 'bg-brand-surface-low border border-brand-outline-variant'} p-8 space-y-6 relative overflow-hidden">
                <h3 class="text-xl font-bold text-brand-on-background font-display tracking-tight">{verif_title}</h3>
                <p class="text-brand-on-background/70 text-sm font-serif">{verif_desc}</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
                    <div class="p-6 bg-brand-surface-lowest border border-brand-outline-variant rounded-[var(--radius-lg)] space-y-3 relative">
                        <span class="text-[10px] text-brand-on-background/50 font-bold uppercase tracking-widest block font-mono">BUTTON_STATES</span>
                        <div class="flex flex-wrap gap-2">
                            <button class="btn-primary px-4 py-2 text-xs font-bold">Активна</button>
                            <button class="btn-primary px-4 py-2 text-xs font-bold opacity-40 cursor-not-allowed" disabled>Блокирована</button>
                        </div>
                    </div>
                    <div class="p-6 bg-brand-surface-lowest border border-brand-outline-variant rounded-[var(--radius-lg)] space-y-3 relative">
                        <span class="text-[10px] text-brand-on-background/50 font-bold uppercase tracking-widest block font-mono">AURA_INDICATORS</span>
                        <div class="flex flex-wrap gap-2">
                            <span class="px-2.5 py-1 bg-brand-primary/10 text-brand-primary text-[10px] font-bold font-mono rounded-full">STATE_ACTIVE</span>
                            <span class="px-2.5 py-1 bg-brand-secondary/10 text-brand-secondary text-[10px] font-bold font-mono rounded-full">STATE_PENDING</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ПОДВАЛ (FOOTER) -->
    <footer class="bg-brand-on-background text-brand-background border-t border-brand-outline-variant py-16 relative">
        <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12">
            <div class="space-y-4">
                <span class="text-xl font-extrabold text-white tracking-tight font-display">{sys_name}</span>
                <p class="text-xs text-brand-background/60 leading-relaxed max-w-xs font-serif">
                    Интеллектуальная дизайн-система на основе независимого машиночитаемого контракта. Никакого визуального мусора, клише и эмодзи.
                </p>
            </div>
            <div>
                <h4 class="text-sm font-bold text-white mb-6 font-display">Навигация по коду</h4>
                <ul class="text-xs text-brand-background/60 space-y-3 font-mono">
                    <li><a href="#features" class="hover:underline hover:text-brand-primary">[ PRESETS_LIBRARY ]</a></li>
                    <li><a href="#demo" class="hover:underline hover:text-brand-primary">[ COMPILER_TEST ]</a></li>
                    <li><a href="#demo" class="hover:underline hover:text-brand-primary">[ AURADESIGN_SPEC_REF ]</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-sm font-bold text-white mb-6 font-display">Машиночитаемый лог</h4>
                <div class="p-4 bg-white/5 rounded-[var(--radius-default)] border border-white/10 text-[11px] text-brand-background/70 font-mono leading-normal">
                    // AuraDesign Core Tokens:<br>
                    primary: {c_primary}<br>
                    background: {c_background}<br>
                    typography: {font_main_clean}
                </div>
            </div>
        </div>
        <div class="max-w-7xl mx-auto px-6 border-t border-white/10 mt-12 pt-8 flex flex-col sm:flex-row items-center justify-between text-[10px] text-brand-background/40 font-mono">
            <span>© 2026 {sys_name} Inc. Все права защищены.</span>
            <span class="uppercase tracking-widest font-semibold pt-2 sm:pt-0">Сверстано AuraDesign Agent</span>
        </div>
    </footer>

</body>
</html>
"""
    return html_template


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AuraDesign Agent CLI Generator")
    parser.add_argument("--contract", default="AURADESIGN.md", help="Путь к файлу дизайн-контракта")
    parser.add_argument("--hero-image", default="", help="URL безфонового ассета для Hero-блока")
    parser.add_argument("--output", default="index.html", help="Путь для сохранения готового HTML")
    
    args = parser.parse_args()
    
    print(f"[Generate] Запуск генератора AuraDesign...")
    
    if not os.path.exists(args.contract):
        print(f"[Error] Дизайн-контракт по пути {args.contract} не найден! Сначала запустите сканер.", file=sys.stderr)
        sys.exit(1)
        
    print(f"[Generate] Чтение контракта: {args.contract}")
    try:
        with open(args.contract, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[Error] Ошибка при чтении файла контракта: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("[Generate] Парсинг и разрешение токенов дизайн-системы...")
    tokens = parse_yaml_front_matter(content)
    
    if not tokens:
        print("[Error] Ошибка: В файле контракта отсутствует или повреждён YAML блок токенов!", file=sys.stderr)
        sys.exit(1)
        
    print(f"[Generate] Сформирована дизайн-система '{get_token(tokens, 'name')}'")
    
    print("[Generate] Сборка HTML страницы и встраивание ассетов...")
    html_code = generate_html_page(tokens, args.hero_image)
    
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_code)
        print(f"[OK] Веб-страница успешно создана и сохранена по пути: {args.output}")
    except Exception as e:
        print(f"[Error] Ошибка записи готового HTML в файл: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
