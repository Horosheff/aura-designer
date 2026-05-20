#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aura Designer - Source Analyzer
===============================
Строит машинные карты источника для режима copy-in-copy:
`AURA_SOURCE_MAP.json`, `AURA_COMPOSITION_LOCK.json`, `AURA_COMPONENT_MAP.json`,
`AURA_SHAPE_MAP.json`.

Модуль намеренно работает на стандартной библиотеке Python. В Cursor sub-agent
может дополнять эти карты данными браузера, скриншотами и MCP-инструментами.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser


if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class SourceHTMLParser(HTMLParser):
    def __init__(self, base_url=""):
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.meta = {}
        self.links = []
        self.images = []
        self.headings = []
        self.buttons = []
        self.anchors = []
        self.forms = []
        self.inline_styles = []
        self.class_names = []
        self._tag_stack = []
        self._capture_title = False
        self._capture_heading = None
        self._capture_button = False
        self._text_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._tag_stack.append(tag)

        class_value = attrs_dict.get("class", "")
        if class_value:
            self.class_names.extend(class_value.split())

        style_value = attrs_dict.get("style", "")
        if style_value:
            self.inline_styles.append(style_value)

        if tag == "title":
            self._capture_title = True
            self._text_buffer = []
        elif tag in {"h1", "h2", "h3", "h4"}:
            self._capture_heading = tag
            self._text_buffer = []
        elif tag == "button":
            self._capture_button = True
            self._text_buffer = []
        elif tag == "meta":
            name = attrs_dict.get("name") or attrs_dict.get("property")
            content = attrs_dict.get("content")
            if name and content:
                self.meta[name] = content
        elif tag == "link":
            href = attrs_dict.get("href")
            rel = attrs_dict.get("rel", "")
            if href:
                self.links.append({"rel": rel, "href": urllib.parse.urljoin(self.base_url, href)})
        elif tag == "img":
            src = attrs_dict.get("src") or attrs_dict.get("data-src") or attrs_dict.get("data-lazy-src")
            if src:
                self.images.append({
                    "src": urllib.parse.urljoin(self.base_url, src),
                    "alt": attrs_dict.get("alt", ""),
                    "class": class_value,
                    "style": style_value,
                })
        elif tag == "a":
            href = attrs_dict.get("href", "")
            self.anchors.append({
                "href": urllib.parse.urljoin(self.base_url, href) if href else "",
                "class": class_value,
                "text": "",
            })
        elif tag == "form":
            self.forms.append({"class": class_value, "style": style_value})

    def handle_endtag(self, tag):
        text = " ".join("".join(self._text_buffer).split())
        if tag == "title" and self._capture_title:
            self.title = text
            self._capture_title = False
        elif self._capture_heading == tag:
            if text:
                self.headings.append({"tag": tag, "text": text})
            self._capture_heading = None
        elif tag == "button" and self._capture_button:
            if text:
                self.buttons.append(text)
            self._capture_button = False

        self._text_buffer = []
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data):
        if self._capture_title or self._capture_heading or self._capture_button:
            self._text_buffer.append(data)


def fetch_html(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AuraDesigner/1.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8", errors="ignore")


def unique(items, limit=None):
    result = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result[:limit] if limit else result


def extract_colors(html, inline_styles):
    colors = re.findall(r"#[0-9a-fA-F]{3,8}\b", html)
    for style in inline_styles:
        colors.extend(re.findall(r"#[0-9a-fA-F]{3,8}\b", style))
        colors.extend(re.findall(r"rgba?\([^)]+\)", style))
    return unique([color.lower() for color in colors], 24)


def extract_fonts(html, links):
    fonts = []
    fonts.extend(re.findall(r"font-family\s*:\s*['\"]?([^;'\"}]+)", html, flags=re.IGNORECASE))
    for link in links:
        href = link.get("href", "")
        if "fonts.googleapis" in href and "family=" in href:
            query = urllib.parse.urlparse(href).query
            for family in urllib.parse.parse_qs(query).get("family", []):
                fonts.append(family.split(":")[0].replace("+", " "))
    return unique([font.strip().split(",")[0] for font in fonts if font.strip()], 12)


def infer_components(parser):
    classes = " ".join(parser.class_names).lower()
    components = []
    signals = {
        "header": ["header", "nav", "navbar", "menu"],
        "hero": ["hero", "intro", "cover", "masthead"],
        "cards": ["card", "grid", "bento", "feature"],
        "ticker": ["ticker", "marquee", "running", "scroll"],
        "gallery": ["gallery", "portfolio", "case", "work"],
        "form": ["form", "input", "contact"],
        "footer": ["footer"],
    }
    for component, needles in signals.items():
        if any(needle in classes for needle in needles):
            components.append({"type": component, "confidence": "class-signal"})

    if parser.forms and not any(c["type"] == "form" for c in components):
        components.append({"type": "form", "confidence": "tag"})
    if parser.images and not any(c["type"] == "gallery" for c in components):
        components.append({"type": "image-assets", "confidence": "tag"})
    return components


def classify_shape_from_token(token):
    lowered = token.lower()
    if any(part in lowered for part in ["rounded-full", "circle", "avatar", "dot"]):
        return "circle-or-pill"
    if any(part in lowered for part in ["pill", "badge", "chip", "tag", "capsule"]):
        return "capsule"
    if any(part in lowered for part in ["blob", "blot", "organic", "squiggle"]):
        return "organic-blob"
    if any(part in lowered for part in ["star", "spark", "burst"]):
        return "star-or-sparkle"
    if any(part in lowered for part in ["wave", "curve", "swoosh"]):
        return "wave-or-curve"
    if any(part in lowered for part in ["card", "panel", "tile"]):
        return "card-container"
    if any(part in lowered for part in ["line", "divider", "border"]):
        return "line-or-divider"
    if "rounded" in lowered:
        return "rounded-rectangle"
    return ""


def extract_shape_tokens(parser):
    tokens = []
    for class_name in parser.class_names:
        shape_type = classify_shape_from_token(class_name)
        if shape_type:
            tokens.append({
                "source": "class",
                "token": class_name,
                "shapeType": shape_type,
                "copyRule": "Повторить тип формы и не добавлять stroke/shadow без источника.",
            })

    for style in parser.inline_styles:
        lowered = style.lower()
        if "border-radius" in lowered:
            tokens.append({
                "source": "inline-style",
                "token": style,
                "shapeType": "border-radius-shape",
                "copyRule": "Скопировать фактический border-radius и пропорции.",
            })
        if "clip-path" in lowered:
            tokens.append({
                "source": "inline-style",
                "token": style,
                "shapeType": "clipped-custom-shape",
                "copyRule": "Скопировать clip-path или перенести контур в inline SVG.",
            })
        if "box-shadow" in lowered:
            tokens.append({
                "source": "inline-style",
                "token": style,
                "shapeType": "shadow-signal",
                "copyRule": "Скопировать тип тени: мягкая/жесткая/ambient; не усиливать черным.",
            })

    unique_tokens = []
    seen = set()
    for item in tokens:
        key = (item["source"], item["token"], item["shapeType"])
        if key not in seen:
            unique_tokens.append(item)
            seen.add(key)
    return unique_tokens[:80]


def build_shape_map(data, parser=None):
    if parser:
        detected = extract_shape_tokens(parser)
        confidence = "class-and-style-heuristics"
    else:
        detected = []
        confidence = "requires-visual-analysis"

    return {
        "version": "alpha",
        "source": data.get("source", ""),
        "purpose": "Фиксирует формы источника, чтобы агент копировал кляксы, круги, blobs, капсулы, линии и тени без стилевого смешения.",
        "confidence": confidence,
        "detectedShapeSignals": detected,
        "manualShapeChecklist": [
            {
                "id": "hero-decor",
                "whatToCapture": "Все декоративные формы hero: кляксы, круги, stickers, blobs, линии, волны.",
                "fields": ["shapeType", "width", "height", "radius", "fill", "stroke", "strokeWidth", "shadow", "opacity", "rotation", "zIndex"],
            },
            {
                "id": "buttons-and-badges",
                "whatToCapture": "Формы кнопок, бейджей, тегов, чипов и декоративных подписей.",
                "fields": ["shapeType", "padding", "radius", "fill", "stroke", "shadow", "hoverBehavior"],
            },
            {
                "id": "cards-and-containers",
                "whatToCapture": "Карточки, панели, рамки, разделители и фоновые плоскости.",
                "fields": ["shapeType", "border", "borderOpacity", "shadow", "background", "cornerRadius"],
            },
            {
                "id": "icons-and-symbols",
                "whatToCapture": "SVG/иконки: число лучей/лепестков, симметрия, мягкость углов, наличие stroke.",
                "fields": ["shapeType", "pathStyle", "pointCount", "symmetry", "stroke", "fill", "lineJoin"],
            },
        ],
        "strictRules": [
            "Не заменять форму источника другой декоративной формой.",
            "Если в источнике клякса/blob, использовать органический SVG path с кривыми.",
            "Если в источнике круг, использовать круг; если капсула, использовать капсулу.",
            "Не добавлять черные stroke и flat-shadow, если их нет в источнике.",
            "Перед финальным отчетом сравнить форму, пропорции, radius, stroke, shadow, opacity и rotation.",
        ],
    }


def infer_composition(parser):
    first_h1 = next((h for h in parser.headings if h["tag"] == "h1"), parser.headings[0] if parser.headings else None)
    primary_image = parser.images[0] if parser.images else None
    class_blob = " ".join(parser.class_names).lower()

    image_position = "unknown"
    if any(token in class_blob for token in ["center", "mx-auto", "items-center", "justify-center"]):
        image_position = "center"
    elif any(token in class_blob for token in ["right", "end"]):
        image_position = "right"
    elif any(token in class_blob for token in ["left", "start"]):
        image_position = "left"

    headline_layer = "normal"
    if any(token in class_blob for token in ["absolute", "z-", "behind", "overlap", "mix-blend"]):
        headline_layer = "requires-manual-layer-check"

    return {
        "replicationMode": "copy-in-copy",
        "sourceIsLaw": True,
        "hero": {
            "headline": first_h1["text"] if first_h1 else "",
            "headlineTag": first_h1["tag"] if first_h1 else "",
            "headlineLayer": headline_layer,
            "primaryImage": primary_image,
            "imagePosition": image_position,
            "mustPreserveLayering": True,
            "mustNotChangeThemeWithoutUserRequest": True,
        },
        "layout": {
            "detectedClassSignals": unique(parser.class_names, 80),
            "componentOrderMustFollowSource": True,
        },
    }


def analyze_url(url):
    html = fetch_html(url)
    parser = SourceHTMLParser(base_url=url)
    parser.feed(html)

    data = {
        "sourceType": "url",
        "source": url,
        "title": parser.title or parser.meta.get("og:title", ""),
        "description": parser.meta.get("description") or parser.meta.get("og:description", ""),
        "colors": extract_colors(html, parser.inline_styles),
        "fonts": extract_fonts(html, parser.links),
        "headings": parser.headings[:24],
        "buttons": parser.buttons[:24],
        "images": parser.images[:24],
        "links": parser.anchors[:24],
        "components": infer_components(parser),
        "composition": infer_composition(parser),
    }
    data["shapeMap"] = build_shape_map(data, parser)
    return data


def analyze_image(image):
    name = os.path.basename(image)
    data = {
        "sourceType": "image",
        "source": image,
        "title": os.path.splitext(name)[0].replace("-", " ").replace("_", " ").strip().title(),
        "description": "Источник является изображением. Требуется визуальный анализ через sub-agent/browser или мультимодальную модель.",
        "colors": [],
        "fonts": [],
        "headings": [],
        "buttons": [],
        "images": [{"src": image, "alt": name, "class": "", "style": ""}],
        "links": [],
        "components": [{"type": "image-reference", "confidence": "input"}],
        "composition": {
            "replicationMode": "copy-in-copy",
            "sourceIsLaw": True,
            "hero": {
                "headline": "",
                "headlineLayer": "requires-visual-analysis",
                "primaryImage": {"src": image, "alt": name},
                "imagePosition": "requires-visual-analysis",
                "mustPreserveLayering": True,
                "mustNotChangeThemeWithoutUserRequest": True,
            },
        },
    }
    data["shapeMap"] = build_shape_map(data)
    return data


def write_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Aura Designer Source Analyzer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL источника")
    group.add_argument("--image", help="Путь или URL изображения-референса")
    parser.add_argument("--output-dir", default=".", help="Папка для JSON-карт")
    args = parser.parse_args()

    print("[Analyze] Строю машинные карты источника...")
    data = analyze_url(args.url) if args.url else analyze_image(args.image)

    source_map = {
        "version": "alpha",
        "source": data,
        "contractMode": "source-accurate-replication",
    }
    composition_lock = data["composition"]
    component_map = {
        "source": data["source"],
        "components": data["components"],
        "headings": data["headings"],
        "buttons": data["buttons"],
        "images": data["images"],
    }
    shape_map = data.get("shapeMap") or build_shape_map(data)

    write_json(os.path.join(args.output_dir, "AURA_SOURCE_MAP.json"), source_map)
    write_json(os.path.join(args.output_dir, "AURA_COMPOSITION_LOCK.json"), composition_lock)
    write_json(os.path.join(args.output_dir, "AURA_COMPONENT_MAP.json"), component_map)
    write_json(os.path.join(args.output_dir, "AURA_SHAPE_MAP.json"), shape_map)

    print("[OK] Source maps созданы:")
    print(f"- {os.path.join(args.output_dir, 'AURA_SOURCE_MAP.json')}")
    print(f"- {os.path.join(args.output_dir, 'AURA_COMPOSITION_LOCK.json')}")
    print(f"- {os.path.join(args.output_dir, 'AURA_COMPONENT_MAP.json')}")
    print(f"- {os.path.join(args.output_dir, 'AURA_SHAPE_MAP.json')}")


if __name__ == "__main__":
    main()
