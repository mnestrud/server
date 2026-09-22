# Brief: icon_dark.svg for Music Assistant providers (backlog#158)

Music Assistant shows each provider's logo on light and dark surfaces. Providers can ship an
`icon_dark.svg` next to `icon.svg`; the UI picks it on the dark theme. The providers below have
logos drawn in colours that all but disappear on a dark background. Produce, per provider:

1. `icon_dark.svg` — the logo for dark surfaces: white, or a lightened brand colour; may keep
   several colours.
2. `icon_monochrome.svg` — a single-colour version, **pure white (`#fff`) on transparent**, no
   other colours, no greys, no opacity tricks. The UI shows it as-is on dark surfaces and
   CSS-inverts it (`filter: invert(1)`) on light ones, so anything that is not white breaks.
   Skip it only where the per-provider entry says the existing one is fine.

## Rules for every file

- Same `viewBox` as the source `icon.svg`; same geometry wherever the source is a vector
  (the existing 20 dark variants in the repo are the default file with black swapped to white).
- Plain vector SVG, **5 KB or less** (repo lint fails above that). No embedded raster images,
  no editor metadata (`sodipodi`, `inkscape`, `metadata`), no `<text>` (fonts are not available).
- Transparent background. Must read clearly on `#121212` at 16 px, 24 px and 48 px.
- No `currentColor` and no CSS variables: the file is served as a `data:` URI, so those resolve
  to black. Use literal colours.
- Keep the brand's identity: white or a lightened brand colour, not a redesign.
- Filename `icon_dark.svg`; drop it in the output path given per provider.

Review page with today's rendering on dark for each provider:
https://htmlpreview.github.io/?https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/scratchpad/icon-compare.html

Survey of owner-published assets (what can be reused instead of redrawn): https://github.com/mnestrud/server/blob/review/provider-dark-icons/scratchpad/logo-research.md

# Part 1 — dark + monochrome


# Part 2 — monochrome only

These providers keep their icon.svg and need only `icon_monochrome.svg`: pure white on transparent, vector, <= 5 KB, same viewBox as icon.svg. The current file (if any) is unusable for the reason given.
