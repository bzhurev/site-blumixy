#!/usr/bin/env python3
"""Regenerate logo, favicons, OG images and press images.

Needs: rsvg-convert and Python Playwright with Chromium.
Run from the repo root:  python3 tools/brand.py
"""
import subprocess
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FONTS = (ROOT / "assets/fonts").as_uri()

VIOLET, LAVENDER, SUN, INK, PAPER = "#5a64ff", "#9b6bff", "#ffc94d", "#1b1a3a", "#f6f5ff"


def mark(x=0, y=0, s=48, gid="g"):
    """Mark drawn in a 48-unit box, scaled to s and placed at x,y."""
    k = s / 48
    return (f'<g transform="translate({x} {y}) scale({k})">'
            f'<g fill="url(#{gid})"><rect x="2" y="2" width="16" height="16" rx="5"/><rect x="30" y="2" width="16" height="16" rx="5"/>'
            f'<rect x="2" y="30" width="16" height="16" rx="5"/><rect x="30" y="30" width="16" height="16" rx="5"/></g>'
            f'<rect x="16" y="16" width="16" height="16" rx="5" fill="{SUN}"/></g>')


def grad(gid="g"):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{LAVENDER}"/></linearGradient></defs>')


def svg(w, h, inner):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{grad()}{inner}</svg>\n'


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def png_from_svg(src, rel, size):
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-o", str(ROOT / rel), str(src)], check=True)


# --- vector marks
logo = write("logo.svg", svg(256, 256, mark(16, 16, 224)))
write("press/logo.svg", logo.read_text())
fav = write("favicon.svg", svg(64, 64, f'<rect width="64" height="64" rx="14" fill="#fff"/>' + mark(6, 6, 52)))
icon = write("/tmp/blumixy-icon.svg", svg(1024, 1024, f'<rect width="1024" height="1024" fill="{INK}"/>' + mark(232, 232, 560)))

png_from_svg(fav, "favicon-32.png", 32)
for s in (120, 152, 180):
    png_from_svg(icon, f"apple-touch-icon-{s}x{s}.png", s)
png_from_svg(icon, "press/app-icon-1024.png", 1024)
png_from_svg(icon, "press/social-avatar-1024.png", 1024)
png_from_svg(logo, "press/logo-1024.png", 1024)

# --- raster pieces with type, rendered in Chromium so the brand fonts are used
CSS = f"""
@font-face{{font-family:U;src:url({FONTS}/unbounded-latin-wght-normal.woff2) format('woff2');font-weight:200 900}}
@font-face{{font-family:O;src:url({FONTS}/onest-latin-wght-normal.woff2) format('woff2');font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
body{{width:var(--w);height:var(--h);background:{PAPER};color:{INK};font-family:O;overflow:hidden;position:relative}}
.word{{font:600 var(--fs)/1 U;letter-spacing:-.04em}}
.tag{{font:500 var(--ts)/1.3 O;color:#4a4870}}
.row{{display:flex;align-items:center;gap:var(--gap)}}
.tiles{{position:absolute;display:grid;grid-template-columns:repeat(4,var(--t));gap:calc(var(--t)*.18)}}
.tiles i{{width:var(--t);height:var(--t);border-radius:calc(var(--t)*.26);background:#e2e0f7}}
.tiles i.v{{background:linear-gradient(145deg,{VIOLET},{LAVENDER})}}
.tiles i.s{{background:{SUN}}}
"""
MARK_SVG = svg(48, 48, mark()).replace('width="48" height="48"', 'width="100%" height="100%"')


def tiles(pattern):
    return "".join(f'<i class="{c}"></i>' for c in pattern)


PIECES = {
    "og-cover.png": (1200, 630, f"""
<div style="position:absolute;left:84px;top:96px">
  <div class="row" style="--gap:22px"><div style="width:84px">{MARK_SVG}</div><div class="word" style="--fs:76px">blumixy</div></div>
  <div class="word" style="--fs:46px;margin-top:72px;max-width:640px;line-height:1.12;letter-spacing:-.03em">AI software, integrations and games</div>
  <div class="tag" style="--ts:26px;margin-top:28px">blumixy.store</div>
</div>
<div class="tiles" style="--t:92px;right:72px;top:118px">{tiles(['v','','v','','','v','s','v','v','','v','','','v','',''])}</div>"""),
    "news-og.png": (1200, 630, f"""
<div style="position:absolute;left:84px;top:96px">
  <div class="row" style="--gap:18px"><div style="width:60px">{MARK_SVG}</div><div class="word" style="--fs:44px">blumixy news</div></div>
  <div class="word" style="--fs:58px;margin-top:84px;max-width:620px;line-height:1.1;letter-spacing:-.03em">Releases, updates and devlogs</div>
  <div class="tag" style="--ts:26px;margin-top:28px">blumixy.store/news</div>
</div>
<div class="tiles" style="--t:92px;right:72px;top:118px">{tiles(['','v','','','v','v','s','','','s','s','v','','','v',''])}</div>"""),
    "news/retsepty-og.png": (1200, 630, f"""
<div style="position:absolute;inset:0;background:#1b1a3a"></div>
<div style="position:absolute;left:84px;top:92px;color:#fff">
  <div class="row" style="--gap:16px"><div style="width:52px">{MARK_SVG}</div><div class="word" style="--fs:34px;color:#fff">blumixy</div></div>
  <div style="display:inline-block;margin-top:64px;padding:8px 18px;border-radius:999px;background:#ffc94d;color:#1b1a3a;font:600 24px O">Out now on Android</div>
  <div class="word" style="--fs:96px;margin-top:26px;color:#fff">Retsepty</div>
  <div class="tag" style="--ts:30px;margin-top:22px;color:#c9c7ee;max-width:560px">A recipe book that fills itself</div>
</div>
<div style="position:absolute;right:84px;top:118px;width:390px;background:#fff;border-radius:30px;padding:34px 34px 28px;color:#1b1a3a">
  <i style="position:absolute;right:28px;top:28px;width:38px;height:38px;border-radius:11px;background:#ffc94d"></i>
  <div class="word" style="--fs:30px;line-height:1.2;letter-spacing:-.02em;padding-right:52px">Creamy mushroom pasta</div>
  <div style="margin-top:24px;display:grid;gap:14px;font:500 24px O">
    <div style="display:flex;gap:14px;align-items:center"><i style="width:14px;height:14px;border-radius:4px;background:linear-gradient(145deg,#5a64ff,#9b6bff)"></i>400 g pasta</div>
    <div style="display:flex;gap:14px;align-items:center"><i style="width:14px;height:14px;border-radius:4px;background:linear-gradient(145deg,#5a64ff,#9b6bff)"></i>300 g mushrooms</div>
    <div style="display:flex;gap:14px;align-items:center"><i style="width:14px;height:14px;border-radius:4px;background:linear-gradient(145deg,#5a64ff,#9b6bff)"></i>200 ml cream</div>
  </div>
  <div class="tag" style="--ts:21px;margin-top:24px">4 servings, 610 kcal each</div>
</div>"""),
    "press/twitter-header-1500x500.png": (1500, 500, f"""
<div class="tiles" style="--t:70px;right:90px;top:70px">{tiles(['v','','v','','','s','','v','v','','v','s','','v','',''])}</div>
<div style="position:absolute;left:520px;bottom:80px" class="tag"><span style="--ts:30px;font-size:30px">AI software, integrations and games</span></div>"""),
    "press/youtube-banner-2560x1440.png": (2560, 1440, f"""
<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:1546px;height:423px;display:flex;align-items:center;justify-content:space-between">
  <div><div class="row" style="--gap:30px"><div style="width:120px">{MARK_SVG}</div><div class="word" style="--fs:110px">blumixy</div></div>
  <div class="tag" style="--ts:40px;margin-top:30px">AI software, integrations and games</div></div>
  <div class="tiles" style="--t:78px;position:static">{tiles(['v','','v','','','s','','v','v','','v','','','v','','s'])}</div>
</div>"""),
}

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for rel, (w, h, body) in PIECES.items():
        pg = b.new_page(viewport={"width": w, "height": h})
        tmp = ROOT / "assets/_render.html"
        tmp.write_text(f"<html><head><style>{CSS}</style></head><body style='--w:{w}px;--h:{h}px'>{body}</body></html>")
        pg.goto(tmp.as_uri())
        pg.evaluate("document.fonts.ready.then(() => document.fonts.size)")
        tmp.unlink()
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(ROOT / rel))
        pg.close()
    b.close()

# --- press kit zip
with zipfile.ZipFile(ROOT / "press/Blumixy-PressKit.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in ["logo.svg", "logo-1024.png", "app-icon-1024.png", "social-avatar-1024.png",
              "twitter-header-1500x500.png", "youtube-banner-2560x1440.png"]:
        z.write(ROOT / "press" / f, f)
    z.writestr("README.txt", "blumixy press kit — https://blumixy.store/press/\n"
                             "Colours: violet #5a64ff, lavender #9b6bff, sun #ffc94d, ink #1b1a3a, paper #f6f5ff\n"
                             "Typefaces: Unbounded (display), Onest (text)\n")
print("brand assets written")
