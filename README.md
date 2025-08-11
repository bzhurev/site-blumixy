# Blumixy Landing (.org)

Статичний лендінг для домену **blumixy.org**.

## Швидкий деплой на GitHub Pages

1. Створи репозиторій, наприклад `site-blumixy`.
2. Завантаж усі файли з цієї папки у корінь репозиторію.
3. У `Settings → Pages` обери:
   - `Source: Deploy from a branch`
   - `Branch: main / root`
   - У полі Custom domain введи `blumixy.org` (файл `CNAME` вже є).
4. Додай DNS-записи у реєстраторі для `blumixy.org` (див. нижче).

## DNS для GitHub Pages (apex-домен)

A-записи для `@` (корінь домену):
- 185.199.108.153
- 185.199.109.153
- 185.199.110.153
- 185.199.111.153

CNAME для `www` → `<your-github-username>.github.io`

> Після внесення DNS-змін може знадобитися 5–60 хвилин на оновлення.

## Соцмережі
Додай посилання на Instagram/TikTok/YouTube в `index.html` у блоці `.socials`.

---

© 2025 Blumixy
