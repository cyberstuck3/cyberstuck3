# Design direction: garden profile README

Recorded after the fact. The first version of this artwork was built without
this file, which is the process failure that prompted the review. The direction
below was supplied by the owner; where a value was chosen by the agent instead,
it says so and is open to override.

## Design Read

> Reading this as: a personal GitHub profile header for recruiters and
> collaborators, in the owner's supplied pixel-art language,
> dial **ENERGY 2 / RHYTHM 1 / MOTION 2**.

- **ENERGY 2.** The page is a professional profile, not an agency portfolio. The
  artwork should be the one thing that says hello; everything under it is a
  table and plain prose.
- **RHYTHM 1.** Five pots on one baseline, evenly spaced, deliberately uniform.
  The variation that carries meaning is flower height, so varying anything else
  would compete with the data.
- **MOTION 2.** The owner asked for wind. Continuous motion is therefore the
  brief, not a default, and the hierarchy is: flowers lead, grass whispers,
  a few petals cross the frame.

## Direction supplied by the owner

1. Garden theme, flowers representing the code types used on GitHub.
2. Visual language taken from a supplied reference image: pixel art, terracotta
   pots, dark panel, one labelled flower per language.
3. Flowers move as if blown by wind.
4. The more of a language, the larger its flower.

Flower-to-language mapping also comes from that reference image: rose for
Python, bougainvillea for HTML, sunflower for the notebook work, sakura for
TypeScript, daisy for CSS.

## Chosen by the agent, open to override

- **Palette.** Six hues, one per flower, plus green and terracotta. This exceeds
  the usual 2-3 core colours because here colour *is* the encoding: each hue
  identifies a language, taken from the reference image. Restraint would destroy
  the information.
- **Type.** Courier New with a monospace stack, at 0.3px tracking. Picked
  because the labels sit under pixel art and a monospace face holds a grid
  without pretending to be a pixel font. A real pixel face would be better and
  is not used only because an external font cannot load inside an SVG served
  through GitHub's image proxy.
- **Transparent panel, two themes.** The reference image is dark, but a dark
  rectangle pasted onto a GitHub profile reads as a foreign block, and a white
  one would glare for anyone reading in dark mode. The panel is therefore
  removed entirely and the artwork sits on GitHub's own canvas. Two SVGs are
  generated and swapped with `<picture>` and `prefers-color-scheme`, differing
  only in label, percentage, soil and grass colour. Flower and pot hues stay
  identical across both, because those carry the encoding.
- **Height scale.** Linear in share of bytes, floored at 0.30 so a sub-1%
  language is a visible seedling rather than nothing. The floor is stated in the
  README and the real figure is printed under every flower.

## Perceivability rule for the sprites

A flower counts as perceivable on a canvas when **either** its outline **or**
its body clears 3:1 against that canvas. On white the dark outline carries the
silhouette, because the bloom's body is bright. On GitHub's dark canvas the
bright body carries it, and the outline merging into the background is fine.
Testing the outline alone reports false failures on dark; testing the body
alone reports false failures on light.

Measured for all five on both canvases: lowest margin is the bougainvillea at
3.20:1 via its mid tone on white, everything else is above 4:1.

## Known limits

**`prefers-reduced-motion` inside the SVG does not work where this ships.**
Chromium does not evaluate user-preference media queries inside an SVG loaded
through `<img>`, which is exactly how GitHub renders it. The in-file
`@media (prefers-reduced-motion: reduce)` block is kept because it works when
the file is opened directly, but it cannot be relied on. A static variant of
each theme is generated and selected by the host page's `<picture>`, which does
see the preference. Verified across all four combinations of colour scheme and
motion preference.

**No layout-shift reservation on the hero image.** GitHub's markdown CSS is
`max-width: 100%` with no `height: auto`, so an `<img>` carrying both `width`
and `height` is squashed on a phone: measured 1.17 instead of 3.27 at 390px.
Keeping the aspect ratio means dropping the `height` attribute, which costs the
pre-load height reservation that R-40 asks for. A permanently distorted image
for every mobile reader is the worse failure, so the ratio wins. Mitigated by
run-length encoding the artwork: 43% fewer nodes, 37% smaller files.

## Identity motif

The pot. Every language sits in the same terracotta pot on the same soil line,
so the only thing that differs between them is how tall the thing growing out of
it is. That is the whole argument of the piece in one repeated shape.

## Reasons, one line each (R-31)

- **Why a garden:** the owner asked for one, and growth is the natural metaphor for a quantity that changes as repositories do.
- **Why one baseline:** a shared ground line makes height comparable at a glance; staggered pots would make the data unreadable.
- **Why no title inside the artwork:** the README heading directly above it already names the piece, so a title in the SVG was duplication.
- **Why flowers swing wider than grass:** a taller stalk has more leverage in the same breeze, and the motion hierarchy keeps the eye on the data.
- **Why the percentage is printed:** the floor on the daisy means the smallest flower is not to scale, so the number has to carry the truth the drawing cannot.
- **Why terracotta and green are the only shared colours:** they are the constants; every other hue is a variable carrying a language's identity.
- **Why the panel is transparent rather than white:** white blends in GitHub's light theme and glares in its dark one; transparent blends in both.
- **Why the daisy gained a dark outline:** on a white canvas a white flower disappears, and it was the only sprite of the five without an edge, so the outline fixes an art inconsistency and a visibility failure at once.
- **Why every flower is centred on its pot axis:** the scaled sprite was previously translated to the pot's left edge, so anything below full size drifted left; centring makes height the only variable the eye reads.
- **Why four SVG files instead of one:** the host page is the only place that can read colour-scheme and motion preferences, so each combination needs its own file for `<picture>` to choose between.
- **Why the static variant drops the drifting petals:** a petal frozen mid-air is a stray square; the ones that read as wind only read that way while moving.
- **Why the drifting petals are theme-aware:** fixed tints measured 1.3 to 2.0 against white, so three of the four were invisible in light mode; each theme now takes the end of the ramp that its canvas can show.
- **Why the sunflower and sakura gained outlines:** their edges measured 1.66:1 and 2.54:1 on white, below the 3:1 graphics threshold, so their silhouettes dissolved into a light page.
