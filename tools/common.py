"""Shared helpers: text measuring, colour tints and HTML -> PNG rendering."""

import os
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
FONT_DIR = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
FONT_FAMILY = "'Segoe UI', 'Noto Sans', Arial, sans-serif"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


@lru_cache(maxsize=None)
def _font(size, bold):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), size)


def text_width(text, size, bold=False):
    return _font(size, bold).getlength(text)


def wrap(text, size, max_width, bold=False):
    """Greedy word wrap using real font metrics."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if text_width(trial, size, bold) <= max_width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def tint(hex_color, amount):
    """Mix a colour with white; amount=0 -> white, 1 -> colour."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    mix = lambda c: round(255 - (255 - c) * amount)
    return f"#{mix(r):02x}{mix(g):02x}{mix(b):02x}"


def shade(hex_color, amount):
    """Darken a colour; amount=0 -> unchanged, 1 -> black."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    mix = lambda c: round(c * (1 - amount))
    return f"#{mix(r):02x}{mix(g):02x}{mix(b):02x}"


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def chrome():
    for path in CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    raise FileNotFoundError("Chrome or Edge is required to render PNG files")


def screenshot(url, out_png, width, height, scale=2):
    """Render a URL (file:// or http://) to PNG with headless Chrome/Edge."""
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([
            chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--no-first-run", f"--user-data-dir={profile}",
            f"--force-device-scale-factor={scale}",
            f"--window-size={int(width)},{int(height)}",
            "--virtual-time-budget=3000",
            f"--screenshot={out_png}", url,
        ], check=True, capture_output=True, timeout=120)
    return out_png


def render_html(html, out_png, width, height, scale=2):
    """Write HTML next to the PNG (kept as editable source) and screenshot it."""
    out_png = Path(out_png)
    src = out_png.with_suffix(".html")
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(html, encoding="utf-8")
    return screenshot(src.resolve().as_uri(), out_png, width, height, scale)


def svg_page(svg, width, height, background="#ffffff"):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>"
            f"html,body{{margin:0;padding:0;background:{background};}}"
            f"svg{{display:block;font-family:{FONT_FAMILY};}}</style></head>"
            f"<body>{svg}</body></html>")
