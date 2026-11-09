#!/usr/bin/env python3
"""Validate 3-Theme Design System v1.1 using Python standard library only."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
CLASSIC_KEYS = {"accent", "onAccent", "accentSoft", "secondary", "decorative"}
BASE_KEYS = {"background", "surface", "surfaceMuted", "text", "textMuted", "border"}
TREND_KEYS = BASE_KEYS | CLASSIC_KEYS
STATUS_KEYS = {"success", "warning", "danger"}
errors = []

def fail(message):
    errors.append(message)

def load(path):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"{path}: {exc}")
        return {}

def validate_colors(name, values, required):
    if not isinstance(values, dict):
        fail(f"{name}: expected an object")
        return
    if set(values) != required:
        fail(f"{name}: expected keys {sorted(required)}; got {sorted(values)}")
    for key, value in values.items():
        if not isinstance(value, str) or not HEX.fullmatch(value):
            fail(f"{name}.{key}: expected #RRGGBB")

def luminance(value):
    rgb = [int(value[x:x + 2], 16) / 255 for x in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045 else
              ((channel + 0.055) / 1.055) ** 2.4 for channel in rgb]
    return sum(a * b for a, b in zip(linear, (0.2126, 0.7152, 0.0722)))

def contrast(a, b):
    bright, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (bright + 0.05) / (dark + 0.05)

def check_pairs(name, tokens):
    for foreground, background in (
        ("text", "background"), ("text", "surface"), ("text", "surfaceMuted"),
        ("textMuted", "background"), ("textMuted", "surface"),
        ("onAccent", "accent"),
    ):
        a, b = tokens.get(foreground), tokens.get(background)
        if not all(isinstance(x, str) and HEX.fullmatch(x) for x in (a, b)):
            continue
        ratio = contrast(a, b)
        if ratio < 4.5:
            fail(f"{name}: {foreground}/{background} = {ratio:.2f}:1 < 4.5:1")

def main():
    core = load("themes/core.json")
    themes = {name: load(f"themes/{name}.json") for name in ("dark", "light", "trend")}
    if core.get("version") != "1.1.0":
        fail("core.version must be 1.1.0")
    for mode in ("dark", "light"):
        validate_colors(f"core.foundations.{mode}", core.get("foundations", {}).get(mode), BASE_KEYS)
        validate_colors(f"core.status.{mode}", core.get("status", {}).get(mode), STATUS_KEYS)
    editions = set()
    for name, theme in themes.items():
        if theme.get("id") != name:
            fail(f"{name}: id mismatch")
        edition = theme.get("edition")
        if not isinstance(edition, str) or not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", edition):
            fail(f"{name}: edition must be YYYY-MM")
        else:
            editions.add(edition)
        if name in ("dark", "light"):
            if theme.get("kind") != "classic" or theme.get("mode") != name:
                fail(f"{name}: classic metadata mismatch")
            validate_colors(f"{name}.tokens", theme.get("tokens"), CLASSIC_KEYS)
            resolved = {**core.get("foundations", {}).get(name, {}), **theme.get("tokens", {})}
        else:
            if theme.get("kind") != "editorial" or theme.get("mode") not in ("dark", "light"):
                fail("trend: editorial metadata mismatch")
            if not theme.get("label") or not theme.get("provenance"):
                fail("trend: label and provenance are required")
            validate_colors("trend.tokens", theme.get("tokens"), TREND_KEYS)
            resolved = theme.get("tokens", {})
        check_pairs(name, resolved)
    if len(editions) != 1:
        fail("All active themes must have the same monthly edition")
    if len(editions) == 1:
        edition = next(iter(editions))
        snapshot = load(f"archives/{edition}.json")
        if snapshot.get("edition") != edition:
            fail("Archive edition mismatch")
        for name in themes:
            if snapshot.get(name) != themes[name]:
                fail(f"archives/{edition}.json: {name} snapshot does not match active theme")
    if errors:
        for issue in errors:
            print("FAIL:", issue)
        return 1
    print(f"PASS: three themes, monthly snapshot and WCAG text contrast checks ({next(iter(editions))})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
