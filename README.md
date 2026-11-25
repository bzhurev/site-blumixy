# blumixy.store

Static site for blumixy, served by GitHub Pages at https://blumixy.store (see `CNAME`).

## Editing

All page text lives in `tools/build.py` (English and Ukrainian side by side). Do not edit the generated `.html` files by hand: they are overwritten on every build.

```bash
python3 tools/build.py   # rebuild all pages, feeds, sitemap, robots.txt, CNAME
python3 tools/brand.py   # optional: regenerate logo, favicons, OG images and press kit (needs rsvg-convert + Playwright)
python3 -m http.server   # preview at http://localhost:8000
```

Settings at the top of `tools/build.py`:

- `DOMAIN` — site address used in canonical links, Open Graph, feeds and sitemap
- `EMAIL` — contact address shown everywhere
- `FORM_ENDPOINT` — set a Formspree (or similar) URL to turn on the subscribe form; while empty, the button opens the visitor's mail app
- `CF_BEACON` — Cloudflare Web Analytics token

To add a news post, add an entry to `POSTS` and rebuild.

## Design

- Colours: ink `#1b1a3a`, paper `#f6f5ff`, violet `#5a64ff`, lavender `#9b6bff`, sun `#ffc94d`
- Type: Unbounded (headings) and Onest (text), self-hosted in `assets/fonts` under the SIL Open Font License
- Styles: `assets/site.css`
