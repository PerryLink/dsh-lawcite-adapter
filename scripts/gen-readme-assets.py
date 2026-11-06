#!/usr/bin/env python3
"""README visuals for dsh-lawcite-adapter, drawn from this package's own artifacts.

Outputs (docs/assets/, idempotent overwrite):

  dsh-lawcite-adapter-hero-{zh,en}-{light,dark}.webp   1440x576
  dsh-lawcite-adapter-flow-v5-{light,dark}.svg          1100x660

Both figures are derived from what this repository actually ships:

  * `src/model.ts` - the reader contract: one header (documentTitle,
    documentType, author, draftedAt, checkedAt) plus one row per citation;
    twelve canonical row fields (citationNo, lawName, articleNo, paragraphNo,
    itemNo, quotedText, usage, purpose, effectiveStatus, versionNote,
    citationStyle, note) with Chinese and English aliases, and
    REQUIRE_ANY_OF = lawName | articleNo | quotedText.
  * `src/shared/table.ts` - alias matching ignores case, spaces, underscores
    and hyphens; at least one known citation column must be recognised or the
    reader refuses the material.
  * `rules/lawcite-adapter.yaml` - pack `2026.1`, eight rules, all
    `institutional-configuration` / `info`: LC-001 presenceAny(lawName,
    articleNo), LC-002 pattern(articleNo), LC-003 presence(quotedText),
    LC-004 enum(effectiveStatus, values []), LC-005 presenceAny(usage,
    purpose), LC-006 headerPresence(documentTitle, documentType), LC-007
    unique(citationNo), LC-008 containsAny(quotedText, placeholder terms).
  * `samples/quickstart/input/LC-001-unsafe.json` - the sample drawn in the
    flow: one row, lawName and articleNo empty, quotedText present, usage and
    purpose present, effectiveStatus 现行有效. A real run of this sample
    (documented by `samples/quickstart/expected/result.json`) yields one issue
    (LC-001, row 1, lawName: both lawName and articleNo empty) and one skipped
    rule (LC-004: values unset). Six rules ran and found nothing, so they
    appear in neither list - that is the distinction the diagram is built to
    preserve.
  * `src/view.ts` - the report fields drawn in the band: summary, issueCount,
    skippedCount, markdown + reportJson, the wording guard and the mandatory
    disclaimer.

Hero - left column is copy (kicker / wordmark / two value lines / two
subtitle lines / meta / footer). The right side is this plugin's own artifact,
not a generic dashboard: one citation inventory page with the empty lawName
and articleNo fields marked, pinned to a report card whose margin notes carry
LC-001 (one issue), LC-008 (placeholder) and LC-004 (skipped, values unset).
The page and the note cards are the same object at two distances: material,
then the difference list.

Flow - grammar = FIELD-COLUMN x RULE MAP, not a row of nodes. The header band
and the seven rule-bearing fields of one citation row are laid out as columns;
every rule sits under the field(s) it reads, with the engine's own check kind.
One sample row is enough to show the three outcomes without inventing a run:
LC-001 fires (one issue, locator row 1 + lawName), LC-004 cannot run because
its values list is unset (skipped, with its reason), and the other six rules
ran clean and enter neither list. The report band carries the real counters
(error 0 / warn 0 / info 1, issueCount 1, skippedCount 1) and a separate
"not checked" strip keeps the boundary visible: existence, being in force,
amendment/repeal, applicability, compliance and liability are outside this
tool.

Every label is measured with the same fonts the figure names before it is
drawn; anything that would overflow aborts the run instead of shipping clipped
text. Hero title 84px, value lines 28px, subtitle 24.5px, meta 20px, footer
16px. Flow: figure title 29px, field names and rule ids 13px, values 12-15px,
report text 11.5px, annotations >= 11px.

Old single-skin assets (`...-flow.svg`, `...-flow-{light,dark}.svg`,
`...-hero.png`, `...-demo.*`, `quickstart.*`) stay on disk so external links
keep resolving; the READMEs reference only the new hero set and flow-v5 pair.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf /
           consolab.ttf.
"""
from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-lawcite-adapter"

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")

os.makedirs(OUT, exist_ok=True)

FONT_CSS_SANS = ("'Microsoft YaHei','Segoe UI','PingFang SC',"
                 "'Noto Sans CJK SC',sans-serif")
FONT_CSS_MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", panel="#fbfaff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent_soft="#ece7f9", tint="#f7f5fb",
        rule="#e7e4f0", warn="#b45309", warn_bg="#fbf1e4",
        shadow=(43, 35, 80), shadow_hex="#2b2440", shadow_alpha=46,
        dot="#cfc8e2", dot_alpha=72,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", panel="#151d2c", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent_soft="#242d42", tint="#202839",
        rule="#2b3348", warn="#d9a441", warn_bg="#292217",
        shadow=(0, 0, 0), shadow_hex="#000000", shadow_alpha=150,
        dot="#2a3346", dot_alpha=66,
    ),
}

# ---------------------------------------------------------------------------
# small shared helpers
# ---------------------------------------------------------------------------
_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def font(size: float, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    key = (kind, max(1, int(round(size))))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[kind], key[1])
    return _font_cache[key]


def measure(text: str, size: float, kind: str = "cjk") -> float:
    return _MEASURE.textlength(text, font=font(size, kind))


def hx(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgba(color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    return hx(color) + (alpha,)


def require_w(text: str, size: float, kind: str, max_w: float,
              what: str) -> None:
    got = measure(text, size, kind)
    if got > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs "
                         f"{got:.1f}px > {max_w:.0f}px")


def fit(text: str, kind: str, max_w: float, start: float,
        minimum: float) -> float:
    size = float(start)
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    if measure(text, size, kind) > max_w:
        raise SystemExit(f"FATAL: text does not fit {max_w:.0f}px at >= "
                         f"{minimum}px: {text!r}")
    return size


def wrap(text: str, size: float, kind: str, max_w: float) -> list[str]:
    """Greedy wrap that respects spaces for Latin and characters for CJK."""
    tokens = text.split(" ") if " " in text else list(text)
    joiner = " " if " " in text else ""
    lines: list[str] = []
    current = ""
    for token in tokens:
        candidate = token if current == "" else current + joiner + token
        if measure(candidate, size, kind) <= max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = token
    if current:
        lines.append(current)
    return lines


def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(top), hx(bottom)
    for y in range(h):
        t = 0.10 * (y / h) + 0.90 * (y / h) ** 1.35
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base.convert("RGBA")


def add_glow(img: Image.Image, cx: int, cy: int, radius: int, color: str,
             alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    rgb = hx(color)
    for i in range(12, 0, -1):
        r = radius * i / 12
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=rgb + (int(alpha * (1 - i / 13)),))
    layer = layer.filter(ImageFilter.GaussianBlur(42))
    return Image.alpha_composite(img, layer)


def add_dots(img: Image.Image, color: str, alpha: int, step: int = 30,
             radius: float = 1.15) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    fill = rgba(color, alpha)
    for y in range(18, img.height, step):
        for x in range(18, img.width, step):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                         fill=fill)
    return Image.alpha_composite(img, layer)


def shadow_card(img: Image.Image, box: tuple[int, int, int, int], radius: int,
                fill: str, edge: str, s: dict, width: int = 1,
                shadow: int = 18, spread: int = 7) -> Image.Image:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle([x0 + 1, y0 + spread, x1 + 1, y1 + spread],
                           radius=radius,
                           fill=rgba("#000000", 0) if s["shadow_alpha"] == 0
                           else s["shadow"] + (s["shadow_alpha"],))
    img = Image.alpha_composite(img, layer.filter(
        ImageFilter.GaussianBlur(shadow / 2)))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(box, radius=radius, fill=rgba(fill),
                           outline=rgba(edge), width=width)
    return img


def rounded(img: Image.Image, box: tuple[int, int, int, int], radius: int,
            fill: str | None = None, edge: str | None = None,
            width: int = 1) -> Image.Image:
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(box, radius=radius,
                           fill=rgba(fill) if fill else None,
                           outline=rgba(edge) if edge else None,
                           width=width)
    return img


def dashed_line(img: Image.Image, start: tuple[float, float],
                end: tuple[float, float], color: str, width: int = 1,
                dash: int = 5, gap: int = 4) -> None:
    draw = ImageDraw.Draw(img)
    x0, y0 = start
    x1, y1 = end
    length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    if length == 0:
        return
    dx, dy = (x1 - x0) / length, (y1 - y0) / length
    pos = 0.0
    while pos < length:
        end_pos = min(pos + dash, length)
        draw.line([(x0 + dx * pos, y0 + dy * pos),
                   (x0 + dx * end_pos, y0 + dy * end_pos)],
                  fill=rgba(color), width=width)
        pos = end_pos + gap


def dashed_rect(img: Image.Image, box: tuple[int, int, int, int], color: str,
                width: int = 1, dash: int = 5, gap: int = 4) -> None:
    x0, y0, x1, y1 = box
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                 ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        dashed_line(img, a, b, color, width, dash, gap)


def txt(img: Image.Image, xy: tuple[float, float], text: str, size: float,
        fill: str, kind: str = "cjk", anchor: str = "la",
        alpha: int = 255) -> None:
    draw = ImageDraw.Draw(img)
    # The layout below is written in baselines; Pillow's default anchor is the
    # ascender top, so translate the two-character anchors explicitly.
    anchor = {"la": "ls", "ma": "ms", "ra": "rs", "mm": "ms"}.get(
        anchor, anchor)
    draw.text(xy, text, font=font(size, kind), fill=rgba(fill, alpha),
              anchor=anchor)


def tracked(img: Image.Image, xy: tuple[float, float], text: str, size: float,
            fill: str, kind: str = "mono_bold", spacing: float = 1.8,
            alpha: int = 255) -> None:
    draw = ImageDraw.Draw(img)
    x, y = xy
    f = font(size, kind)
    for ch in text:
        draw.text((x, y), ch, font=f, fill=rgba(fill, alpha), anchor="ls")
        x += draw.textlength(ch, font=f) + spacing


# ---------------------------------------------------------------------------
# 1. hero - Pillow, 1440x576, zh/en x light/dark
# ---------------------------------------------------------------------------
COPY = {
    "zh": dict(
        kicker="DSH 插件 · 法条引用核对",
        title=[[("逐处核对，", "text")], [("逐栏落点", "accent")]],
        values=["只回答：哪一行、哪一栏、差什么。",
                "不查法规库，不下结论，不改原件。"],
        subs=["8 条规则逐条附依据；执行不了的写入 skipped。",
              "只列差异，结论与责任留给复核人。"],
        meta=["lawcite_adapter · JSON / YAML · LC-001…LC-008",
              "DSH ≥0.2.1 <0.3.0 · rules/lawcite-adapter.yaml"],
        footer="原件永不修改 · Apache-2.0 · PerryLink DSH plugin family",
        title_ys=[172, 272],
        value_ys=[340, 378],
        sub_ys=[422, 450],
        meta_ys=[496, 520],
        footer_y=556,
        divider_y=534,
    ),
    "en": dict(
        kicker="DSH PLUGIN · LAW CITATION CHECK",
        title=[[("Line by line,", "text")], [("field by field.", "accent")]],
        values=["Which row, which column, what differs.",
                "No statute database, no verdict, no edits."],
        subs=["8 rules, each sourced; cannot-run checks say so.",
              "Differences only; the verdict is yours."],
        meta=["lawcite_adapter · JSON / YAML · LC-001…LC-008",
              "DSH ≥0.2.1 <0.3.0 · rules/lawcite-adapter.yaml"],
        footer="The original is never modified · Apache-2.0 · PerryLink DSH plugin family",
        title_ys=[168, 268],
        value_ys=[336, 374],
        sub_ys=[418, 446],
        meta_ys=[494, 518],
        footer_y=554,
        divider_y=532,
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    c = COPY[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = add_glow(img, 1080, 170, 430, s["accent"], 36 if skin == "light" else 24)
    img = add_glow(img, 280, 520, 380, "#8b7ad8" if skin == "light" else "#32406b",
                   34 if skin == "light" else 20)
    img = add_dots(img, s["dot"], s["dot_alpha"])

    # editorial rail
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([54, 86, 58, 546], radius=2, fill=rgba(s["accent"]))
    draw.ellipse([50, 80, 62, 92], fill=rgba(s["accent"]))
    draw.ellipse([50, 540, 62, 552], fill=rgba(s["accent"]))

    # left copy
    tracked(img, (84, 92), c["kicker"], 17, s["accent"], "cjk_bold", 1.4)
    draw = ImageDraw.Draw(img)

    title_size = 84.0
    for line, y in zip(c["title"], c["title_ys"]):
        max_w = 650.0
        total = sum(measure(part, title_size, "cjk_bold") for part, _ in line)
        if total > max_w:
            title_size = min(title_size,
                             fit("".join(part for part, _ in line),
                                 "cjk_bold", max_w, title_size, 48))
        x = 84.0
        for part, color in line:
            txt(img, (x, y), part, title_size, s[color], "cjk_bold")
            x += measure(part, title_size, "cjk_bold")

    for text, y in zip(c["values"], c["value_ys"]):
        require_w(text, 28, "cjk", 650, f"{lang} value line")
        txt(img, (84, y), text, 28, s["text"], "cjk")

    for text, y in zip(c["subs"], c["sub_ys"]):
        require_w(text, 24.5, "cjk", 650, f"{lang} subtitle line")
        txt(img, (84, y), text, 24.5, s["sub"], "cjk")

    for text, y in zip(c["meta"], c["meta_ys"]):
        require_w(text, 20, "mono", 650, f"{lang} meta line")
        txt(img, (84, y), text, 20, s["sub"], "mono")

    draw = ImageDraw.Draw(img)
    draw.line([84, c["divider_y"], 700, c["divider_y"]],
              fill=rgba(s["edge"]), width=1)
    require_w(c["footer"], 16, "cjk", 650, f"{lang} footer")
    txt(img, (84, c["footer_y"]), c["footer"], 16, s["faint"], "cjk")

    # right-hand audit sheet
    img = shadow_card(img, (760, 68, 1380, 508), 22, s["card"], s["edge"], s,
                      width=1, shadow=22, spread=9)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([792, 100, 1128, 476], radius=14,
                           fill=rgba(s["card"]), outline=rgba(s["edge"]), width=1)
    draw.rounded_rectangle([792, 100, 798, 476], radius=3,
                           fill=rgba(s["accent"]))

    tracked(img, (814, 122), "CITATION INVENTORY", 11, s["accent"],
            "mono_bold", 1.2)
    txt(img, (814, 168), "某某买卖合同纠纷起诉状", 18.5, s["text"], "cjk_bold")
    txt(img, (814, 189), "documentTitle · documentType · 2026-05-12",
        11, s["faint"], "mono")
    draw = ImageDraw.Draw(img)
    draw.line([814, 202, 1106, 202], fill=rgba(s["rule"]), width=1)
    for y, w in ((216, 276), (232, 232)):
        draw.rounded_rectangle([814, y, 814 + w, y + 6], radius=3,
                               fill=rgba(s["rule"]))

    # row 1 - the sample row; lawName and articleNo are empty
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([810, 246, 1112, 352], radius=10,
                           fill=rgba(s["tint"]), outline=rgba(s["accent"]),
                           width=1)
    draw.ellipse([820, 256, 840, 276], fill=rgba(s["accent"]))
    txt(img, (830, 269), "1", 10.5, s["card"], "mono_bold", "mm")
    txt(img, (848, 271), "row 1", 11, s["faint"], "mono")
    txt(img, (940, 271), "lawName · articleNo", 11, s["faint"], "mono")
    txt(img, (848, 294), "lawName", 11, s["faint"], "mono")
    dashed_rect(img, (848, 302, 918, 326), s["accent"], 1, 4, 3)
    txt(img, (883, 321), "（空）", 12, s["accent"], "cjk", "mm")
    txt(img, (936, 294), "articleNo", 11, s["faint"], "mono")
    dashed_rect(img, (936, 302, 1006, 326), s["accent"], 1, 4, 3)
    txt(img, (971, 321), "（空）", 12, s["accent"], "cjk", "mm")
    txt(img, (848, 344), "quotedText", 11, s["faint"], "mono")
    txt(img, (934, 344), "当事人一方不履行合同义务……", 11, s["sub"], "cjk")

    # row 2 - a placeholder is visible, so the LC-008 annotation has a referent
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([810, 356, 1112, 424], radius=10,
                           fill=rgba(s["card"]), outline=rgba(s["edge"]),
                           width=1)
    draw.ellipse([820, 366, 840, 386], fill=rgba(s["faint"]))
    txt(img, (830, 379), "2", 10.5, s["card"], "mono_bold", "mm")
    txt(img, (848, 379), "《中华人民共和国劳动合同法》", 11.5, s["sub"], "cjk")
    txt(img, (1020, 379), "第三十九条", 11.5, s["sub"], "cjk")
    txt(img, (848, 404), "quotedText", 11, s["faint"], "mono")
    txt(img, (934, 404), "【待补充】", 12, s["warn"], "cjk")

    for y, w in ((436, 250), (452, 210)):
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([814, y, 814 + w, y + 6], radius=3,
                               fill=rgba(s["rule"]))
    txt(img, (814, 470), "locator = row + field · 8 rules", 11,
        s["faint"], "mono")

    # report card pinned at the margin
    img = shadow_card(img, (1148, 100, 1360, 476), 14, s["panel"], s["edge"], s,
                      width=1, shadow=16, spread=5)
    tracked(img, (1166, 122), "REPORT", 11, s["accent"], "mono_bold", 1.2)
    txt(img, (1166, 142), "lawcite_adapter", 11, s["faint"], "mono")

    # annotation 1 - LC-001
    img = shadow_card(img, (1162, 158, 1346, 246), 10, s["card"], s["edge"], s,
                      width=1, shadow=10, spread=3)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1162, 158, 1166, 246], radius=2,
                           fill=rgba(s["accent"]))
    draw.ellipse([1322, 164, 1340, 182], fill=rgba(s["accent"]))
    txt(img, (1331, 176), "1", 9.5, s["card"], "mono_bold", "mm")
    txt(img, (1176, 182), "LC-001", 13, s["accent"], "mono_bold")
    txt(img, (1176, 200), "row 1 · lawName", 11, s["sub"], "mono")
    txt(img, (1176, 220), "found  both empty", 11.5, s["text"], "cjk")
    txt(img, (1176, 236), "expected  ≥ 1 of the two", 11, s["faint"], "cjk")

    # annotation 2 - LC-008
    img = shadow_card(img, (1162, 256, 1346, 344), 10, s["card"], s["edge"], s,
                      width=1, shadow=10, spread=3)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1162, 256, 1166, 344], radius=2,
                           fill=rgba(s["accent"]))
    draw.ellipse([1322, 262, 1340, 280], fill=rgba(s["accent"]))
    txt(img, (1331, 274), "2", 9.5, s["card"], "mono_bold", "mm")
    txt(img, (1176, 280), "LC-008", 13, s["accent"], "mono_bold")
    txt(img, (1176, 298), "row 2 · quotedText", 11, s["sub"], "mono")
    txt(img, (1176, 318), "found  【待补充】", 11.5, s["text"], "cjk")
    txt(img, (1176, 334), "expected  no placeholder", 11, s["faint"], "cjk")

    # annotation 3 - LC-004, skipped rather than passed
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1162, 354, 1346, 430], radius=10,
                           fill=rgba(s["warn_bg"]),
                           outline=rgba(s["accent"]), width=1)
    dashed_rect(img, (1162, 354, 1346, 430), s["accent"], 1, 5, 4)
    txt(img, (1176, 378), "LC-004", 13, s["accent"], "mono_bold")
    txt(img, (1240, 378), "skipped", 11, s["accent"], "mono")
    txt(img, (1176, 398), "values []", 11, s["sub"], "mono")
    txt(img, (1176, 414), "enum · not configured", 11, s["faint"], "cjk")

    draw = ImageDraw.Draw(img)
    draw.line([1176, 442, 1332, 442], fill=rgba(s["rule"]), width=1)
    txt(img, (1176, 460), "no verdict · original unchanged", 11,
        s["faint"], "cjk")

    # a thin, measured link between the page and its margin notes
    draw = ImageDraw.Draw(img)
    draw.ellipse([1132, 292, 1140, 300], fill=rgba(s["accent"]))
    dashed_line(img, (1140, 296), (1162, 210), s["accent"], 1, 4, 3)
    draw.ellipse([1132, 386, 1140, 394], fill=rgba(s["accent"]))
    dashed_line(img, (1140, 390), (1162, 310), s["accent"], 1, 4, 3)

    # outer-panel caption
    tracked(img, (792, 84), "AUDIT SHEET", 11, s["accent"], "mono_bold", 1.2)
    txt(img, (1290, 84), "JSON / YAML", 11, s["faint"], "mono")

    path = os.path.join(OUT, f"{NAME}-hero-{lang}-{skin}.webp")
    img.convert("RGB").save(path, "WEBP", quality=90, method=6)
    print(f"wrote {os.path.basename(path)}")


# ---------------------------------------------------------------------------
# 2. flow - hand-written SVG, 1100x660, light/dark
# ---------------------------------------------------------------------------
def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    W, H = 1100, 660
    accent = s["accent"]
    parts: list[str] = []

    def t(x: float, y: float, text: str, size: float, fill: str,
          kind: str = "sans", weight: int = 400, anchor: str = "start",
          opacity: float | None = None, tracking: float | None = None,
          baseline: bool = False) -> str:
        family = FONT_CSS_MONO if kind == "mono" else FONT_CSS_SANS
        attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
                 f'font-family="{family}"', f'font-size="{size}"',
                 f'xml:space="preserve"']
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if tracking is not None:
            attrs.append(f'letter-spacing="{tracking}"')
        return f"<text {' '.join(attrs)}>{escape(text)}</text>"

    def r(x: float, y: float, w: float, h: float, fill: str,
          stroke: str | None = None, sw: float = 1.3, rx: float = 0,
          dash: str | None = None, shadow: bool = False,
          opacity: float | None = None) -> str:
        attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"',
                 f'rx="{rx}"', f'fill="{fill}"']
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        return f"<rect {' '.join(attrs)}/>"

    def line(x1: float, y1: float, x2: float, y2: float, stroke: str,
             sw: float = 1.2, dash: str | None = None,
             opacity: float | None = None) -> str:
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw}"',
                 'stroke-linecap="round"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        return f"<line {' '.join(attrs)}/>"

    def pill(x: float, y: float, text: str, size: float, fg: str, bg: str,
             edge: str | None = None, dash: str | None = None,
             kind: str = "mono", weight: int = 700,
             pad: float = 16) -> tuple[str, float, float]:
        font_kind = f"{kind}_bold" if weight >= 700 else kind
        w = measure(text, size, font_kind) + pad
        h = size + 9
        body = r(x, y, w, h, bg, edge or "none", 1, h / 2, dash)
        body += t(x + w / 2, y + h / 2 + size * 0.34, text, size, fg,
                  kind, weight, "middle")
        return body, w, h

    def pill_w(text: str, size: float, kind: str = "mono",
               weight: int = 700, pad: float = 16) -> float:
        font_kind = f"{kind}_bold" if weight >= 700 else kind
        return measure(text, size, font_kind) + pad

    # ---- background ------------------------------------------------------
    parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="fig-title fig-desc">
<title id="fig-title">{NAME}: one citation inventory, eight rules, a field-column map</title>
<desc id="fig-desc">The header band and the seven rule-bearing fields of one citation row are laid out as columns. Each rule sits under the field or fields it reads, with the engine's own check kind: LC-001 presenceAny reads lawName and articleNo, LC-002 pattern reads articleNo, LC-003 presence and LC-008 containsAny read quotedText, LC-004 enum reads effectiveStatus, LC-005 presenceAny reads usage and purpose, LC-006 headerPresence reads the header, LC-007 unique reads citationNo. The real run of samples/quickstart/input/LC-001-unsafe.json yields one issue (LC-001, row 1, lawName: lawName and articleNo both empty) and one skipped rule (LC-004: values unset, enum cannot run). LC-002, LC-003, LC-005, LC-006, LC-007 and LC-008 ran and found nothing, so they enter neither list. The report band carries error 0, warn 0, info 1, issueCount 1, skippedCount 1, buildView, markdown plus reportJson, the wording guard and the disclaimer. The strip above the report keeps the boundary visible: statute existence, being in force, amendment or repeal, applicability, compliance and liability are not checked. The tool only reads file or material; the original is never modified and the verdict stays with the reviewer.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0.18" y2="1">
    <stop offset="0" stop-color="{s['bg_from']}"/><stop offset="1" stop-color="{s['bg_to']}"/>
  </linearGradient>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="180%">
    <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="{s['shadow_hex']}" flood-opacity="{0.14 if skin == 'light' else 0.52}"/>
  </filter>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="1.2" fill="{s['dot']}"/>
  </pattern>
</defs>
<rect x="0" y="0" width="{W}" height="{H}" rx="22" fill="url(#bg)"/>
<rect x="0" y="0" width="{W}" height="{H}" rx="22" fill="url(#dots)" opacity="0.5"/>
''')

    # ---- header ----------------------------------------------------------
    parts.append(t(44, 50, NAME, 29, s["text"], "mono", 700))
    parts.append(t(44, 76,
                   "8 rules read one citation inventory; every finding names a row and a field.",
                   14.5, s["sub"], "sans"))
    pill_text = "rules/lawcite-adapter.yaml · v2026.1 · 8 rules"
    pw = pill_w(pill_text, 11.5, "mono", 700)
    top_pill, _, _ = pill(1056 - pw, 26, pill_text, 11.5, accent,
                          s["accent_soft"], None, None, "mono", 700)
    parts.append(top_pill)
    parts.append(t(44, 104,
                   "IN  ·  file | material  ·  JSON / YAML  ·  header + rows[]  ·  read-only",
                   11, s["faint"], "mono"))
    parts.append(t(1056, 104,
                   "OUT  ·  issues[] · skipped[] · summary · markdown + reportJson",
                   11, s["faint"], "mono", anchor="end"))
    parts.append(line(44, 116, 1056, 116, s["rule"], 1))

    # ---- 01 material -----------------------------------------------------
    parts.append(t(44, 142, "01", 12, accent, "mono", 700))
    parts.append(t(70, 142, "MATERIAL", 12, accent, "sans", 700, tracking=1.4))
    parts.append(t(1056, 142,
                   "parseMaterial · aliases → 12 canonical fields",
                   11, s["faint"], "sans", anchor="end"))
    parts.append(r(44, 152, 1012, 68, s["card"], s["edge"], 1.4, 16,
                   shadow=True))
    parts.append(r(44, 152, 4, 68, accent, None, 0, 2))
    parts.append(t(60, 174, "documentTitle", 11, s["faint"], "mono"))
    parts.append(t(60, 196, "某某买卖合同纠纷起诉状", 13.5, s["text"], "sans"))
    parts.append(t(300, 174, "documentType", 11, s["faint"], "mono"))
    parts.append(t(300, 196, "民事起诉状", 13.5, s["text"], "sans"))
    parts.append(t(470, 174, "author", 11, s["faint"], "mono"))
    parts.append(t(470, 196, "王律师", 13.5, s["text"], "sans"))
    parts.append(t(580, 174, "draftedAt", 11, s["faint"], "mono"))
    parts.append(t(580, 196, "2026-05-12", 12.5, s["text"], "mono"))
    lc6, _, _ = pill(874, 164, "LC-006", 11.5, accent, s["accent_soft"],
                     None, None, "mono", 700)
    parts.append(lc6)
    parts.append(t(874, 199, "headerPresence", 11, s["faint"], "mono"))
    parts.append(t(1036, 174, "ran · neither list", 11, s["faint"], "sans",
                   anchor="end"))

    # ---- 02 field x rule -------------------------------------------------
    parts.append(t(44, 238, "02", 12, accent, "mono", 700))
    parts.append(t(70, 238, "FIELD × RULE", 12.5, accent, "sans", 700,
                   tracking=1.2))
    parts.append(t(212, 238,
                   "each rule sits under the field it reads; one row is enough",
                   11, s["faint"], "sans"))
    parts.append(t(1056, 238,
                   "onlyRules / disabledRules → skipped[]",
                   11, s["faint"], "sans", anchor="end"))

    cards = [
        dict(x=44, key="citationNo", value=[("1", 24, "mono", "text")],
             rules=[("LC-007", "unique")], outcome="ran"),
        dict(x=190, key="lawName", value=None,
             rules=[("LC-001", "presenceAny")], outcome="issue"),
        dict(x=336, key="articleNo", value=None,
             rules=[("LC-001", "presenceAny"), ("LC-002", "pattern")],
             outcome="same"),
        dict(x=482, key="quotedText",
             value=[("当事人一方不履行", 12.5, "sans", "text"),
                    ("合同义务……", 12.5, "sans", "text")],
             rules=[("LC-003", "presence"), ("LC-008", "containsAny")],
             outcome="ran"),
        dict(x=628, key="usage",
             value=[("第 2 部分", 12.5, "sans", "text"),
                    ("事实与理由", 12.5, "sans", "text")],
             rules=[("LC-005", "presenceAny")], outcome="ran"),
        dict(x=774, key="purpose",
             value=[("违约责任依据", 13, "sans", "text")],
             rules=[("LC-005", "presenceAny")], outcome="ran"),
        dict(x=920, key="effectiveStatus",
             value=[("现行有效", 15, "sans", "text")],
             rules=[("LC-004", "enum")], outcome="skipped"),
    ]

    for card in cards:
        x = card["x"]
        y, w, h = 250, 136, 206
        outcome = card["outcome"]
        fill = s["tint"] if outcome in ("issue", "skipped") else s["card"]
        if outcome == "skipped":
            parts.append(r(x, y, w, h, fill, accent, 1.8, 16, "5 4",
                           shadow=True))
        elif outcome == "issue":
            parts.append(r(x, y, w, h, fill, accent, 2, 16, None,
                           shadow=True))
        elif outcome == "same":
            parts.append(r(x, y, w, h, fill, accent, 1.5, 16, None,
                           shadow=True))
        else:
            parts.append(r(x, y, w, h, fill, s["edge"], 1.4, 16, None,
                           shadow=True))
        if outcome == "issue":
            parts.append(r(x + 1, y + 1, w - 2, 3, accent, None, 0, 1.5))
        elif outcome == "same":
            parts.append(r(x + 1, y + 1, w - 2, 3, accent, None, 0, 1.5,
                           opacity=0.5))

        parts.append(t(x + 14, 286, card["key"], 13, s["text"], "mono", 700))

        if card["value"] is None:
            parts.append(t(x + 14, 320, "—", 28, accent, "mono", 700))
            parts.append(t(x + 14, 338, "(empty)", 11, s["faint"], "mono"))
        else:
            value = card["value"]
            if len(value) == 1:
                text, size, kind, color = value[0]
                parts.append(t(x + 14, 326, text, size, s[color], kind,
                               700 if size >= 22 else 400))
            else:
                for idx, (text, size, kind, color) in enumerate(value):
                    parts.append(t(x + 14, 308 + idx * 18, text, size,
                                   s[color], kind, 400))

        rules = card["rules"]
        if len(rules) == 1:
            p, _, _ = pill(x + 14, 356, rules[0][0], 12.5, accent,
                           s["accent_soft"],
                           accent if outcome == "skipped" else None,
                           "5 4" if outcome == "skipped" else None, "mono", 700)
            parts.append(p)
            parts.append(t(x + 14, 390, rules[0][1], 11, s["faint"], "mono"))
        else:
            start = 346 if card["value"] is None else 336
            for idx, (rid, kind) in enumerate(rules):
                py = start + idx * 46
                ps, _, _ = pill(x + 14, py, rid, 12.5, accent,
                                s["accent_soft"], None, None, "mono", 700)
                parts.append(ps)
                parts.append(t(x + 14, py + 32, kind, 11, s["faint"], "mono"))

        # outcome line
        if outcome == "issue":
            parts.append(f'<circle cx="{x + 18}" cy="438" r="3.6" fill="{accent}"/>')
            parts.append(t(x + 28, 442, "issue", 11.5, accent, "sans", 700))
        elif outcome == "same":
            parts.append(f'<circle cx="{x + 18}" cy="438" r="3.6" fill="none" stroke="{accent}" stroke-width="1.4"/>')
            parts.append(t(x + 28, 442, "same issue", 11.5, accent, "sans", 700))
        elif outcome == "skipped":
            parts.append(f'<circle cx="{x + 18}" cy="438" r="3.6" fill="none" stroke="{accent}" stroke-width="1.4" stroke-dasharray="2 2"/>')
            parts.append(t(x + 28, 442, "skipped", 11.5, accent, "sans", 700))
        else:
            parts.append(f'<circle cx="{x + 18}" cy="438" r="3.6" fill="none" stroke="{s["faint"]}" stroke-width="1.3"/>')
            parts.append(t(x + 28, 442, "ran", 11.5, s["faint"], "sans"))

    # ---- boundary strip --------------------------------------------------
    parts.append(line(44, 464, 1056, 464, accent, 1.2, "4 6", 0.45))
    parts.append(t(44, 480, "NOT CHECKED", 11, s["warn"], "sans", 700,
                   tracking=0.8))
    parts.append(t(154, 480,
                   "statute existence · being in force · amendment / repeal · applicability · compliance · liability",
                   11, s["faint"], "sans"))
    parts.append(t(1056, 480, "no statute database", 11, s["faint"], "sans",
                   anchor="end"))

    # ---- 03 report -------------------------------------------------------
    parts.append(r(44, 488, 1012, 144, s["card"], s["edge"], 1.4, 18,
                   shadow=True))
    parts.append(t(64, 510, "03", 12, accent, "mono", 700))
    parts.append(t(90, 510, "REPORT", 12.5, accent, "sans", 700,
                   tracking=1.2))
    parts.append(t(158, 510, "buildView", 11, s["faint"], "mono"))
    parts.append(t(1036, 510,
                   "error 0 · warn 0 · info 1 · issueCount 1 · skippedCount 1",
                   11.5, s["text"], "mono", 700, anchor="end"))

    # issues
    part, iw, ih = pill(64, 520, "issues[]", 11.5, accent, s["accent_soft"],
                        None, None, "mono", 700)
    parts.append(part)
    parts.append(t(64 + iw + 8, 536, "1", 11.5, accent, "mono", 700))
    parts.append(r(64, 540, 612, 58, s["tint"], s["edge"], 1.2, 12))
    parts.append(t(78, 558, "LC-001", 12.5, accent, "mono", 700))
    parts.append(t(140, 558, "row 1 · lawName", 11.5, s["sub"], "mono"))
    parts.append(t(78, 576, "found", 11, s["faint"], "sans"))
    parts.append(t(122, 576, "lawName ∅ · articleNo ∅", 11.5, s["text"], "sans"))
    parts.append(t(78, 592, "expected", 11, s["faint"], "sans"))
    parts.append(t(138, 592, "at least one of the two", 11.5, s["sub"], "sans"))

    # skipped
    part, sw, sh = pill(716, 520, "skipped[]", 11.5, accent, s["accent_soft"],
                        None, None, "mono", 700)
    parts.append(part)
    parts.append(t(716 + sw + 8, 536, "1", 11.5, accent, "mono", 700))
    parts.append(r(716, 540, 200, 58, s["tint"], accent, 1.2, 12, "5 4"))
    parts.append(t(730, 558, "LC-004", 12.5, accent, "mono", 700))
    parts.append(t(790, 558, "skipped", 11, accent, "sans", 700))
    parts.append(t(730, 576, "values []", 11, s["sub"], "mono"))
    parts.append(t(730, 592, "enum · not configured", 11, s["faint"], "sans"))

    parts.append(t(64, 618,
                   "ran clean: LC-002 · LC-003 · LC-005 · LC-006 · LC-007 · LC-008 → neither list",
                   11.5, s["faint"], "sans"))
    parts.append(t(1036, 618,
                   "markdown + reportJson · wording guard + disclaimer",
                   11.5, s["faint"], "sans", anchor="end"))

    # ---- footer ----------------------------------------------------------
    parts.append(t(44, 650,
                   "differences only · no verdict · the original is never modified",
                   11.5, s["sub"], "sans"))
    parts.append(t(1056, 650,
                   "sample LC-001-unsafe.json · 8 rules · 7 fields",
                   11.5, s["faint"], "sans", anchor="end"))

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# 3. main
# ---------------------------------------------------------------------------
def main() -> None:
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
        svg = flow_svg(skin)
        # XML well-formedness gate before anything is written
        try:
            ET.fromstring(svg)
        except ET.ParseError as exc:
            raise SystemExit(f"FATAL: flow SVG is not well-formed: {exc}")
        path = os.path.join(OUT, f"{NAME}-flow-v5-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(svg)
        print(f"wrote {os.path.basename(path)}")
    print("wrote 4 hero webp + 2 flow svg to docs/assets/")


if __name__ == "__main__":
    main()
