#!/usr/bin/env python3
"""Render README.md to a local HTML page that looks like GitHub.

Rewrites the raw.githubusercontent URLs for files that live in this repo to
local paths, so the hero SVG shows up before anything is pushed.

    python3 tools/preview.py && open preview.html
"""

import re
import webbrowser
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
RAW = "https://raw.githubusercontent.com/pratt778/pratt778/main/"

CSS = """
:root{color-scheme:dark}
body{background:#0d1117;color:#e6edf3;margin:0;padding:32px 16px;
 font:16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}
.wrap{max-width:830px;margin:0 auto}
.note{border:1px solid #3d444d;border-left:3px solid #DB6B34;border-radius:6px;
 padding:10px 14px;margin:0 0 24px;color:#9198a1;font-size:13px}
h2{border-bottom:1px solid #3d444d;padding-bottom:.3em;margin:24px 0 16px;
 font-size:1.5em;font-weight:600}
h3{border-bottom:1px solid #3d444d;padding-bottom:.3em;margin-top:24px}
p{margin:0 0 16px}
code{background:#151b23;padding:.2em .4em;border-radius:6px;font-size:85%;
 font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
pre{background:#151b23;padding:16px;border-radius:6px;overflow:auto}
pre code{background:none;padding:0;font-size:13px;line-height:1.45}
img{max-width:100%;vertical-align:middle}
hr{border:0;border-top:1px solid #3d444d;margin:24px 0}
a{color:#4493f8;text-decoration:none}
details{margin:12px 0}
summary{cursor:pointer;padding:4px 0}
sub{color:#9198a1}
"""


def main():
    md = (ROOT / "README.md").read_text(encoding="utf-8")

    # point same-repo assets at the local files so they render pre-push
    for name in ("dark_mode.svg", "light_mode.svg"):
        md = md.replace(RAW + name, name)

    html = markdown.markdown(
        md, extensions=["fenced_code", "tables", "md_in_html"]
    )

    note = ("<p class='note'>Local preview. The hero SVG is read from disk; "
            "the contribution-snake images stay blank until the workflow has "
            "run once on GitHub.</p>")

    out = ROOT / "preview.html"
    out.write_text(
        f"<!doctype html><meta charset='utf-8'><title>README preview</title>"
        f"<style>{CSS}</style><div class='wrap'>{note}{html}</div>",
        encoding="utf-8",
    )
    print(f"wrote {out}")
    webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()
