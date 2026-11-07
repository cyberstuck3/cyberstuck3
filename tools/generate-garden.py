#!/usr/bin/env python3
"""Animated pixel-art garden for a GitHub profile README.

Flower height tracks each language's share of bytes, read from the GitHub
languages API. Emits one SVG per colour theme; the panel itself is transparent
so the artwork sits on GitHub's own canvas instead of pasting a block onto it.

    python3 generate-garden.py
"""
CELL = 8

LANGS = [
    ("Python",           194563, "rose"),
    ("HTML",             154005, "bougainvillea"),
    ("Jupyter Notebook",  64417, "sunflower"),
    ("TypeScript",        57214, "sakura"),
    ("CSS",                  23, "daisy"),
]
TOTAL = sum(b for _, b, _ in LANGS)

# Only the text, soil line and grass change between themes. Flower and pot
# hues are the encoding: they identify a language and must stay constant.
THEMES = {
    "light": {"label": "#1f2328", "pct": "#59636e", "soil": "#3f7d33", "grass": "#4a8b3a"},
    "dark":  {"label": "#e6edf3", "pct": "#8b949e", "soil": "#2f6b29", "grass": "#3f8c36"},
}

PAL = {
    '.': None,
    's': '#4a8b3a', 'L': '#357a2c', 'M': '#52a541',
    'p': '#8f4b26', 'P': '#c07442', 'o': '#7a3d1e', 'O': '#a85c30',
    'r': '#a8302a', 'R': '#d8443a', 'S': '#f26a58', 'h': '#7d1f1a',
    'b': '#e2701a', 'B': '#f7a736', 'k': '#9c3f08', 'w': '#ffe6ee',
    'y': '#f0c419', 'Y': '#ffe066', 'c': '#6b3f10', 'C': '#96601a',
    'q': '#ef7fa6', 'Q': '#ffb8d0', 'e': '#f5c542',
    'n': '#6b7a82', 'D': '#ffffff',
}

POT = [
    ".ppppppppppp.", ".pPPPPPPPPPp.", "..ooooooooo..", "..oOOOOOOOo..",
    "...ooooooo...", "...oOOOOOo...", "....ooooo....",
]
STEM = [
    "......s......", "...LMMs......", "..LMMMs......", "...LMMs......",
    "......s......", "......sMML...", "......sMMML..", "......sMML...",
    "......s......", "......s......", "......s......",
]
HEADS = {
"rose": [
    # Petal divisions are drawn in the SHADOW tone, never the outline tone.
    # Hard dark marks inside a light field read as eyes, a mouth, or a maze;
    # mid-dark marks read as form. The furl sits off-centre, and the highlight
    # runs down the upper left so the bloom has a light direction.
    "....hhhhh....",
    "..hhSSSSShh..",
    ".hSSSSSSSSrh.",
    ".hSSrrrrSRrh.",
    "hSSrRRRRrRRrh",
    "hSSrRrrRrRRrh",
    "hSSrRRRrrRRrh",
    ".hSSrrrrRRrh.",
    ".hSSSSRRRRrh.",
    "..hhrrrrrhh..",
    "....hhhhh....",
],
"bougainvillea": [
    "....kbbbk....", "...kbBBBbk...", "...kbBwBbk...", "..kbbBBBbbk..",
    ".kbBBbkbBBbk.", "kbBBBbkbBBBbk", "kbBBwbkbwBBbk", ".kbBBbkbBBbk.",
    "..kbbk.kbbk..", "......k......",
],
"sunflower": [
    "....y.y.y....", "...yYyYyYy...", "..yYycccyYy..", ".yYycCCCcyYy.",
    "yYyccCCCccyYy", "yYycCCCCCcyYy", "yYyccCCCccyYy", ".yYycCCCcyYy.",
    "..yYycccyYy..", "...yYyYyYy...", "....y.y.y....",
],
"sakura": [
    "....q.q.q....", "..qqQwQwQqq..", ".qQwwwwwwwQq.", ".qQwwweewwQq.",
    "qQwwweeewwwQq", ".qQwwweewwQq.", ".qQwwwwwwwQq.", "..qqQwQwQqq..",
    "....q.q.q....",
],
"daisy": [
    ".....n.n.....", "..n.nDDDn.n..", "...nDDDDDn...", "..nDDeeeDDn..",
    ".nnDeeeeeDnn.", "..nDDeeeDDn..", "...nDDDDDn...", "..n.nDDDn.n..",
    ".....n.n.....",
],
}

W, H = 1040, 318
GROUND = 238
SLOT = W / len(LANGS)
SPRITE_W = 13 * CELL


def rects(grid, oy=0):
    """Run-length encode each row: adjacent cells of one colour become a single
    wider rect. Same picture, roughly a third of the nodes, so the SVG lands
    faster and the layout settles sooner."""
    out = []
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            col = PAL.get(row[c])
            if not col:
                c += 1
                continue
            run = 1
            while c + run < len(row) and PAL.get(row[c + run]) == col:
                run += 1
            out.append(f'<rect x="{c*CELL}" y="{oy+r*CELL}" width="{run*CELL}" height="{CELL}" fill="{col}"/>')
            c += run
    return "".join(out)


def scale_for(pct):
    """Linear in share, floored at 0.30 so a sub-1% language is a visible
    seedling rather than nothing. The printed figure carries the real number."""
    return round(max(0.30, 0.30 + 0.70 * (pct / 41.4)), 3)


def build(theme, animated=True):
    """A media query inside an SVG loaded through <img> is not evaluated against
    the user's settings in Chromium, so the in-file prefers-reduced-motion block
    cannot be relied on where this actually ships. A static variant is emitted
    and selected by the host page instead, which does see the preference."""
    T = THEMES[theme]
    parts, css = [], []

    for i, (label, byts, flower) in enumerate(LANGS):
        pct = 100 * byts / TOTAL
        s = scale_for(pct)
        head = HEADS[flower]
        sprite_h = (len(head) + len(STEM)) * CELL
        cx = SLOT * i + SLOT / 2

        pot_h = len(POT) * CELL
        pot_x = cx - SPRITE_W / 2
        pot_y = GROUND - pot_h

        inner = rects(head) + rects(STEM, len(head) * CELL)
        px, py = SPRITE_W / 2, sprite_h          # pivot: stalk meets the soil
        amp = round(1.8 + 3.2 * s, 2)            # taller stalk, more leverage
        dur = round(3.2 + 0.5 * i, 2)
        css.append(
            f"@keyframes sw{i}{{0%,100%{{transform:rotate(-{amp}deg)}}50%{{transform:rotate({amp}deg)}}}}"
            f".f{i}{{animation:sw{i} {dur}s ease-in-out infinite;animation-delay:-{round(0.8*i,2)}s;"
            f"transform-origin:{px}px {py}px}}"
        )

        # Centre the SCALED sprite on the pot's axis. Translating to the pot's
        # left edge and scaling about (0,0) left small flowers hugging the rim.
        flower_x = cx - (SPRITE_W * s) / 2
        fy = pot_y - sprite_h * s + 2.5 * CELL * s
        shown = f"{pct:.1f}%" if pct >= 0.1 else "&lt;0.1%"

        parts.append(f'<g transform="translate({flower_x:.1f},{fy:.1f}) scale({s})"><g class="f{i}">{inner}</g></g>')
        parts.append(f'<g transform="translate({pot_x:.1f},{pot_y})">{rects(POT)}</g>')
        parts.append(
            f'<text x="{cx:.0f}" y="{GROUND+32}" class="lbl">{label}</text>'
            f'<text x="{cx:.0f}" y="{GROUND+54}" class="pct">{shown}</text>'
        )

    blades = []
    for i in range(68):
        bx = 8 + i * 15.2
        bh = 6 + (i * 5) % 11
        blades.append(f'<rect class="g{i%5}" x="{bx:.0f}" y="{GROUND-bh}" width="3" height="{bh}" '
                      f'fill="{T["grass"]}" style="transform-origin:{bx+1.5:.0f}px {GROUND}px"/>')
    for k in range(5):
        # Grass whispers at 1.6deg; flowers swing at ~5deg. The hierarchy keeps
        # the eye on the data instead of the lawn.
        css.append(f"@keyframes gs{k}{{0%,100%{{transform:rotate(-1.6deg)}}50%{{transform:rotate(1.6deg)}}}}"
                   f".g{k}{{animation:gs{k} {round(5.5+k*0.8,2)}s ease-in-out infinite;animation-delay:-{round(k*1.1,2)}s}}")

    petals, SEEDS = [], ([(60,38,'#ffb8d0',15,0),(430,22,'#f7a736',18,-6),
                          (760,54,'#ffe066',16,-12),(180,86,'#e8503f',19,-3)] if animated else [])
    for i,(x,y,col,dur,delay) in enumerate(SEEDS):
        petals.append(f'<rect class="d{i}" x="{x}" y="{y}" width="6" height="6" rx="1" fill="{col}" opacity=".8"/>')
        css.append(
            f"@keyframes dr{i}{{0%{{transform:translate(0,0) rotate(0)}}"
            f"50%{{transform:translate(110px,{GROUND-40-y}px) rotate(180deg)}}"
            f"100%{{transform:translate(240px,{GROUND-10-y}px) rotate(400deg)}}}}"
            f"@keyframes fd{i}{{0%,100%{{opacity:0}}15%,80%{{opacity:.85}}}}"
            f".d{i}{{animation:dr{i} {dur}s linear infinite, fd{i} {dur}s linear infinite;animation-delay:{delay}s}}")

    alt = ("A pixel-art garden in a breeze. Five potted flowers share one soil line; each is a "
           "language in these repositories, drawn at a height proportional to its share of bytes. "
           "Python 41.4 percent, HTML 32.8 percent, Jupyter Notebook 13.7 percent, "
           "TypeScript 12.2 percent, CSS under one percent.")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{alt}">
<style>
text{{font-family:"Courier New",ui-monospace,monospace;text-anchor:middle}}
.lbl{{fill:{T['label']};font-size:16px;font-weight:700;letter-spacing:.3px}}
.pct{{fill:{T['pct']};font-size:13px}}
{" ".join(css) if animated else ""}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
{"".join(petals)}
<rect x="2" y="{GROUND}" width="{W-4}" height="3" fill="{T['soil']}"/>
{"".join(blades)}
<g shape-rendering="crispEdges">{"".join(parts)}</g>
</svg>'''


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    out = os.environ.get("GARDEN_OUT", "/Users/aifamaladinaulya/Documents/qa-portfolio/profile-readme/assets")
    for theme in THEMES:
        for animated, suffix in ((True, ""), (False, "-static")):
            name = f"garden-{theme}{suffix}.svg"
            svg = build(theme, animated)
            open(os.path.join(out, name), "w").write(svg)
            print(f"  {name:28s} {len(svg):>6} bytes  animasi={'ya' if animated else 'tidak'}")
    print()
    for label, byts, _ in LANGS:
        pct = 100 * byts / TOTAL
        print(f"  {label:18s} {pct:5.1f}%  scale={scale_for(pct)}")
