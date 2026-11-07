#!/usr/bin/env python3
"""Animated pixel-art garden. Flower height tracks each language's share of
bytes on the GitHub account, measured from the GitHub languages API."""
CELL = 8

LANGS = [
    ("Python",           194563, "rose"),
    ("HTML",             154005, "bougainvillea"),
    ("Jupyter Notebook",  64417, "sunflower"),
    ("TypeScript",        57214, "sakura"),
    ("CSS",                  23, "daisy"),
]
TOTAL = sum(b for _, b, _ in LANGS)

PAL = {
    '.': None,
    'w': '#ffe6ee',
    's': '#4a8b3a', 'L': '#357a2c', 'M': '#52a541',
    'p': '#8f4b26', 'P': '#c07442', 'o': '#7a3d1e', 'O': '#a85c30',
    'r': '#c0392b', 'R': '#e8503f', 'h': '#7d1f1a',
    'b': '#e2701a', 'B': '#f7a736', 'k': '#9c3f08',
    'y': '#f0c419', 'Y': '#ffe066', 'c': '#6b3f10', 'C': '#96601a',
    'q': '#ef7fa6', 'Q': '#ffb8d0', 'w': '#ffe6ee', 'e': '#f5c542',
    'd': '#dfe6e9', 'D': '#ffffff',
}

POT = [
    ".ppppppppppp.",
    ".pPPPPPPPPPp.",
    "..ooooooooo..",
    "..oOOOOOOOo..",
    "...ooooooo...",
    "...oOOOOOo...",
    "....ooooo....",
]

STEM = [
    "......s......",
    "...LMMs......",
    "..LMMMs......",
    "...LMMs......",
    "......s......",
    "......sMML...",
    "......sMMML..",
    "......sMML...",
    "......s......",
    "......s......",
    "......s......",
]

HEADS = {
"rose": [
    "....hhhhh....",
    "..hhrrrrrhh..",
    ".hrrRRRRRrrh.",
    ".hrRRrrrRRrh.",
    "hrRRrRRRrRRrh",
    "hrRrRRhRRrRrh",
    "hrRRrRRRrRRrh",
    ".hrRRrrrRRrh.",
    ".hrrRRRRRrrh.",
    "..hhrrrrrhh..",
    "....hhhhh....",
],
"bougainvillea": [
    "....kbbbk....",
    "...kbBBBbk...",
    "...kbBwBbk...",
    "..kbbBBBbbk..",
    ".kbBBbkbBBbk.",
    "kbBBBbkbBBBbk",
    "kbBBwbkbwBBbk",
    ".kbBBbkbBBbk.",
    "..kbbk.kbbk..",
    "......k......",
],
"sunflower": [
    "....y.y.y....",
    "...yYyYyYy...",
    "..yYycccyYy..",
    ".yYycCCCcyYy.",
    "yYyccCCCccyYy",
    "yYycCCCCCcyYy",
    "yYyccCCCccyYy",
    ".yYycCCCcyYy.",
    "..yYycccyYy..",
    "...yYyYyYy...",
    "....y.y.y....",
],
"sakura": [
    "....q.q.q....",
    "..qqQwQwQqq..",
    ".qQwwwwwwwQq.",
    ".qQwwweewwQq.",
    "qQwwweeewwwQq",
    ".qQwwweewwQq.",
    ".qQwwwwwwwQq.",
    "..qqQwQwQqq..",
    "....q.q.q....",
],
"daisy": [
    ".....d.d.....",
    "..d.dDDDd.d..",
    "...dDDDDDd...",
    "..dDDeeeDDd..",
    ".ddDeeeeeDdd.",
    "..dDDeeeDDd..",
    "...dDDDDDd...",
    "..d.dDDDd.d..",
    ".....d.d.....",
],
}

def rects(grid, oy=0):
    out = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            col = PAL.get(ch)
            if col:
                out.append(f'<rect x="{c*CELL}" y="{oy + r*CELL}" width="{CELL}" height="{CELL}" fill="{col}"/>')
    return "".join(out)

W, H = 1040, 350
GROUND = 266
SLOT = W / len(LANGS)
SPRITE_W = 13 * CELL

# Height scale is linear in share, floored so a sub-1% language still shows as a
# seedling instead of nothing. The printed figure always carries the real number.
def scale_for(pct):
    return round(max(0.30, 0.30 + 0.70 * (pct / 41.4)), 3)

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
    px, py = SPRITE_W / 2, sprite_h          # pivot: where the stalk enters the soil
    amp = round(1.8 + 3.2 * s, 2)            # taller stalk, more leverage, wider swing
    dur = round(3.2 + 0.5 * i, 2)
    css.append(
        f"@keyframes sw{i}{{0%,100%{{transform:rotate(-{amp}deg)}}50%{{transform:rotate({amp}deg)}}}}"
        f".f{i}{{animation:sw{i} {dur}s ease-in-out infinite;animation-delay:-{round(0.8*i,2)}s;"
        f"transform-origin:{px}px {py}px}}"
    )

    shown = f"{pct:.1f}%" if pct >= 0.1 else "&lt;0.1%"
    fy = pot_y - sprite_h * s + 2.5 * CELL * s
    parts.append(f'<g transform="translate({pot_x:.1f},{fy:.1f}) scale({s})"><g class="f{i}">{inner}</g></g>')
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
                  f'fill="#2f6b29" style="transform-origin:{bx+1.5:.0f}px {GROUND}px"/>')
for k in range(5):
    css.append(f"@keyframes gs{k}{{0%,100%{{transform:rotate(-6deg)}}50%{{transform:rotate(6deg)}}}}"
               f".g{k}{{animation:gs{k} {round(2.4+k*0.35,2)}s ease-in-out infinite;animation-delay:-{round(k*0.45,2)}s}}")

petals = []
SEEDS = [(60,44,'#ffb8d0',13,0),(250,22,'#f7a736',16,-4),(470,70,'#e8503f',14,-8),
         (640,30,'#ffe066',17,-2),(800,62,'#ffb8d0',15,-11),(930,18,'#f7a736',12,-6),
         (150,96,'#ffe6ee',18,-13),(560,110,'#ffe066',14,-5)]
for i,(x,y,col,dur,delay) in enumerate(SEEDS):
    petals.append(f'<rect class="d{i}" x="{x}" y="{y}" width="6" height="6" rx="1" fill="{col}" opacity=".8"/>')
    css.append(
        f"@keyframes dr{i}{{0%{{transform:translate(0,0) rotate(0)}}"
        f"50%{{transform:translate(110px,{GROUND-40-y}px) rotate(180deg)}}"
        f"100%{{transform:translate(240px,{GROUND-10-y}px) rotate(400deg)}}}}"
        f"@keyframes fd{i}{{0%,100%{{opacity:0}}15%,80%{{opacity:.85}}}}"
        f".d{i}{{animation:dr{i} {dur}s linear infinite, fd{i} {dur}s linear infinite;animation-delay:{delay}s}}"
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A pixel-art garden in a night breeze. Each flower is a language used on this GitHub account, drawn at a height proportional to its share of bytes: Python 41.4 percent, HTML 32.8 percent, Jupyter Notebook 13.7 percent, TypeScript 12.2 percent, CSS under one percent.">
<style>
text{{font-family:"Courier New",ui-monospace,monospace;text-anchor:middle}}
.lbl{{fill:#e8eef2;font-size:16px;font-weight:700;letter-spacing:.6px}}
.pct{{fill:#7f949e;font-size:13px}}
.ttl{{fill:#9fd4a8;font-size:14px;letter-spacing:4px}}
{" ".join(css)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#13161b"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="#252b33" stroke-width="2"/>
<text x="{W/2:.0f}" y="30" class="ttl">A GARDEN OF WHAT I WRITE</text>
{"".join(petals)}
<rect x="2" y="{GROUND}" width="{W-4}" height="{H-GROUND-2}" fill="#171f18"/>
<rect x="2" y="{GROUND}" width="{W-4}" height="3" fill="#2f6b29"/>
{"".join(blades)}
<g shape-rendering="crispEdges">{"".join(parts)}</g>
</svg>'''

out = "/Users/aifamaladinaulya/Documents/qa-portfolio/profile-readme/assets/garden.svg"
open(out, "w").write(svg)
print(f"written {len(svg)} bytes")
for label, byts, _ in LANGS:
    pct = 100*byts/TOTAL
    print(f"  {label:18s} {pct:5.1f}%  scale={scale_for(pct)}")
