#!/usr/bin/env python3
"""Static site generator for blumixy.store.

Run from the repo root:  python3 tools/build.py
It rewrites every HTML page, feed and sitemap in the repo root from the
content below. Edit text here, not in the generated .html files.
"""
from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- settings
DOMAIN = "https://blumixy.store"
EMAIL = "contact@blumixy.org"          # change here if the mailbox moves
FORM_ENDPOINT = ""                     # e.g. "https://formspree.io/f/abcd1234"; empty = mailto fallback
BING_VERIFY = "66F88F1686AAF6DE5A6E77250C82DC7F"  # Bing Webmaster Tools meta tag
CF_BEACON = "a2aeabb7cbf24a51815b19be0e10a6eb"  # Cloudflare Web Analytics token
BUILD_DATE = date(2026, 11, 25)
SOCIAL = [
    ("Instagram", "https://www.instagram.com/blumixy_official/"),
    ("TikTok", "https://www.tiktok.com/@blumixy_official"),
    ("YouTube", "https://www.youtube.com/channel/UC0BAkExF7BuQo8fXEvK0RBw"),
    ("X", "https://x.com/blumixyofficial"),
]

LANGS = ("en", "uk")
PREFIX = {"en": "", "uk": "/uk"}
LOCALE = {"en": "en_US", "uk": "uk_UA"}

e = html.escape

# ---------------------------------------------------------------- strings
T = {
    "en": {
        "nav": [("about", "About"), ("services", "Services"), ("news", "News"), ("press", "Press")],
        "skip": "Skip to content",
        "contact_us": "Email us",
        "see_services": "See services",
        "read_more": "Learn more",
        "foot_studio": "Product studio for AI software, integrations and casual games.",
        "foot_company": "Company", "foot_follow": "Follow", "foot_legal": "Legal",
        "privacy": "Privacy", "terms": "Terms", "subscribe": "Get updates",
        "rights": "All rights reserved.",
        "lang_name": "English",
        "months": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
        "date_fmt": "{m} {d}, {y}",
        "all_news": "All news",
    },
    "uk": {
        "nav": [("about", "Про нас"), ("services", "Послуги"), ("news", "Новини"), ("press", "Преса")],
        "skip": "Перейти до змісту",
        "contact_us": "Написати нам",
        "see_services": "Наші послуги",
        "read_more": "Детальніше",
        "foot_studio": "Продуктова студія: ПЗ зі ШІ, інтеграції та казуальні ігри.",
        "foot_company": "Студія", "foot_follow": "Соцмережі", "foot_legal": "Документи",
        "privacy": "Конфіденційність", "terms": "Умови", "subscribe": "Отримувати новини",
        "rights": "Усі права захищено.",
        "lang_name": "Українська",
        "months": ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня",
                   "серпня", "вересня", "жовтня", "листопада", "грудня"],
        "date_fmt": "{d} {m} {y}",
        "all_news": "Усі новини",
    },
}

SERVICES = {
    "en": [
        ("ai", "AI & automation",
         "Assistants and agents that do real work inside your tools, not demos that stay demos.",
         ["Chat assistants and agents wired into your systems",
          "Retrieval over your own documents (RAG)",
          "Workflow automation: from prototype to pilot to production"]),
        ("software", "Software delivery",
         "Web and mobile products with a lean stack and a short path from idea to release.",
         ["Web and mobile apps, from MVP to v1",
          "Internal tools and dashboards",
          "Data pipelines and integrations between services"]),
        ("ux", "UX/UI & release",
         "Interfaces people understand on the first try, shipped with monitoring in place.",
         ["Rapid prototyping and usability reviews",
          "Release, observability and iteration after launch"]),
    ],
    "uk": [
        ("ai", "ШІ та автоматизація",
         "Асистенти й агенти, які виконують реальну роботу у ваших інструментах, а не лишаються демо.",
         ["Чат-асистенти та агенти, інтегровані у ваші системи",
          "Пошук і відповіді за вашими документами (RAG)",
          "Автоматизація процесів: прототип, пілот, продакшн"]),
        ("software", "Розробка ПЗ",
         "Веб- і мобільні продукти на легкому стеку з коротким шляхом від ідеї до релізу.",
         ["Веб- і мобільні застосунки, від MVP до v1",
          "Внутрішні інструменти та дашборди",
          "Пайплайни даних та інтеграції між сервісами"]),
        ("ux", "UX/UI та реліз",
         "Інтерфейси, зрозумілі з першого разу, і реліз із моніторингом з першого дня.",
         ["Швидке прототипування та юзабіліті-рев’ю",
          "Реліз, спостережуваність та ітерації після запуску"]),
    ],
}
GLYPH = {  # which cells of a 2x2 glyph are lit
    "ai": ["on", "", "", "on"],
    "software": ["on", "on", "", "on"],
    "ux": ["on", "", "on", "on"],
    "games": ["on", "on", "on", "sun"],
}

STEPS = {
    "en": [("Scope", "One call to agree what success looks like and what we leave out."),
           ("Prototype", "A working slice in days, tested on real data or real users."),
           ("Pilot", "Running with a small group, measured against the agreed goal."),
           ("Production", "Hardened, monitored and handed over, or run by us.")],
    "uk": [("Обсяг", "Одна зустріч, щоб домовитися, що вважаємо успіхом і що не робимо."),
           ("Прототип", "Робочий фрагмент за кілька днів, перевірений на реальних даних."),
           ("Пілот", "Запуск для невеликої групи з вимірюванням результату."),
           ("Продакшн", "Стабільна версія з моніторингом: передаємо вам або супроводжуємо.")],
}

POSTS = [
    {
        "slug": "retsepty-launch",
        "date": date(2026, 11, 27),
        "og": "/news/retsepty-og.png",
        "hero": True,
        "app": {"icon": "/assets/apps/retsepty-icon-512.png",
                "en": ("Retsepty", "Coming soon to Android"),
                "uk": ("Рецепти", "Незабаром на Android")},
        "en": {
            "title": "Retsepty: your recipe book that fills itself",
            "summary": "Recipes from TikTok, Instagram and photos in one book, with a shopping list that writes itself. Coming soon to Android.",
            "lead": "Recipes from TikTok, Instagram and photos in one book. The shopping list writes itself.",
            "blocks": [
                ("p", "Saw a tasty recipe on TikTok or Reels? Tap Share, pick Retsepty, and in a few seconds it’s in your book with ingredients, step-by-step instructions and nutrition. No screenshots, no notes, no hunting for “that video”."),
                ("h2", "How it works"),
                ("steps", [
                    ("Share", "From TikTok, Instagram, YouTube or any cooking site, or take a photo of a cookbook page."),
                    ("Get a recipe", "AI listens to the video and reads the caption, then lays out ingredients, steps and nutrition."),
                    ("Cook", "Add everything to your shopping list in one tap and follow the steps in cooking mode."),
                ]),
                ("h2", "Everything in one app"),
                ("featurelist", [
                    ("ai", "Save recipes from anywhere", [
                        "TikTok, Instagram Reels, YouTube: AI listens to the video and reads the caption",
                        "Any cooking website",
                        "A photo of a cookbook page or grandma’s handwritten recipe, up to 6 pages per recipe",
                        "A photo of a finished dish: the app recognises it and suggests a classic recipe",
                        "Plain text from your notes or a messenger"]),
                    ("software", "A recipe card that works for you", [
                        "Tap − or + to change servings, and every ingredient recalculates",
                        "Calories, protein, fat and carbs per serving",
                        "Favourites and search by name or ingredient: “potato” finds everything with potatoes"]),
                    ("ux", "A smart shopping list", [
                        "Add all ingredients in one tap",
                        "The same product from several recipes adds up into one line",
                        "Each item shows which dish it’s for",
                        "Salt, water and other things you already have don’t clutter the list"]),
                    ("games", "Cooking mode", [
                        "Big steps that are easy to read from the stove",
                        "A timer for each step, and several can run at once",
                        "The screen stays on while you cook"]),
                    ("ai", "Family", [
                        "Share your family code to get one recipe book and one shopping list for everyone",
                        "One adds a recipe and the other sees it; one buys the milk and the other sees it’s already in the basket"]),
                ]),
                ("cta", ("Be the first to try it", "Retsepty is coming soon to Android, with iOS to follow. Follow us to hear about the launch and early access first.")),
            ],
        },
        "uk": {
            "title": "Рецепти: ваша книга рецептів, яка наповнюється сама",
            "summary": "Рецепти з TikTok, Instagram і фото в одній книзі, а список покупок складеться сам. Незабаром на Android.",
            "lead": "Рецепти з TikTok, Instagram і фото в одній книзі. Список покупок складеться сам.",
            "blocks": [
                ("p", "Побачили смачний рецепт у TikTok чи Reels? Натисніть «Поділитися», оберіть «Рецепти», і за кілька секунд він уже у вашій книзі: з інгредієнтами, покроковими інструкціями та КБЖВ. Без скриншотів, нотаток і пошуку «того відео»."),
                ("h2", "Як це працює"),
                ("steps", [
                    ("Поділіться", "З TikTok, Instagram, YouTube чи будь-якого кулінарного сайту, або сфотографуйте сторінку книги."),
                    ("Отримайте рецепт", "ШІ слухає відео й читає опис, а потім розкладає все на інгредієнти, кроки та КБЖВ."),
                    ("Готуйте", "Додайте все до списку покупок одним натиском і готуйте в режимі готування."),
                ]),
                ("h2", "Усе в одному застосунку"),
                ("featurelist", [
                    ("ai", "Збереження рецептів звідусіль", [
                        "TikTok, Instagram Reels, YouTube: ШІ слухає відео й читає опис",
                        "Будь-які кулінарні сайти",
                        "Фото сторінки з кулінарної книги чи бабусиного рукописного рецепта (до 6 сторінок одного рецепта)",
                        "Фото готової страви: застосунок упізнає її й запропонує класичний рецепт",
                        "Просто текст з нотаток чи месенджера"]),
                    ("software", "Зручна картка рецепта", [
                        "Кількість порцій −/+, і всі інгредієнти перераховуються автоматично",
                        "Калорії, білки, жири й вуглеводи на порцію",
                        "Обране й пошук за назвою або продуктом: «картопля» знайде все з картоплею"]),
                    ("ux", "Розумний список покупок", [
                        "Інгредієнти додаються одним натиском",
                        "Однакові продукти з кількох рецептів сумуються в один рядок",
                        "Біля кожного продукту видно, для якої він страви",
                        "Сіль, вода та інше, що зазвичай є вдома, не захаращують список"]),
                    ("games", "Режим готування", [
                        "Великі кроки, які зручно читати біля плити",
                        "Таймери для кожного етапу, кілька можуть працювати одночасно",
                        "Екран не гасне, поки ви готуєте"]),
                    ("ai", "Сім’я", [
                        "Поділіться кодом сім’ї, і у вас буде спільна книга рецептів і один список покупок на всіх",
                        "Один додав рецепт, інший уже бачить його; один купив молоко, інший бачить, що воно вже в кошику"]),
                ]),
                ("cta", ("Спробуйте першими", "«Рецепти» незабаром вийдуть на Android, а згодом і на iOS. Стежте за нами, щоб першими дізнатися про запуск і ранній доступ.")),
            ],
        },
    },
]


# ---------------------------------------------------------------- helpers
def url(lang: str, key: str) -> str:
    p = PREFIX[lang]
    return {
        "home": f"{p}/",
        "about": f"{p}/about.html",
        "services": f"{p}/services.html",
        "news": f"{p}/news/",
        "press": f"{p}/press/",
        "subscribe": f"{p}/subscribe.html",
        "privacy": f"{p}/privacy.html",
        "terms": f"{p}/terms.html",
    }.get(key) or f"{p}/news/{key}.html"


def fmt_date(lang: str, d: date) -> str:
    t = T[lang]
    return t["date_fmt"].format(m=t["months"][d.month - 1], d=d.day, y=d.year)


def mark_svg(size: int = 30) -> str:
    """The blumixy mark: four violet tiles merged around a sun-coloured core."""
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" aria-hidden="true">'
            '<defs><linearGradient id="bm" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#5a64ff"/><stop offset="1" stop-color="#9b6bff"/></linearGradient></defs>'
            '<g fill="url(#bm)"><rect x="2" y="2" width="16" height="16" rx="5"/><rect x="30" y="2" width="16" height="16" rx="5"/>'
            '<rect x="2" y="30" width="16" height="16" rx="5"/><rect x="30" y="30" width="16" height="16" rx="5"/></g>'
            '<rect x="16" y="16" width="16" height="16" rx="5" fill="#ffc94d"/></svg>')


def glyph(kind: str) -> str:
    cells = "".join(f'<i class="{c}"></i>' for c in GLYPH[kind])
    return f'<div class="glyph" aria-hidden="true">{cells}</div>'


APP_CARD = {
    "en": ("TikTok link", "Cookbook photo", "Creamy mushroom pasta", ["400 g pasta", "300 g mushrooms", "200 ml cream"], "4 servings · 610 kcal"),
    "uk": ("Посилання з TikTok", "Фото з книги", "Паста з грибами у вершках", ["400 г пасти", "300 г печериць", "200 мл вершків"], "4 порції · 610 ккал"),
}


def app_card(lang: str) -> str:
    """Small illustration for the home spotlight: inputs merge into one recipe card."""
    a, b, title, items, meta = APP_CARD[lang]
    li = "".join(f"<li>{e(i)}</li>" for i in items)
    return (f'<div class="app-demo" aria-hidden="true"><div class="src"><span>{e(a)}</span><span>{e(b)}</span></div>'
            f'<div class="card"><i class="core"></i><b>{e(title)}</b><ul>{li}</ul><small>{e(meta)}</small></div></div>')


def app_id(p: dict, lang: str) -> str:
    a = p.get("app")
    if not a:
        return ""
    name, status = a[lang]
    return (f'<div class="app-id"><img src="{a["icon"]}" alt="{e(name)}" width="64" height="64">'
            f'<div><b>{e(name)}</b><span class="when">{e(status)}</span></div></div>')


def render_blocks(blocks: list) -> str:
    out = ""
    for kind, val in blocks:
        if kind == "h2":
            out += f"<h2>{e(val)}</h2>"
        elif kind == "p":
            out += f"<p>{e(val)}</p>"
        elif kind == "steps":
            out += '<ol class="steps post-steps">' + "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in val) + "</ol>"
        elif kind == "featurelist":
            out += '<div class="flist">' + "".join(
                f'<section>{glyph(g)}<div><h3>{e(t)}</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul></div></section>'
                for g, t, items in val) + "</div>"
        elif kind == "cta":
            h, ptxt = val
            out += f'<div class="post-cta"><h2>{e(h)}</h2><p>{e(ptxt)}</p>{social_list()}</div>'
        elif kind == "features":
            out += '<div class="features">' + "".join(
                f"<div>{glyph(g)}<h3>{e(t)}</h3><p>{e(d)}</p></div>" for g, t, d in val) + "</div>"
    return out


def social_list() -> str:
    return '<ul class="social">' + "".join(
        f'<li><a href="{u}" rel="me noopener">{n}</a></li>' for n, u in SOCIAL) + "</ul>"


def page(lang: str, key: str, path: str, title: str, desc: str, body: str,
         alt_path: str | None = None, og_image: str = "/og-cover.png",
         og_type: str = "website", extra_ld: dict | None = None) -> str:
    """Wrap page body in the shared shell. `path`/`alt_path` are the EN/UK twins."""
    t = T[lang]
    other = "uk" if lang == "en" else "en"
    paths = {lang: path, other: alt_path} if alt_path else {lang: path}
    en_path = paths.get("en", path)
    hreflang = ""
    if alt_path:
        hreflang = (f'<link rel="alternate" hreflang="en" href="{DOMAIN}{paths["en"]}">\n'
                    f'<link rel="alternate" hreflang="uk" href="{DOMAIN}{paths["uk"]}">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{en_path}">\n')
    nav = "".join(
        f'<a href="{url(lang, k)}"{" aria-current=\"page\"" if k == key else ""}>{e(label)}</a>'
        for k, label in t["nav"])
    lang_switch = ""
    for lg, label in (("en", "EN"), ("uk", "UA")):
        target = paths.get(lg) or url(lg, "home")
        cur = ' aria-current="true"' if lg == lang else ""
        lang_switch += f'<a href="{target}" hreflang="{lg}" lang="{lg}"{cur} title="{T[lg]["lang_name"]}">{label}</a>'

    org = {
        "@context": "https://schema.org", "@type": "Organization", "name": "blumixy",
        "url": f"{DOMAIN}/", "logo": f"{DOMAIN}/press/logo-1024.png", "email": EMAIL,
        "sameAs": [u for _, u in SOCIAL],
    }
    ld = f'<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>'
    if extra_ld:
        ld += f'\n<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>'
    beacon = (f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
              f'data-cf-beacon=\'{{"token":"{CF_BEACON}"}}\'></script>') if CF_BEACON else ""
    full_title = title if key == "home" else f"{title} — blumixy"
    verify = f'\n<meta name="msvalidate.01" content="{BING_VERIFY}">' if BING_VERIFY and key == "home" else ""

    foot_company = "".join(f'<li><a href="{url(lang, k)}">{e(l)}</a></li>' for k, l in t["nav"])
    foot_company += f'<li><a href="{url(lang, "subscribe")}">{e(t["subscribe"])}</a></li>'
    foot_follow = "".join(f'<li><a href="{u}" rel="me noopener">{n}</a></li>' for n, u in SOCIAL)

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{DOMAIN}{path}">
{hreflang}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon-180x180.png" sizes="180x180">
<link rel="alternate" type="application/rss+xml" title="blumixy — News" href="{DOMAIN}/news/rss.xml">
<meta name="theme-color" content="#f6f5ff">{verify}
<meta property="og:site_name" content="blumixy">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta property="og:image" content="{DOMAIN}{og_image}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{LOCALE[lang]}"><meta property="og:locale:alternate" content="{LOCALE[other]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@blumixyofficial">
<link rel="preload" href="/assets/fonts/unbounded-{'cyrillic' if lang == 'uk' else 'latin'}-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
{beacon}
{ld}
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
<header class="site-head">
  <div class="wrap head-row">
    <a class="brand" href="{url(lang, 'home')}" aria-label="blumixy">{mark_svg()}<span>blumixy</span></a>
    <nav class="menu" aria-label="Main">{nav}</nav>
    <div class="lang">{lang_switch}</div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="{url(lang, 'home')}" aria-label="blumixy">{mark_svg(26)}<span>blumixy</span></a>
        <p class="muted" style="margin-top:14px;max-width:22em">{e(t["foot_studio"])}</p>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
      <div><h2>{e(t["foot_company"])}</h2><ul>{foot_company}</ul></div>
      <div><h2>{e(t["foot_follow"])}</h2><ul>{foot_follow}</ul></div>
      <div><h2>{e(t["foot_legal"])}</h2><ul>
        <li><a href="{url(lang, 'privacy')}">{e(t["privacy"])}</a></li>
        <li><a href="{url(lang, 'terms')}">{e(t["terms"])}</a></li></ul></div>
    </div>
    <p class="foot-note">© 2025–{BUILD_DATE.year} blumixy. {e(t["rights"])}</p>
  </div>
</footer>
<script>
(function(){{var h=document.querySelector('.site-head');function s(){{h.classList.toggle('scrolled',window.scrollY>8)}}addEventListener('scroll',s,{{passive:true}});s();}})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- pages
def home(lang: str) -> str:
    c = {
        "en": dict(
            title="blumixy — AI software, integrations and games",
            desc="blumixy is a product studio building AI-powered software, integrations and casual games.",
            h1="AI software, pragmatic integrations and polished apps",
            lead="We help teams ship fast and clean: AI assistants, workflow automation, web and mobile apps. Games are our own product line.",
            what_h="What we build",
            what_p="Three things, done properly. Every project starts small and earns its next step.",
            games_t="Games", games_p="Cozy casual titles with clean UI and satisfying mechanics. Our first one is almost out.",
            games_li=["Blumixy Puzzle, a merge-and-match for iOS and Android", "Devlogs and playtests in the open"],
            how_h="How a project runs", how_p="Short cycles with a measurable result at the end of each one.",
            spot_when="Coming soon to Android", spot_h="Retsepty",
            spot_p="Recipes from TikTok, Instagram and photos in one book. The shopping list writes itself.",
            contact_h="Have a project in mind?",
            contact_p="Tell us what you want to automate or build.",
            board_label="Animated blumixy tiles merging into the logo",
        ),
        "uk": dict(
            title="blumixy — ПЗ зі ШІ, інтеграції та ігри",
            desc="blumixy — продуктова студія: програмне забезпечення зі ШІ, інтеграції та казуальні ігри.",
            h1="ПЗ зі ШІ, практичні інтеграції та якісні застосунки",
            lead="Допомагаємо командам запускатися швидко й чисто: ШІ-асистенти, автоматизація процесів, веб- і мобільні застосунки. Ігри — наш власний продуктовий напрям.",
            what_h="Що ми робимо",
            what_p="Три напрями, зроблені як слід. Кожен проєкт починається з малого і переходить на наступний етап лише після результату.",
            games_t="Ігри", games_p="Затишні казуальні ігри з чистим інтерфейсом і приємними механіками. Перша майже готова.",
            games_li=["Blumixy Puzzle — merge-and-match для iOS та Android", "Відкриті девлоги та плейтести"],
            how_h="Як іде проєкт", how_p="Короткі цикли з вимірюваним результатом наприкінці кожного.",
            spot_when="Незабаром на Android", spot_h="Рецепти",
            spot_p="Рецепти з TikTok, Instagram і фото в одній книзі. Список покупок складеться сам.",
            contact_h="Маєте задачу?",
            contact_p="Розкажіть, що хочете автоматизувати чи створити.",
            board_label="Анімація: плитки blumixy зливаються в логотип",
        ),
    }[lang]
    t = T[lang]

    cells = "".join(
        f'<span class="cell" style="left:calc(var(--gap) + {x} * (var(--cell) + var(--gap)));top:calc(var(--gap) + {y} * (var(--cell) + var(--gap)))"></span>'
        for y in range(3) for x in range(3))
    # final positions = the mark; data-from = where each tile starts before merging
    tiles = "".join(
        f'<span class="tile" style="--x:{x};--y:{y}" data-from="{fx},{fy}"></span>'
        for (x, y), (fx, fy) in zip([(0, 0), (2, 0), (0, 2), (2, 2)], [(1, 0), (2, 1), (0, 1), (1, 2)]))
    board = (f'<div class="board merged" id="board" role="img" aria-label="{e(c["board_label"])}">{cells}{tiles}'
             f'<span class="tile core" style="--x:1;--y:1"></span></div>')

    offers = ""
    for kind, name, p, items in SERVICES[lang]:
        offers += (f'<article class="offer">{glyph(kind)}<div><h3>{e(name)}</h3><p>{e(p)}</p></div>'
                   f'<ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul></article>')
    offers += (f'<article class="offer">{glyph("games")}<div><h3>{e(c["games_t"])}</h3><p>{e(c["games_p"])}</p></div>'
               f'<ul>{"".join(f"<li>{e(i)}</li>" for i in c["games_li"])}</ul></article>')
    steps = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in STEPS[lang])
    post = POSTS[0]

    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>{e(c["h1"])}</h1>
      <p class="lead">{e(c["lead"])}</p>
      <div class="actions">
        <a class="btn primary" href="mailto:{EMAIL}">{e(t["contact_us"])}</a>
        <a class="btn" href="{url(lang, 'services')}">{e(t["see_services"])}</a>
      </div>
    </div>
    {board}
  </div>
</section>
<script>
(function(){{
  var b=document.getElementById('board');
  if(!b||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var ts=b.querySelectorAll('.tile:not(.core)'),fin=[];
  b.classList.remove('merged');
  ts.forEach(function(t,i){{var f=t.dataset.from.split(',');fin.push([t.style.getPropertyValue('--x'),t.style.getPropertyValue('--y')]);
    t.style.transition='none';t.style.setProperty('--x',f[0]);t.style.setProperty('--y',f[1]);}});
  b.offsetWidth;
  setTimeout(function(){{ts.forEach(function(t,i){{t.style.transition='';t.style.transitionDelay=(i*0.12)+'s';t.style.setProperty('--x',fin[i][0]);t.style.setProperty('--y',fin[i][1]);}});
    b.classList.add('merged');}},350);
}})();
</script>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>{e(c["what_h"])}</h2><p>{e(c["what_p"])}</p></div>
    {offers}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>{e(c["how_h"])}</h2><p>{e(c["how_p"])}</p></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="section" style="border-top:0;padding-top:0">
  <div class="wrap">
    <div class="spot">
      <div>
        <div class="app-id"><img src="{post['app']['icon']}" alt="" width="64" height="64"><span class="when">{e(c["spot_when"])}</span></div>
        <h2>{e(c["spot_h"])}</h2>
        <p>{e(c["spot_p"])}</p>
        <div class="actions"><a class="btn on-dark" href="{url(lang, post['slug'])}">{e(t["read_more"])}</a></div>
      </div>
      {app_card(lang)}
    </div>
  </div>
</section>

<section class="section contact">
  <div class="wrap">
    <h2>{e(c["contact_h"])}</h2>
    <p class="lead" style="margin-top:16px">{e(c["contact_p"])}</p>
    <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
    {social_list()}
  </div>
</section>
"""
    return page(lang, "home", url(lang, "home"), c["title"], c["desc"], body, url("uk" if lang == "en" else "en", "home"))


def about(lang: str) -> str:
    c = {
        "en": dict(title="About", desc="About blumixy: a small product studio for AI software, integrations and games.",
                   h1="About blumixy",
                   lead="We are a small product studio. We design and ship AI-powered software and pragmatic integrations for other teams, and we make our own casual games.",
                   ph="What we believe",
                   p=[("Clarity over noise", "If an interface or a report needs explaining, it isn’t finished yet."),
                      ("Pragmatic engineering", "The simplest stack that does the job, with room to grow when it’s needed."),
                      ("Outcomes over output", "We measure success by what changed for you, not by hours or features shipped.")],
                   wh="How we work",
                   w=["Short cycles with a measurable milestone at the end of each one.",
                      "A lean stack with logging and monitoring from day one.",
                      "Care for performance and UX in everything we ship, from internal tools to games."]),
        "uk": dict(title="Про нас", desc="Про blumixy: невелика продуктова студія — ПЗ зі ШІ, інтеграції та ігри.",
                   h1="Про blumixy",
                   lead="Ми невелика продуктова студія. Проєктуємо та запускаємо ПЗ зі ШІ та практичні інтеграції для інших команд, а також робимо власні казуальні ігри.",
                   ph="У що ми віримо",
                   p=[("Ясність замість шуму", "Якщо інтерфейс чи звіт треба пояснювати, роботу ще не завершено."),
                      ("Прагматична інженерія", "Найпростіший стек, що виконує задачу, із запасом для росту."),
                      ("Результат, а не активність", "Успіх — це те, що змінилося для вас, а не години чи кількість фіч.")],
                   wh="Як ми працюємо",
                   w=["Короткі цикли з вимірюваною віхою наприкінці кожного.",
                      "Легкий стек із логуванням і моніторингом з першого дня.",
                      "Увага до швидкодії та UX у всьому — від внутрішніх інструментів до ігор."]),
    }[lang]
    kinds = ["ai", "software", "games"]
    trio = "".join(f"<div>{glyph(k)}<h3>{e(a)}</h3><p>{e(b)}</p></div>" for k, (a, b) in zip(kinds, c["p"]))
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>{e(c["h1"])}</h1><p class="lead">{e(c["lead"])}</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(c["ph"])}</h2></div>
  <div class="trio">{trio}</div>
</div></section>
<section class="section"><div class="wrap prose">
  <h2 style="margin-top:0">{e(c["wh"])}</h2>
  <ul>{"".join(f"<li>{e(x)}</li>" for x in c["w"])}</ul>
  <div class="actions"><a class="btn primary" href="mailto:{EMAIL}">{e(T[lang]["contact_us"])}</a></div>
</div></section>
"""
    return page(lang, "about", url(lang, "about"), c["title"], c["desc"], body, url("uk" if lang == "en" else "en", "about"))


def services(lang: str) -> str:
    c = {
        "en": dict(title="Services", desc="AI and automation, software delivery, UX/UI and release by blumixy.",
                   h1="Services", lead="From prototype to production: clear scope, a lean stack and quick feedback loops.",
                   how="How a project runs",
                   cta_h="Start with a short call", cta_p="Send us a few lines about the problem. We’ll reply with questions and a rough plan."),
        "uk": dict(title="Послуги", desc="ШІ та автоматизація, розробка ПЗ, UX/UI та реліз від blumixy.",
                   h1="Послуги", lead="Від прототипу до продакшну: чіткий обсяг робіт, легкий стек і швидкий зворотний зв’язок.",
                   how="Як іде проєкт",
                   cta_h="Почнімо з короткої розмови", cta_p="Напишіть кілька рядків про задачу. Ми відповімо питаннями та орієнтовним планом."),
    }[lang]
    offers = "".join(
        f'<article class="offer">{glyph(k)}<div><h3>{e(n)}</h3><p>{e(p)}</p></div>'
        f'<ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul></article>'
        for k, n, p, items in SERVICES[lang])
    steps = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in STEPS[lang])
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>{e(c["h1"])}</h1><p class="lead">{e(c["lead"])}</p>
</div></section>
<section><div class="wrap">{offers}</div></section>
<section class="section" style="border-top:0"><div class="wrap">
  <div class="section-head"><h2>{e(c["how"])}</h2></div>
  <ol class="steps">{steps}</ol>
</div></section>
<section class="section contact"><div class="wrap">
  <h2>{e(c["cta_h"])}</h2><p class="lead" style="margin-top:16px">{e(c["cta_p"])}</p>
  <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
</div></section>
"""
    return page(lang, "services", url(lang, "services"), c["title"], c["desc"], body, url("uk" if lang == "en" else "en", "services"))


def news_index(lang: str) -> str:
    c = {"en": dict(title="News", desc="Company news, releases and devlogs from blumixy.", lead="Company updates, releases and devlogs."),
         "uk": dict(title="Новини", desc="Новини студії, релізи та девлоги blumixy.", lead="Оновлення студії, релізи та девлоги.")}[lang]
    items = "".join(
        f'<li><a href="{url(lang, p["slug"])}"><time datetime="{p["date"].isoformat()}">{fmt_date(lang, p["date"])}</time>'
        f'<div><h3>{e(p[lang]["title"])}</h3><p>{e(p[lang]["summary"])}</p></div></a></li>'
        for p in sorted(POSTS, key=lambda p: p["date"], reverse=True))
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>{e(c["title"])}</h1><p class="lead">{e(c["lead"])}</p>
</div></section>
<section><div class="wrap"><ul class="posts">{items}</ul></div></section>
"""
    return page(lang, "news", url(lang, "news"), c["title"], c["desc"], body, url("uk" if lang == "en" else "en", "news"))


def news_post(lang: str, p: dict) -> str:
    c = p[lang]
    path = url(lang, p["slug"])
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": c["title"],
          "datePublished": p["date"].isoformat(), "dateModified": p["date"].isoformat(), "inLanguage": lang,
          "image": f"{DOMAIN}{p.get('og', '/news-og.png')}",
          "author": {"@type": "Organization", "name": "blumixy"},
          "publisher": {"@type": "Organization", "name": "blumixy",
                        "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/press/logo-1024.png"}},
          "mainEntityOfPage": f"{DOMAIN}{path}"}
    paras = render_blocks(c["blocks"]) if "blocks" in c else "".join(f"<p>{e(x)}</p>" for x in c["body"])
    body = f"""
<article>
<section class="page-head"><div class="wrap{' post-hero' if p.get('hero') else ' prose'}"><div>
  <a class="crumb" href="{url(lang, 'news')}">{e(T[lang]["all_news"])}</a>
  <time class="article-meta" datetime="{p["date"].isoformat()}">{fmt_date(lang, p["date"])}</time>
  {app_id(p, lang)}
  <h1>{e(c["title"])}</h1>
  <p class="lead">{e(c["lead"])}</p>
</div>{app_card(lang) if p.get('hero') else ''}</div></section>
<div class="wrap"><div class="prose post-body">
  {paras}
  {'' if any(k == 'cta' for k, _ in c.get('blocks', [])) else social_list()}
</div></div>
</article>
"""
    return page(lang, "news", path, c["title"], c["summary"], body,
                url("uk" if lang == "en" else "en", p["slug"]), og_image=p.get("og", "/news-og.png"), og_type="article", extra_ld=ld)


def press(lang: str) -> str:
    c = {
        "en": dict(title="Press kit", desc="Press kit: logos, assets and facts about blumixy.",
                   lead="Logos, images and short facts for articles, posts and partner pages.",
                   facts_h="Quick facts", assets_h="Logos and images", boiler_h="About blumixy, in two sentences",
                   f=[("Focus", "AI integrations, software products, automation, casual games"),
                      ("Website", f'<a href="{DOMAIN}/">blumixy.store</a>'),
                      ("Email", f'<a href="mailto:{EMAIL}">{EMAIL}</a>')],
                   dl="Download", zip="Download the full press kit (ZIP)",
                   boiler="blumixy is a product studio designing and shipping AI-powered software and integrations. We combine clean design, pragmatic engineering and measurable outcomes, and make our own casual games."),
        "uk": dict(title="Пресматеріали", desc="Пресматеріали: логотипи, зображення та факти про blumixy.",
                   lead="Логотипи, зображення та короткі факти для статей, публікацій і сторінок партнерів.",
                   facts_h="Коротко", assets_h="Логотипи та зображення", boiler_h="Про blumixy у двох реченнях",
                   f=[("Напрями", "ШІ-інтеграції, програмні продукти, автоматизація, казуальні ігри"),
                      ("Сайт", f'<a href="{DOMAIN}/">blumixy.store</a>'),
                      ("Пошта", f'<a href="mailto:{EMAIL}">{EMAIL}</a>')],
                   dl="Завантажити", zip="Завантажити всі пресматеріали (ZIP)",
                   boiler="blumixy — продуктова студія, що проєктує та запускає ПЗ зі ШІ та інтеграції. Поєднуємо чистий дизайн, прагматичну інженерію та вимірюваний результат, а також робимо власні казуальні ігри."),
    }[lang]
    social = '<a href="{0}" rel="me noopener">{1}</a>'
    facts = "".join(f"<dt>{e(a)}</dt><dd>{b}</dd>" for a, b in c["f"])
    facts += f'<dt>{"Social" if lang == "en" else "Соцмережі"}</dt><dd>{", ".join(social.format(u, n) for n, u in SOCIAL)}</dd>'
    assets = [("logo.svg", "Logo (SVG)"), ("logo-1024.png", "Logo (PNG, 1024)"),
              ("app-icon-1024.png", "App icon (1024)"), ("social-avatar-1024.png", "Social avatar (1024)"),
              ("twitter-header-1500x500.png", "X header (1500×500)"), ("youtube-banner-2560x1440.png", "YouTube banner (2560×1440)")]
    figs = "".join(
        f'<li><figure><img src="/press/{f}" alt="{e(n)}" loading="lazy">'
        f'<figcaption><span>{e(n)}</span><a href="/press/{f}" download>{e(c["dl"])}</a></figcaption></figure></li>'
        for f, n in assets)
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>{e(c["title"])}</h1><p class="lead">{e(c["lead"])}</p>
  <div class="actions"><a class="btn primary" href="/press/Blumixy-PressKit.zip" download>{e(c["zip"])}</a></div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(c["facts_h"])}</h2></div>
  <dl class="facts">{facts}</dl>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(c["assets_h"])}</h2></div>
  <ul class="assets">{figs}</ul>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>{e(c["boiler_h"])}</h2></div>
  <p class="boiler">{e(c["boiler"])}</p>
</div></section>
"""
    return page(lang, "press", url(lang, "press"), c["title"], c["desc"], body, url("uk" if lang == "en" else "en", "press"))


def subscribe(lang: str) -> str:
    c = {
        "en": dict(title="Get updates", desc="Get product and release news from blumixy by email.",
                   lead="Leave your email to hear about releases and playtests. We only write when there is something worth reading.",
                   label="Email address", btn="Subscribe",
                   note="We use your email only to send blumixy updates. Unsubscribe any time by replying “stop”."),
        "uk": dict(title="Отримувати новини", desc="Новини про продукти та релізи blumixy на пошту.",
                   lead="Залиште email, щоб дізнаватися про релізи та плейтести. Пишемо лише тоді, коли є що сказати.",
                   label="Електронна пошта", btn="Підписатися",
                   note="Використовуємо вашу пошту лише для новин blumixy. Відписатися можна будь-коли, відповівши «стоп»."),
    }[lang]
    if FORM_ENDPOINT:
        form = (f'<form class="form" action="{FORM_ENDPOINT}" method="POST">'
                f'<label for="em">{e(c["label"])}</label>'
                f'<input id="em" type="email" name="email" required autocomplete="email" placeholder="you@example.com">'
                f'<input type="hidden" name="_subject" value="blumixy — new subscriber ({lang})">'
                f'<button class="btn primary" type="submit">{e(c["btn"])}</button><p class="note">{e(c["note"])}</p></form>')
    else:  # no form backend yet: open the visitor's mail app with a ready message
        form = (f'<form class="form" action="mailto:{EMAIL}" method="GET">'
                f'<input type="hidden" name="subject" value="Subscribe">'
                f'<button class="btn primary" type="submit">{e(c["btn"])}</button><p class="note">{e(c["note"])}</p></form>')
    body = f"""
<section class="page-head"><div class="wrap">
  <h1>{e(c["title"])}</h1><p class="lead">{e(c["lead"])}</p>
  {form}
</div></section>
"""
    return page(lang, "subscribe", url(lang, "subscribe"), c["title"], c["desc"], body, url("uk" if lang == "en" else "en", "subscribe"))


LEGAL = {
    "privacy": {
        "en": ("Privacy policy", "How blumixy.store handles your data.", [
            ("What we collect", ["This website does not use cookies or ad trackers.",
                                 "We use Cloudflare Web Analytics to count visits. It does not use cookies and does not identify individual visitors.",
                                 "If you email us or subscribe to updates, we keep your email address and the messages you send."]),
            ("How we use it", ["To reply to you and, if you subscribed, to send blumixy news.",
                               "We do not sell or share your data with third parties for marketing."]),
            ("Your choices", [f"Ask us to delete your messages or email address at any time: {EMAIL}."]),
        ]),
        "uk": ("Політика конфіденційності", "Як blumixy.store поводиться з вашими даними.", [
            ("Що ми збираємо", ["Сайт не використовує cookie та рекламні трекери.",
                                "Для підрахунку відвідувань ми використовуємо Cloudflare Web Analytics. Він не використовує cookie і не ідентифікує окремих відвідувачів.",
                                "Якщо ви пишете нам або підписуєтеся на новини, ми зберігаємо вашу адресу та листи."]),
            ("Як ми це використовуємо", ["Щоб відповісти вам, а якщо ви підписалися — щоб надсилати новини blumixy.",
                                         "Ми не продаємо і не передаємо ваші дані третім особам для маркетингу."]),
            ("Ваш вибір", [f"Ви можете будь-коли попросити видалити ваші листи чи адресу: {EMAIL}."]),
        ]),
    },
    "terms": {
        "en": ("Terms of use", "Terms of use for blumixy.store.", [
            ("Using this site", ["The content on this site is provided for general information about blumixy and its products.",
                                 "Logos and images from the press kit may be used to write about blumixy. Please don’t alter them."]),
            ("Projects and products", ["Client work is governed by a separate agreement for each project.",
                                       "Our games and apps have their own terms, shown in the respective app store."]),
            ("Contact", [f"Questions about these terms: {EMAIL}."]),
        ]),
        "uk": ("Умови використання", "Умови використання blumixy.store.", [
            ("Використання сайту", ["Матеріали сайту надано для загальної інформації про blumixy та її продукти.",
                                    "Логотипи та зображення з пресматеріалів можна використовувати в публікаціях про blumixy. Просимо не змінювати їх."]),
            ("Проєкти та продукти", ["Роботу для клієнтів регулює окрема угода для кожного проєкту.",
                                     "Наші ігри та застосунки мають власні умови, вказані у відповідних магазинах застосунків."]),
            ("Контакт", [f"Питання щодо цих умов: {EMAIL}."]),
        ]),
    },
}


def legal(lang: str, key: str) -> str:
    title, desc, sections = LEGAL[key][lang]
    upd = ("Last updated: " if lang == "en" else "Оновлено: ") + fmt_date(lang, BUILD_DATE)
    secs = "".join(f"<h2>{e(h)}</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in items)}</ul>" for h, items in sections)
    body = f"""
<section class="page-head"><div class="wrap prose">
  <h1>{e(title)}</h1><p class="muted" style="margin-top:16px">{e(upd)}</p>
  {secs}
</div></section>
"""
    return page(lang, key, url(lang, key), title, desc, body, url("uk" if lang == "en" else "en", key))


def not_found() -> str:
    body = f"""
<section class="page-head lost"><div class="wrap">
  <h1>Page not found</h1>
  <p class="lead">The link may be old or mistyped. Сторінку не знайдено — можливо, посилання застаріло.</p>
  <div class="actions"><a class="btn primary" href="/">Go to the home page</a><a class="btn" href="/uk/">На головну</a></div>
</div></section>
"""
    return page("en", "404", "/404.html", "Page not found", "This page doesn’t exist.", body)


# ---------------------------------------------------------------- feeds, sitemap
def feeds() -> dict[str, str]:
    posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)
    rfc = lambda d: d.strftime("%a, %d %b %Y 12:00:00 +0000")
    items = "".join(
        f"""  <item>
    <title>{e(p["en"]["title"])}</title>
    <link>{DOMAIN}{url("en", p["slug"])}</link>
    <guid isPermaLink="true">{DOMAIN}{url("en", p["slug"])}</guid>
    <pubDate>{rfc(p["date"])}</pubDate>
    <description>{e(p["en"]["summary"])}</description>
  </item>
""" for p in posts)
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>blumixy — News</title>
  <link>{DOMAIN}/news/</link>
  <atom:link href="{DOMAIN}/news/rss.xml" rel="self" type="application/rss+xml"/>
  <description>Company updates, releases and devlogs</description>
  <language>en</language>
  <lastBuildDate>{rfc(posts[0]["date"])}</lastBuildDate>
{items}</channel>
</rss>
"""
    entries = "".join(
        f"""  <entry>
    <title>{e(p["en"]["title"])}</title>
    <link href="{DOMAIN}{url("en", p["slug"])}"/>
    <id>{DOMAIN}{url("en", p["slug"])}</id>
    <updated>{p["date"].isoformat()}T12:00:00Z</updated>
    <summary>{e(p["en"]["summary"])}</summary>
  </entry>
""" for p in posts)
    atom = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>blumixy — News</title>
  <link href="{DOMAIN}/news/"/>
  <link href="{DOMAIN}/news/atom.xml" rel="self"/>
  <updated>{posts[0]["date"].isoformat()}T12:00:00Z</updated>
  <id>{DOMAIN}/news/</id>
  <author><name>blumixy</name></author>
{entries}</feed>
"""
    jf = {"version": "https://jsonfeed.org/version/1.1", "title": "blumixy — News",
          "home_page_url": f"{DOMAIN}/news/", "feed_url": f"{DOMAIN}/news/index.json",
          "items": [{"id": f"{DOMAIN}{url('en', p['slug'])}", "url": f"{DOMAIN}{url('en', p['slug'])}",
                     "title": p["en"]["title"], "content_text": p["en"]["summary"],
                     "date_published": f"{p['date'].isoformat()}T12:00:00Z"} for p in posts]}
    return {"news/rss.xml": rss, "feed.xml": rss, "news/atom.xml": atom,
            "news/index.json": json.dumps(jf, ensure_ascii=False, indent=2) + "\n"}


def sitemap() -> str:
    keys = ["home", "about", "services", "news", "press", "subscribe", "privacy", "terms"] + [p["slug"] for p in POSTS]
    out = []
    for k in keys:
        for lg in LANGS:
            alts = "".join(f'\n  <xhtml:link rel="alternate" hreflang="{a}" href="{DOMAIN}{url(a, k)}"/>' for a in LANGS)
            alts += f'\n  <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}{url("en", k)}"/>'
            out.append(f"<url>\n  <loc>{DOMAIN}{url(lg, k)}</loc>\n  <lastmod>{BUILD_DATE.isoformat()}</lastmod>{alts}\n</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(out) + "\n</urlset>\n")


def path_to_file(p: str) -> str:
    p = p.lstrip("/")
    return p + "index.html" if (p == "" or p.endswith("/")) else p


def main() -> None:
    files: dict[str, str] = {}
    for lg in LANGS:
        for fn in (home, about, services, news_index, press, subscribe):
            key = fn.__name__.replace("news_index", "news")
            files[path_to_file(url(lg, key))] = fn(lg)
        for k in ("privacy", "terms"):
            files[path_to_file(url(lg, k))] = legal(lg, k)
        for p in POSTS:
            files[path_to_file(url(lg, p["slug"]))] = news_post(lg, p)
    files["404.html"] = not_found()
    files.update(feeds())
    files["sitemap.xml"] = sitemap()
    files["robots.txt"] = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    files["CNAME"] = DOMAIN.split("//")[1] + "\n"
    for rel, content in files.items():
        f = ROOT / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files")


if __name__ == "__main__":
    main()
