#!/usr/bin/env python3
"""Render index.md into a self-contained preview_static.html for local checking.

The preview file is written to the repo root so that relative paths
(images/, data/) resolve correctly. It is a scratch artifact: never commit it.

Usage:  ~/.workbuddy/binaries/python/envs/default/bin/python .workbuddy/build_preview.py
"""
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://mgao97.github.io"

src = (ROOT / "index.md").read_text(encoding="utf-8")
body = markdown.markdown(src, extensions=["extra", "tables", "fenced_code"])

# Make relative hrefs absolute against the live site.
# NOTE: the replacement must re-emit href=" itself, otherwise the attribute is eaten.
body = re.sub(r'href="(?!https?://|#|mailto:)', 'href="' + SITE, body)

css = (ROOT / "stylesheet.css").read_text(encoding="utf-8")
title = re.search(r"<title>(.*?)</title>", src, re.S)
title = title.group(1).strip() if title else "Min Gao"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""

out = ROOT / "preview_static.html"
out.write_text(html, encoding="utf-8")

# --- sanity checks -------------------------------------------------------
raw = html
checks = {
    "div open": raw.count("<div"),
    "div close": raw.count("</div>"),
    "pub-card": raw.count('class="pub-card"'),
}
print(f"wrote {out}  ({len(html)} bytes)")
print(checks)
for k, v in checks.items():
    if k.startswith("div") and raw.count("<div") != raw.count("</div>"):
        print("!! unbalanced divs")
