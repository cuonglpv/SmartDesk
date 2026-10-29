"""Render the Relume-style sitemap (page cards -> functional sections)."""

from pathlib import Path

from PIL import Image, ImageChops

from common import DOCS, FONT_FAMILY, esc, render_html, tint
import model

OUT = DOCS / "images" / "relume"
BG = "#f1f1ef"
COLORS = dict(model.SITEMAP_GROUPS)

CSS = f"""
*{{box-sizing:border-box}}
body{{margin:0;background:{BG};font-family:{FONT_FAMILY};color:#18181b;padding:48px 40px 60px}}
.wrap{{display:inline-flex;flex-direction:column;align-items:center}}
h1{{font-size:30px;margin:0 0 4px;letter-spacing:-.5px}}
.sub{{color:#71717a;font-size:15px;margin:0 0 30px}}
.root{{background:#18181b;color:#fff;border-radius:12px;padding:14px 28px;font-weight:700;font-size:19px;
      position:relative;display:flex;gap:10px;align-items:center}}
.root small{{font-weight:500;opacity:.7;font-size:13px}}
.root::after{{content:'';position:absolute;left:50%;top:100%;height:30px;border-left:2px solid #a1a1aa}}
.cols{{display:flex;gap:22px;margin-top:30px;align-items:flex-start}}
.col{{position:relative;padding-top:30px;display:flex;flex-direction:column;align-items:center}}
.col::before{{content:'';position:absolute;top:0;left:50%;height:30px;border-left:2px solid #a1a1aa}}
.col::after{{content:'';position:absolute;top:0;left:-11px;right:-11px;border-top:2px solid #a1a1aa}}
.col:first-child::after{{left:50%}} .col:last-child::after{{right:50%}}
.col:only-child::after{{display:none}}
.child{{position:relative;margin-top:30px}}
.child::before{{content:'';position:absolute;top:-30px;left:50%;height:30px;border-left:2px dashed #a1a1aa}}
.card{{width:330px;background:#fff;border-radius:12px;border:1px solid #e4e4e7;
      box-shadow:0 1px 2px rgba(0,0,0,.05),0 6px 18px rgba(0,0,0,.04);overflow:hidden}}
.head{{padding:13px 15px 11px;border-top:5px solid var(--c)}}
.head .row{{display:flex;justify-content:space-between;align-items:baseline;gap:8px}}
.head b{{font-size:17px}}
.id{{font-size:11.5px;font-weight:700;color:var(--c);background:var(--t);padding:2px 7px;border-radius:20px;white-space:nowrap}}
.meta{{font-size:12px;color:#71717a;margin-top:5px;font-family:Consolas,monospace}}
.roles{{font-size:12px;color:#52525b;margin-top:3px}}
.secs{{padding:4px 10px 10px;display:flex;flex-direction:column;gap:7px}}
.sec{{background:#f7f7f8;border:1px solid #ececef;border-radius:8px;padding:8px 10px}}
.sec b{{display:block;font-size:13.5px;margin-bottom:2px}}
.sec span{{font-size:12.5px;color:#52525b;line-height:1.4}}
.ucs{{padding:0 15px 12px;font-size:11.5px;color:#71717a}}
.grp{{width:250px;background:#fff;border-radius:12px;border:1px solid #e4e4e7;overflow:hidden}}
.grp .head b{{font-size:16px}}
.pages{{padding:6px 10px 12px;display:flex;flex-direction:column;gap:6px}}
.pg{{background:#f7f7f8;border:1px solid #ececef;border-radius:8px;padding:7px 10px;font-size:13.5px;
     display:flex;justify-content:space-between;gap:6px}}
.pg.sub{{margin-left:18px;margin-bottom:0}}
.pg em{{white-space:nowrap;font-style:normal;color:#a1a1aa;font-size:12px}}
.legend{{margin-top:28px;font-size:13px;color:#71717a}}
"""


def page_card(scr):
    c = COLORS[scr["group"]]
    secs = "".join(f"<div class='sec'><b>{esc(n)}</b><span>{esc(d)}</span></div>"
                   for n, d in scr["sections"])
    ucs = ", ".join(scr["ucs"]) or "Cross-cutting"
    return (f"<div class='card' style='--c:{c};--t:{tint(c, .12)}'>"
            f"<div class='head'><div class='row'><b>{esc(scr['name'])}</b>"
            f"<span class='id'>{scr['id']}</span></div>"
            f"<div class='meta'>{esc(scr['route'])}</div>"
            f"<div class='roles'>{esc(scr['roles'])}</div></div>"
            f"<div class='secs'>{secs}</div><div class='ucs'>Use cases: {ucs}</div></div>")


def trim(png):
    im = Image.open(png).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((2, 2)))
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        pad = 60
        im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad),
                      min(im.width, box[2] + pad), min(im.height, box[3] + pad)))
    im.save(png, optimize=True)
    return png


def group_page(group, slug):
    screens = [s for s in model.SCREENS if s["group"] == group]
    tops = [s for s in screens if s["id"] not in model.SITEMAP_PARENT]
    by_parent = {}
    for s in screens:
        p = model.SITEMAP_PARENT.get(s["id"])
        if p:
            by_parent.setdefault(p, []).append(s)

    def column(s):
        html = page_card(s)
        for child in by_parent.get(s["id"], []):
            html += f"<div class='child'>{column(child)}</div>"
        return html

    cols = "".join(f"<div class='col'>{column(s)}</div>" for s in tops)
    c = COLORS[group]
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"<div class='wrap'><h1>SmartDesk — {esc(group)}</h1>"
            f"<p class='sub'>Relume-style sitemap · each page card lists its functional sections</p>"
            f"<div class='root' style='background:{c}'>{esc(group)}<small>{len(screens)} pages</small></div>"
            f"<div class='cols'>{cols}</div>"
            f"<div class='legend'>Solid line: navigation item · Dashed line: opened from the parent page (detail / sub-page)</div>"
            f"</div></body></html>")
    width = len(tops) * 352 + 100
    out = render_html(html, OUT / f"sitemap-{slug}.png", width, 2600)
    return trim(out)


def overview():
    cols = ""
    for group, c in model.SITEMAP_GROUPS:
        screens = [s for s in model.SCREENS if s["group"] == group]
        pages = "".join(
            f"<div class='pg{' sub' if s['id'] in model.SITEMAP_PARENT else ''}'>"
            f"<span>{esc(s['name'])}</span><em>{s['id']}</em></div>" for s in screens)
        cols += (f"<div class='col'><div class='grp' style='--c:{c}'>"
                 f"<div class='head'><b>{esc(group)}</b></div><div class='pages'>{pages}</div></div></div>")
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"<div class='wrap'><h1>SmartDesk — Sitemap overview</h1>"
            f"<p class='sub'>{len(model.SCREENS)} pages in 5 role-based areas · indented pages open from the page above</p>"
            f"<div class='root'>SmartDesk<small>AI-assisted IT Helpdesk SaaS</small></div>"
            f"<div class='cols'>{cols}</div></div></body></html>")
    out = render_html(html, OUT / "sitemap-overview.png", 5 * 272 + 100, 1400)
    return trim(out)


if __name__ == "__main__":
    ucs_on_screens = {u for s in model.SCREENS for u in s["ucs"]}
    missing = sorted(set(model.USE_CASES) - ucs_on_screens)
    assert not missing, f"use cases without a screen: {missing}"
    print(overview())
    for group, _ in model.SITEMAP_GROUPS:
        print(group_page(group, group.lower().replace(" ", "-")))
