"""Render the UML use case diagrams to docs/images/use-cases/*.png."""

from common import DOCS, esc, render_html, svg_page
import model

OUT = DOCS / "images" / "use-cases"

ELL_W, ELL_H, ELL_GAP, EXT_GAP = 420, 60, 18, 46
PKG_PAD_TOP, PKG_PAD, PKG_GAP = 40, 18, 22
BOUND_X, BOUND_W = 330, 560
ACTOR_MIN_GAP = 170
INK, LINE, ELL_FILL, ELL_STROKE = "#1e293b", "#94a3b8", "#eef4ff", "#5b7fc7"
AI_FILL, AI_STROKE = "#e7f7f1", "#2f9e7a"


def actor_svg(x, y, name, secondary=False):
    color = "#475569" if secondary else INK
    return (f"<g stroke='{color}' stroke-width='2.4' fill='none' stroke-linecap='round'>"
            f"<circle cx='{x}' cy='{y - 38}' r='13' fill='#fff'/>"
            f"<line x1='{x}' y1='{y - 25}' x2='{x}' y2='{y + 10}'/>"
            f"<line x1='{x - 22}' y1='{y - 12}' x2='{x + 22}' y2='{y - 12}'/>"
            f"<line x1='{x}' y1='{y + 10}' x2='{x - 18}' y2='{y + 38}'/>"
            f"<line x1='{x}' y1='{y + 10}' x2='{x + 18}' y2='{y + 38}'/></g>"
            f"<text x='{x}' y='{y + 64}' text-anchor='middle' font-size='17' font-weight='700' "
            f"fill='{color}'>{esc(name)}</text>"
            + (f"<text x='{x}' y='{y + 84}' text-anchor='middle' font-size='13' fill='#64748b'>"
               f"«secondary»</text>" if secondary else ""))


def spread(items, top, bottom):
    """Keep actors at least ACTOR_MIN_GAP apart while staying near their target y."""
    items = sorted(items, key=lambda a: a[1])
    for i in range(1, len(items)):
        name, y = items[i]
        if y - items[i - 1][1] < ACTOR_MIN_GAP:
            items[i] = (name, items[i - 1][1] + ACTOR_MIN_GAP)
    overflow = items[-1][1] - bottom if items else 0
    if overflow > 0:
        items = [(n, max(top, y - overflow)) for n, y in items]
    return dict(items)


def build(diagram):
    cx = BOUND_X + BOUND_W / 2
    ext_targets = {a for a, _ in diagram["extends"]}
    y = 110
    pos, parts = {}, []
    for title, ucs in diagram["packages"]:
        top = y
        y += PKG_PAD_TOP
        for i, uc in enumerate(ucs):
            if i:
                y += EXT_GAP if uc in ext_targets else ELL_GAP
            pos[uc] = y + ELL_H / 2
            y += ELL_H
        y += PKG_PAD
        parts.append(
            f"<rect x='{BOUND_X + 28}' y='{top}' width='{BOUND_W - 56}' height='{y - top}' rx='10' "
            f"fill='#fff' fill-opacity='.55' stroke='#9fb3d1' stroke-dasharray='6 5'/>"
            f"<text x='{BOUND_X + 44}' y='{top + 25}' font-size='13' font-weight='700' "
            f"letter-spacing='1' fill='#5b6b82'>{esc(title.upper())}</text>")
        y += PKG_GAP
    bottom = y + 10
    height = bottom + 40

    boundary = (f"<rect x='{BOUND_X}' y='70' width='{BOUND_W}' height='{bottom - 70}' rx='16' "
                f"fill='#f8fafc' stroke='#334155' stroke-width='2'/>"
                f"<text x='{cx}' y='98' text-anchor='middle' font-size='18' font-weight='700' "
                f"fill='{INK}'>SmartDesk — system boundary</text>")

    def target_y(actor):
        ys = [pos[u] for u in diagram["links"].get(actor, [])]
        return sum(ys) / len(ys)

    left = spread([(a, target_y(a)) for a in diagram["left"]], 160, bottom - 120)
    right = spread([(a, target_y(a)) for a in diagram["right"]], 160, bottom - 120)
    lx, rx = 150, BOUND_X + BOUND_W + 170
    width = rx + 150 if right else BOUND_X + BOUND_W + 80

    lines = []
    for actor, ys in list(left.items()) + list(right.items()):
        is_left = actor in left
        ax = lx + 30 if is_left else rx - 30
        for uc in diagram["links"].get(actor, []):
            ex = cx - ELL_W / 2 if is_left else cx + ELL_W / 2
            lines.append(f"<line x1='{ax}' y1='{ys - 10}' x2='{ex}' y2='{pos[uc]}' "
                         f"stroke='{LINE}' stroke-width='1.6'/>")

    for child, parent in diagram["generalization"]:
        side = left if child in left else right
        x = lx if child in left else rx
        y1, y2 = side[child] - 54, side[parent] + 92
        lines.append(f"<line x1='{x}' y1='{y1}' x2='{x}' y2='{y2 + 16}' stroke='{INK}' stroke-width='2'/>"
                     f"<polygon points='{x},{y2} {x - 11},{y2 + 18} {x + 11},{y2 + 18}' "
                     f"fill='#fff' stroke='{INK}' stroke-width='2'/>")

    ells = []
    for uc, uy in pos.items():
        name = model.USE_CASES[uc][0]
        ai = uc in model.AI_SUPPORTED
        ells.append(
            f"<ellipse cx='{cx}' cy='{uy}' rx='{ELL_W / 2}' ry='{ELL_H / 2}' "
            f"fill='{AI_FILL if ai else ELL_FILL}' stroke='{AI_STROKE if ai else ELL_STROKE}' stroke-width='1.6'/>"
            f"<text x='{cx}' y='{uy - 6}' text-anchor='middle' font-size='13' font-weight='700' "
            f"fill='{AI_STROKE if ai else ELL_STROKE}'>{uc}</text>"
            f"<text x='{cx}' y='{uy + 15}' text-anchor='middle' font-size='16' fill='{INK}'>{esc(name)}</text>")

    for ext, base in diagram["extends"]:
        x = cx + 60
        y1, y2 = pos[ext] - ELL_H / 2, pos[base] + ELL_H / 2
        ells.append(f"<line x1='{x}' y1='{y1}' x2='{x}' y2='{y2 + 9}' stroke='#475569' "
                    f"stroke-width='1.6' stroke-dasharray='5 4'/>"
                    f"<polyline points='{x - 6},{y2 + 11} {x},{y2 + 1} {x + 6},{y2 + 11}' fill='none' "
                    f"stroke='#475569' stroke-width='1.6'/>"
                    f"<text x='{x + 12}' y='{(y1 + y2) / 2 + 5}' font-size='13' font-style='italic' "
                    f"fill='#475569'>«extend»</text>")

    actors = "".join(actor_svg(lx, y, a) for a, y in left.items())
    actors += "".join(actor_svg(rx, y, a, secondary=(a == "AI Provider")) for a, y in right.items())

    legend = ""
    if any(u in model.AI_SUPPORTED for u in pos):
        legend = (f"<ellipse cx='{BOUND_X + 40}' cy='{height - 22}' rx='16' ry='9' fill='{AI_FILL}' "
                  f"stroke='{AI_STROKE}'/><text x='{BOUND_X + 64}' y='{height - 17}' font-size='14' "
                  f"fill='#475569'>AI-assisted use case (AI provider is a secondary actor)</text>")

    title = (f"<text x='{width / 2}' y='44' text-anchor='middle' font-size='26' font-weight='700' "
             f"fill='{INK}'>{esc(diagram['title'])}</text>")
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
           f"viewBox='0 0 {width} {height}'>{title}{boundary}{''.join(parts)}{''.join(lines)}"
           f"{''.join(ells)}{actors}{legend}</svg>")
    return render_html(svg_page(svg, width, height), OUT / f"{diagram['file']}.png", width, height)


if __name__ == "__main__":
    covered = {u for d in model.UC_DIAGRAMS for _, ucs in d["packages"] for u in ucs}
    missing = sorted(set(model.USE_CASES) - covered)
    assert not missing, f"use cases missing from diagrams: {missing}"
    for d in model.UC_DIAGRAMS:
        print(build(d))
