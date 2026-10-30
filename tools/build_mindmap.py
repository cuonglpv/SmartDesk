"""Build docs/mindmap/smartdesk.xmind and an XMind-style PNG for each sheet."""

import json
import uuid
import zipfile

from common import DOCS, esc, render_html, shade, svg_page, text_width, tint
import model

OUT = DOCS / "mindmap"
PALETTE = ["#E5484D", "#F2803A", "#2BA36B", "#14A3A3", "#3B82F6",
           "#7C5CE0", "#D9467A", "#C98A0A", "#0E8FB8"]

SHEETS = [
    ("Top-down problem analysis", model.TOP_DOWN_ROOT, model.TOP_DOWN, "mindmap-top-down"),
    ("Feature map", model.FEATURE_ROOT, model.FEATURES, "mindmap-features"),
]


# ---------------------------------------------------------------------------
# .xmind (XMind 2020+ JSON format)
# ---------------------------------------------------------------------------

def _topic(title, style=None, children=None):
    topic = {"id": uuid.uuid4().hex, "class": "topic", "title": title}
    if style:
        topic["style"] = {"id": uuid.uuid4().hex, "properties": style}
    if children:
        topic["children"] = {"attached": children}
    return topic


def build_xmind():
    sheets = []
    for title, root, branches, _ in SHEETS:
        mains = []
        for i, (branch, leaves) in enumerate(branches):
            color = PALETTE[i % len(PALETTE)]
            subs = [_topic(leaf, {"svg:fill": tint(color, 0.14), "fo:color": "#1F2937",
                                  "border-line-width": "0pt", "line-color": color})
                    for leaf in leaves]
            mains.append(_topic(branch, {"svg:fill": color, "fo:color": "#FFFFFF",
                                         "fo:font-weight": "bold", "line-color": color,
                                         "border-line-color": shade(color, 0.15)}, subs))
        root_topic = _topic(root, {"svg:fill": "#FFFFFF", "fo:color": "#111827",
                                   "fo:font-weight": "bold", "border-line-color": "#111827",
                                   "border-line-width": "3pt"}, mains)
        root_topic["structureClass"] = "org.xmind.ui.map.clockwise"
        sheets.append({"id": uuid.uuid4().hex, "class": "sheet", "title": title,
                       "rootTopic": root_topic,
                       "topicPositioning": "fixed"})
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "smartdesk.xmind"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("content.json", json.dumps(sheets, ensure_ascii=False, indent=1))
        z.writestr("metadata.json", json.dumps({"creator": {"name": "SmartDesk docs"}}))
        z.writestr("manifest.json", json.dumps(
            {"file-entries": {"content.json": {}, "metadata.json": {}}}))
    return path


# ---------------------------------------------------------------------------
# PNG render in XMind "map" layout
# ---------------------------------------------------------------------------

MAIN_FS, SUB_FS, ROOT_FS = 21, 16, 34
SUB_H, SUB_GAP, BLOCK_GAP = 34, 10, 34
MAIN_H = 50
MAIN_SUB_FS, MAIN_LINE_H = 15, 24  # second line of a main topic (actors)
PAD_X = 16


def _rounded_path(points, r=10):
    """Polyline with rounded corners (used for XMind-like elbow branches)."""
    d = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    for i in range(1, len(points) - 1):
        (x0, y0), (x1, y1), (x2, y2) = points[i - 1], points[i], points[i + 1]
        rr = min(r, abs(x1 - x0) / 2 or r, abs(y1 - y0) / 2 or r,
                 abs(x2 - x1) / 2 or r, abs(y2 - y1) / 2 or r)
        sx = (x1 - x0 > 0) - (x1 - x0 < 0)
        sy = (y1 - y0 > 0) - (y1 - y0 < 0)
        ex = (x2 - x1 > 0) - (x2 - x1 < 0)
        ey = (y2 - y1 > 0) - (y2 - y1 < 0)
        d += f" L{x1 - sx * rr:.1f},{y1 - sy * rr:.1f} Q{x1:.1f},{y1:.1f} {x1 + ex * rr:.1f},{y1 + ey * rr:.1f}"
    d += f" L{points[-1][0]:.1f},{points[-1][1]:.1f}"
    return d


def render_sheet(root, branches, name):
    n = len(branches)
    right = list(range((n + 1) // 2))
    left = list(range((n + 1) // 2, n))[::-1]  # clockwise: left side bottom -> top

    def main_h(i):
        return MAIN_H + MAIN_LINE_H * (len(branches[i][0].split("\n")) - 1)

    def block_h(i):
        k = len(branches[i][1])
        return max(main_h(i), k * SUB_H + (k - 1) * SUB_GAP)

    def side_h(idx):
        return sum(block_h(i) for i in idx) + BLOCK_GAP * (len(idx) - 1)

    height = max(side_h(right), side_h(left)) + 140
    root_lines = root.split("\n")
    root_w = max(text_width(t, ROOT_FS if j == 0 else 20, True) for j, t in enumerate(root_lines)) + 70
    root_h = 64 + 30 * (len(root_lines) - 1)

    main_w = {i: max(text_width(t, MAIN_FS if j == 0 else MAIN_SUB_FS, j == 0)
                     for j, t in enumerate(b.split("\n"))) + 2 * PAD_X + 8
              for i, (b, _) in enumerate(branches)}
    sub_w = {i: max(text_width(s, SUB_FS) for s in leaves) + 2 * PAD_X
             for i, (_, leaves) in enumerate(branches)}
    reach = lambda idx: max((main_w[i] + 60 + sub_w[i] for i in idx), default=0)
    gap_root = 120
    width = reach(left) + reach(right) + root_w + 2 * gap_root + 80
    cx = 40 + reach(left) + gap_root + root_w / 2
    cy = height / 2

    parts = []
    nodes = []

    def place(idx, side):
        y = cy - side_h(idx) / 2
        for i in idx:
            bh = block_h(i)
            my = y + bh / 2
            color = PALETTE[i % len(PALETTE)]
            title, leaves = branches[i]
            mw = main_w[i]
            mx = cx + side * (root_w / 2 + gap_root) + (0 if side > 0 else -mw)
            # root -> main curve
            sx = cx + side * (root_w / 2 - 12)
            ex = mx if side > 0 else mx + mw
            parts.append(
                f"<path d='M{sx:.1f},{cy:.1f} C{sx + side * 70:.1f},{cy:.1f} "
                f"{ex - side * 80:.1f},{my:.1f} {ex:.1f},{my:.1f}' fill='none' "
                f"stroke='{color}' stroke-width='4' stroke-linecap='round'/>")
            mh = main_h(i)
            lines = title.split("\n")
            nodes.append(
                f"<rect x='{mx:.1f}' y='{my - mh / 2:.1f}' width='{mw:.1f}' height='{mh}' "
                f"rx='12' fill='{color}' stroke='{shade(color, 0.18)}' stroke-width='2.5'/>")
            for j, line in enumerate(lines):
                ty = my + 7 - MAIN_LINE_H * (len(lines) - 1) / 2 + j * MAIN_LINE_H
                nodes.append(
                    f"<text x='{mx + mw / 2:.1f}' y='{ty:.1f}' text-anchor='middle' "
                    f"font-size='{MAIN_FS if j == 0 else MAIN_SUB_FS}' "
                    f"font-weight='{700 if j == 0 else 500}' fill='#fff' "
                    f"opacity='{1 if j == 0 else .92}'>{esc(line)}</text>")
            # main -> subtopics (elbow bracket)
            k = len(leaves)
            sy0 = my - (k * SUB_H + (k - 1) * SUB_GAP) / 2
            out_x = mx + mw if side > 0 else mx
            trunk_x = out_x + side * 28
            sw = sub_w[i]
            for j, leaf in enumerate(leaves):
                ly = sy0 + j * (SUB_H + SUB_GAP) + SUB_H / 2
                lx = trunk_x + side * 22 + (0 if side > 0 else -sw)
                end_x = lx if side > 0 else lx + sw
                parts.append(
                    f"<path d='{_rounded_path([(out_x, my), (trunk_x, my), (trunk_x, ly), (end_x, ly)])}' "
                    f"fill='none' stroke='{color}' stroke-width='2' opacity='.8'/>")
                nodes.append(
                    f"<rect x='{lx:.1f}' y='{ly - SUB_H / 2:.1f}' width='{sw:.1f}' height='{SUB_H}' rx='9' "
                    f"fill='{tint(color, 0.13)}'/>"
                    f"<text x='{lx + (PAD_X if side > 0 else sw - PAD_X):.1f}' y='{ly + 5.5:.1f}' "
                    f"text-anchor='{'start' if side > 0 else 'end'}' font-size='{SUB_FS}' "
                    f"fill='{shade(color, 0.55)}'>{esc(leaf)}</text>")
            y += bh + BLOCK_GAP

    place(right, 1)
    place(left, -1)

    root_svg = (f"<rect x='{cx - root_w / 2:.1f}' y='{cy - root_h / 2:.1f}' width='{root_w:.1f}' "
                f"height='{root_h}' rx='16' fill='#fff' stroke='#111827' stroke-width='4'/>")
    for j, line in enumerate(root_lines):
        fs = ROOT_FS if j == 0 else 20
        ty = cy - root_h / 2 + 44 + j * 32
        root_svg += (f"<text x='{cx:.1f}' y='{ty:.1f}' text-anchor='middle' font-size='{fs}' "
                     f"font-weight='{800 if j == 0 else 600}' fill='{'#111827' if j == 0 else '#4b5563'}'>"
                     f"{esc(line)}</text>")

    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{width:.0f}' height='{height:.0f}' "
           f"viewBox='0 0 {width:.0f} {height:.0f}'>{''.join(parts)}{''.join(nodes)}{root_svg}</svg>")
    return render_html(svg_page(svg, width, height), OUT / f"{name}.png", width, height)


if __name__ == "__main__":
    print(build_xmind())
    for _, root, branches, name in SHEETS:
        print(render_sheet(root, branches, name))
