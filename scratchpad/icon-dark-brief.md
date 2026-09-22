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

## airplay

- why: single-colour #0000ff mark; brand mark, not a plain glyph
- viewBox: `0 0 24 24`
- current colours: #0000ff
- current size: 2681 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/airplay/icon.svg
- output 1: `music_assistant/providers/airplay/icon_dark.svg`
- output 2: `music_assistant/providers/airplay/icon_monochrome.svg` — exists but is an embedded PNG (50591 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/airplay/icon_monochrome.svg
- official assets: Apple HIG says use the white AirPlay icon on dark backgrounds; glyph shipped only as PDF in a .dmg — a white recolour of our mark is the same thing

```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   viewBox="0 0 24 24"
   version="1.1"
   id="svg1"
   sodipodi:docname="icon.svg"
   inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:dc="http://purl.org/dc/elements/1.1/">
  <defs
     id="defs1" />

  <title
     id="title1">AirPlay Audio</title>
  <path
     d="M11.908.183a12 12 0 0 0-8.044 3.172c-4.882 4.475-5.166 12.08-.692 16.962.204.244.448.447.692.692a.315.315 0 0 0 .408-.04l.53-.61a.32.32 0 0 0 0-.448C.53 15.965.243 9.253 4.23 4.982S14.889.427 19.16 4.414s4.555 10.655.568 14.927c-.203.203-.365.407-.568.57a.32.32 0 0 0 0 .447l.53.611a.37.37 0 0 0 .446.04c4.882-4.516 5.166-12.081.692-16.962a11.98 11.98 0 0 0-8.92-3.864m.387 3.518A8.6 8.6 0 0 0 6.143 6c-3.458 3.213-3.66 8.623-.447 12.08.122.123.243.285.406.407a.32.32 0 0 0 .447 0l.53-.61a.32.32 0 0 0 0-.446A7.26 7.26 0 0 1 4.8 12.183c0-3.946 3.212-7.16 7.158-7.16s7.16 3.253 7.16 7.199a7.2 7.2 0 0 1-2.238 5.209.32.32 0 0 0 0 .447l.529.61c.122.121.325.162.447.04a8.6 8.6 0 0 0 .408-12.122 8.5 8.5 0 0 0-5.97-2.705zm-.266 3.316A5.2 5.2 0 0 0 8.34 8.48c-2.075 1.993-2.115 5.247-.122 7.322l.121.123a.32.32 0 0 0 .447 0l.53-.611a.32.32 0 0 0 0-.448 3.8 3.8 0 0 1-1.098-2.683 3.73 3.73 0 0 1 3.742-3.742 3.73 3.73 0 0 1 3.742 3.742c0 1.017-.406 1.951-1.139 2.683a.32.32 0 0 0 0 .448l.53.61a.32.32 0 0 0 .447 0 5.19 5.19 0 0 0 .123-7.321 5.13 5.13 0 0 0-3.633-1.586zm.006 7.744a.6.6 0 0 0-.402.146l-.04.041-7.159 8.055a.506.506 0 0 0 .041.69.44.44 0 0 0 .283.124h14.36a.495.495 0 0 0 .489-.488.46.46 0 0 0-.121-.326l-7.08-8.055a.5.5 0 0 0-.37-.187z"
     id="path1"
     style="fill:#0000ff;fill-opacity:1" />
  <metadata
     id="metadata1">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:title>AirPlay Audio</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
</svg>
```
## fully_kiosk

- why: single-colour #00f mark; brand mark, not a plain glyph
- viewBox: `0 0 135.467 135.467`
- current colours: #00f
- current size: 2902 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/fully_kiosk/icon.svg
- output 1: `music_assistant/providers/fully_kiosk/icon_dark.svg`
- output 2: `music_assistant/providers/fully_kiosk/icon_monochrome.svg` — exists and is fine (white, 2902 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/fully_kiosk/icon_monochrome.svg

```svg
<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="512" height="512" viewBox="0 0 135.467 135.467"><path d="M38.812 134.447c-.657-.325-1.473-1.069-1.907-1.737-.472-.728-.867-1.888-1.048-3.074-.16-1.048-.389-4.734-.51-8.191-.12-3.457-.224-7.25-.231-8.429-.007-1.178.166-4.252.385-6.83.323-3.806.332-5.205.048-7.434-.318-2.494-.292-3.113.287-6.74.41-2.562.675-5.688.74-8.71.056-2.593.109-5.152.117-5.687.01-.535-.17-1.16-.4-1.388-.362-.363-.733-.304-2.959.473-1.399.488-2.818.888-3.154.888a.83.83 0 0 1-.79-.57c-.128-.403.375-1.494 1.714-3.717 1.674-2.779 2.155-3.343 4.124-4.842 1.605-1.222 2.352-2.003 2.667-2.79.24-.6.634-2.376.876-3.944.241-1.568.588-4.716.77-6.994.183-2.279.523-5.172.756-6.429s.669-3.016.968-3.909c.449-1.334.496-1.883.267-3.09-.182-.958-.18-2.16.005-3.462.155-1.096.476-3.102.712-4.456s.565-2.988.73-3.63.616-2.003 1-3.024c.386-1.022 1.246-2.852 1.913-4.069.666-1.216 2.04-3.384 3.055-4.818 1.013-1.434 2.925-3.846 4.248-5.36S56.39 9.06 57.352 8.24s3.101-2.19 4.751-3.042c1.65-.853 4.222-1.97 5.715-2.481 2.155-.739 3.214-.938 5.143-.968 1.335-.02 2.911-.22 3.502-.443.959-.362 1.236-.35 2.582.107 1.447.492 1.577.493 3.212.005 1.248-.372 2.581-.497 4.99-.47 2.45.028 3.775.19 5.216.637 1.312.408 2.247.916 2.915 1.584.59.59 1.062 1.4 1.18 2.026.107.573.122 2.343.033 3.933-.09 1.59-.427 4.111-.75 5.604-.324 1.493-.8 3.293-1.058 4-.259.707-.741 1.584-1.072 1.949-.38.418-.814.613-1.176.528-.316-.074-2.503-.935-4.86-1.912-4.286-1.777-4.286-1.777-6.143-1.158-1.595.531-2.071.577-3.371.325-1.043-.203-2.198-.201-3.714.005-1.21.164-2.972.485-3.915.712s-2.372.626-3.177.886c-.804.26-1.942.805-2.528 1.211s-1.242 1.061-1.458 1.454-1.228 2.45-2.249 4.571c-1.374 2.857-2.118 4.881-2.867 7.805-.556 2.172-1.847 7.593-2.87 12.048-1.023 4.454-2.05 8.556-2.284 9.114s-.424 1.505-.424 2.103.2 1.375.445 1.724c.244.349.679.635.966.635s2.24-.574 4.34-1.276c2.101-.7 4.785-1.425 5.963-1.609 1.179-.183 4.072-.767 6.429-1.296 3.148-.707 4.973-.962 6.878-.962 1.426 0 4.044-.261 5.818-.58 2.769-.5 3.554-.538 5.55-.275 1.49.196 2.958.612 4.089 1.159 1.467.71 1.866 1.065 2.375 2.115.586 1.212.6 1.444.33 5.787-.282 4.524-.282 4.524-1.417 6.516-1.085 1.903-1.179 1.988-2.094 1.901-.527-.05-2.436-.397-4.244-.771a1126 1126 0 0 1-5.634-1.182c-1.987-.425-2.604-.45-4-.163-.908.187-3.58.48-5.937.65s-5.121.434-6.143.587a96 96 0 0 1-3.556.455c-1.029.107-2.308.497-3.243.989-1.374.722-1.837.812-4.18.812-2.369 0-2.695.065-3.223.643-.324.353-.78 1.028-1.014 1.5-.235.471-.623 1.564-.864 2.428-.24.865-.721 2.903-1.068 4.531-.507 2.384-.576 3.232-.353 4.359.224 1.135.118 2.387-.56 6.612-.52 3.239-.78 5.734-.685 6.59.084.758-.097 3.2-.402 5.429a231 231 0 0 0-.862 7.194c-.17 1.728-.415 6.444-.547 10.478-.23 7.08-.265 7.394-.997 8.992-.417.912-.965 1.885-1.218 2.165-.336.371-.889.507-2.058.507-1.02 0-2.014-.206-2.747-.569" style="fill:#00f;stroke-width:1.07986;fill-opacity:1"/></svg>
```
## siriusxm

- why: single-colour #0000eb mark; brand mark, not a plain glyph
- viewBox: `0 0 1536 1542`
- current colours: #0000eb
- current size: 715 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/siriusxm/icon.svg
- output 1: `music_assistant/providers/siriusxm/icon_dark.svg`
- output 2: `music_assistant/providers/siriusxm/icon_monochrome.svg` — exists but uses #0000eb, #ffffff: replace, must be white only
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/siriusxm/icon_monochrome.svg

```svg
<svg version="1.2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1542" width="24" height="25">
	<title>SIRI_BIG copy-svg</title>
	<style>
		.s0 { fill: #0000eb }
	</style>
	<path id="Layer" class="s0" d="m1477.8 829.2c36.1 54.7 57.3 121 57.3 203.4-2.5 303.2-253.7 508.5-794.6 508.5-338 0-709.6-103-740.5-495v-19.3h506.8l-112.1 330.2 369.6-256.8 369.7 256.8-96-283.9c-14.8-28.9-53.4-45-53.4-45-202.2-112-938.9-51.5-938.9-546.6 0-372.7 392.2-481.5 699.3-481.5 321.4 0 698.7 72.7 732.2 459v14.8h-570.5l-141.1-415.2-141.6 415.2h-457.2l255.6 175.7c74.7-29.6 154.6-42.4 234.4-51.5 85.7-9 171.9-10.9 258.2-5.1 72.1 4.5 144.3 14.8 215.1 31.5 63.8 14.8 128.8 31.6 186.7 63.1 65.1 36.1 121.7 81.1 161 141.7z"/>
</svg>
```
## lastfm_recommendations

- why: multi-colour brand mark (black + red)
- viewBox: `0 0 804 447`
- current colours: #d1170e, black
- current size: 2013 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/lastfm_recommendations/icon.svg
- output 1: `music_assistant/providers/lastfm_recommendations/icon_dark.svg`
- output 2: `music_assistant/providers/lastfm_recommendations/icon_monochrome.svg` — none exists: create one

```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
 viewBox="0 0 804 447"
 fill="none"
 version="1.1"
 id="svg1"
 sodipodi:docname="audioscrobbler-icon (1).svg"
 inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)"
 xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
 xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
 xmlns="http://www.w3.org/2000/svg"
 xmlns:svg="http://www.w3.org/2000/svg">
 <defs id="defs1" />

 <path
 d="M354.475 397.74L325.008 317.643C325.008 317.643 277.126 371.046 205.321 371.046C141.781 371.046 96.6749 315.802 96.6749 227.413C96.6749 114.167 153.753 73.6561 209.921 73.6561C290.938 73.6561 316.715 126.135 338.817 193.35L368.284 285.425C397.74 374.725 452.984 446.543 612.264 446.543C726.441 446.543 803.776 411.56 803.776 319.488C803.776 244.911 761.417 206.242 682.234 187.823L623.311 174.938C582.804 165.732 570.836 149.153 570.836 121.535C570.836 90.2306 595.689 71.8148 636.207 71.8148C680.396 71.8148 704.332 88.3894 708.018 127.979L800.09 116.928C792.725 34.0662 735.644 0 641.731 0C558.872 0 477.847 31.3044 477.847 131.662C477.847 194.27 508.231 233.864 584.642 252.276L647.258 267.002C694.213 278.053 709.859 297.386 709.859 324.095C709.859 358.154 676.717 371.966 614.109 371.966C521.12 371.966 482.454 323.17 460.352 255.952L429.969 163.887C391.306 44.193 329.615 0 207.156 0C71.8148 0 0 85.624 0 231.095C0 371.046 71.8148 446.54 200.722 446.54C304.748 446.536 354.475 397.74 354.475 397.74Z"
 fill="black"
 id="path1"
 style="fill:#d1170e;fill-opacity:1" />
</svg>
```
## lastfm_scrobble

- why: multi-colour brand mark (black + red); same logo as lastfm_recommendations
- viewBox: `0 0 804 447`
- current colours: #d1170e, black
- current size: 2125 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/lastfm_scrobble/icon.svg
- output 1: `music_assistant/providers/lastfm_scrobble/icon_dark.svg`
- output 2: `music_assistant/providers/lastfm_scrobble/icon_monochrome.svg` — exists and is fine (white, 1112 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/lastfm_scrobble/icon_monochrome.svg

```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   viewBox="0 0 804 447"
   fill="none"
   version="1.1"
   id="svg1"
   sodipodi:docname="audioscrobbler-icon (1).svg"
   inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs1" />

  <path
     d="M354.475 397.74L325.008 317.643C325.008 317.643 277.126 371.046 205.321 371.046C141.781 371.046 96.6749 315.802 96.6749 227.413C96.6749 114.167 153.753 73.6561 209.921 73.6561C290.938 73.6561 316.715 126.135 338.817 193.35L368.284 285.425C397.74 374.725 452.984 446.543 612.264 446.543C726.441 446.543 803.776 411.56 803.776 319.488C803.776 244.911 761.417 206.242 682.234 187.823L623.311 174.938C582.804 165.732 570.836 149.153 570.836 121.535C570.836 90.2306 595.689 71.8148 636.207 71.8148C680.396 71.8148 704.332 88.3894 708.018 127.979L800.09 116.928C792.725 34.0662 735.644 0 641.731 0C558.872 0 477.847 31.3044 477.847 131.662C477.847 194.27 508.231 233.864 584.642 252.276L647.258 267.002C694.213 278.053 709.859 297.386 709.859 324.095C709.859 358.154 676.717 371.966 614.109 371.966C521.12 371.966 482.454 323.17 460.352 255.952L429.969 163.887C391.306 44.193 329.615 0 207.156 0C71.8148 0 0 85.624 0 231.095C0 371.046 71.8148 446.54 200.722 446.54C304.748 446.536 354.475 397.74 354.475 397.74Z"
     fill="black"
     id="path1"
     style="fill:#d1170e;fill-opacity:1" />
</svg>
```
## heos

- why: multi-colour brand mark (near-black + red)
- viewBox: `0 0 512 512`
- current colours: #040404, #ca2d1a
- current size: 3119 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/heos/icon.svg
- output 1: `music_assistant/providers/heos/icon_dark.svg`
- output 2: `music_assistant/providers/heos/icon_monochrome.svg` — none exists: create one

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" version="1.1"><path d="M 27.500 183.965 C 21.734 185.468, 18.982 186.975, 14.560 191.051 C 6.348 198.621, 6.500 197.395, 6.500 256 C 6.500 297.064, 6.778 308.286, 7.871 311.381 C 10.747 319.523, 21.062 327.504, 29.593 328.187 L 33.500 328.500 33.500 256.014 C 33.500 176.380, 33.991 182.273, 27.500 183.965 M 478 256.066 L 478 329.223 481.750 328.574 C 491.950 326.811, 501.658 318.699, 504.007 309.975 C 504.709 307.366, 504.972 288.366, 504.784 253.767 C 504.503 202.053, 504.477 201.456, 502.294 197.376 C 498.563 190.402, 490.753 185.153, 481.750 183.569 L 478 182.909 478 256.066 M 75.852 224.391 C 67.859 227.246, 60.813 235.766, 58.926 244.858 C 57.452 251.956, 58.216 267.291, 60.287 272.190 C 62.453 277.311, 69.713 284.942, 74.500 287.129 C 76.700 288.134, 80.188 288.966, 82.250 288.978 L 86 289 86 256 L 86 223 82.750 223.044 C 80.963 223.068, 77.858 223.674, 75.852 224.391 M 426 256 L 426 289 429.250 288.990 C 434.014 288.976, 442.023 284.876, 445.889 280.474 C 451.905 273.621, 452.953 269.995, 452.978 255.946 C 452.998 244.428, 452.787 242.965, 450.416 238.207 C 446.014 229.375, 436.884 223, 428.634 223 L 426 223 426 256" stroke="none" fill="#040404" fill-rule="evenodd"/><path d="M 244.500 1.039 C 225.111 5.014, 209.028 20.820, 204.498 40.353 C 203.161 46.116, 202.993 58.330, 203.228 132.250 L 203.500 217.500 206.490 222.899 C 209.917 229.087, 216.792 234.222, 224.050 236.013 C 227.064 236.757, 238.707 237.029, 258.550 236.818 L 288.500 236.500 293.590 233.814 C 299.267 230.819, 304.120 225.803, 306.752 220.213 C 308.373 216.769, 308.500 210.306, 308.500 131 C 308.500 50.876, 308.383 45.043, 306.638 38.231 C 302.325 21.400, 287.148 6.288, 270.081 1.833 C 263.158 0.026, 251.246 -0.344, 244.500 1.039 M 150.760 106.558 C 135.803 110.183, 121.974 121.961, 115.405 136.670 C 111.098 146.313, 110.886 152.644, 111.220 261.500 C 111.567 374.839, 111.183 367.804, 117.683 379.629 C 121.778 387.077, 133.571 398.223, 141.110 401.772 C 146.910 404.501, 157.292 407, 162.832 407 L 165 407 165 256 L 165 105 160.750 105.083 C 158.412 105.129, 153.917 105.793, 150.760 106.558 M 347 256 L 347 407 350.750 406.985 C 356.541 406.962, 366.789 404.236, 372.404 401.223 C 384.761 394.594, 396.596 378.968, 398.995 366.114 C 399.629 362.718, 399.995 321.884, 399.985 255.614 C 399.969 140.883, 400.094 143.551, 394.223 132.587 C 390.721 126.046, 378.954 114.279, 372.413 110.777 C 366.786 107.763, 356.537 105.038, 350.750 105.015 L 347 105 347 256 M 221.882 276.354 C 216.294 278.392, 211.210 281.858, 208.394 285.550 C 202.929 292.715, 202.999 291.476, 203.017 381.409 C 203.036 471.013, 203.107 472.372, 208.319 482.631 C 214.304 494.411, 227.733 506.061, 239.276 509.489 C 258.840 515.299, 279.029 510.254, 293 496.065 C 300.561 488.385, 304.347 481.873, 306.459 472.913 C 308.753 463.180, 308.752 298.383, 306.457 291.879 C 304.633 286.708, 300.217 281.847, 294 278.165 L 289.500 275.500 257.500 275.267 C 233.019 275.090, 224.650 275.345, 221.882 276.354" stroke="none" fill="#ca2d1a" fill-rule="evenodd"/></svg>
```
## somafm

- why: red wordmark; no monochrome variant exists
- viewBox: `0 0 550 154.95`
- current colours: red
- current size: 3655 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/somafm/icon.svg
- output 1: `music_assistant/providers/somafm/icon_dark.svg`
- output 2: `music_assistant/providers/somafm/icon_monochrome.svg` — exists and is fine (white, 3656 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/somafm/icon_monochrome.svg
- official assets: owner allows black or white for B/W use depending on background (https://somafm.com/linktous/logos.html); vector only as EPS

```svg
<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 550 154.95"><path d="M48.354 66.866c-2.848 0-7.69-.57-7.69 3.845 0 2.278 1.709 3.133 3.703 3.987L78.542 90.22c8.829 3.987 13.386 9.54 13.386 19.366 0 13.813-9.399 20.363-22.5 20.363H48.354c-7.12 0-11.962-.285-17.088-4.272-2.564-1.994-6.266-4.557-6.266-7.974 0-3.845 3.276-6.836 7.12-6.836 2.136 0 3.703.713 5.27 2.421 2.42 2.706 6.692 2.99 10.964 2.99h18.512c4.841 0 11.391.428 11.391-7.546 0-3.276-3.987-5.411-7.12-6.835L38.956 87.229c-7.547-3.417-11.961-7.832-11.961-16.66 0-10.823 8.544-17.373 18.796-17.373h23.354c7.547 0 10.68.427 15.806 4.699 2.563 2.136 5.411 3.845 5.411 7.69 0 3.844-3.275 6.834-6.977 6.834-2.563 0-4.13-.996-5.839-2.847-2.278-2.42-4.699-2.706-8.401-2.706zm56.383 11.819c0-9.113 1.852-12.246 8.687-17.8 6.693-5.553 9.825-7.689 19.366-7.689h10.822c9.541 0 12.674 2.136 19.367 7.69 6.835 5.553 8.686 8.686 8.686 17.8v25.774c0 8.97-2.278 12.388-9.398 18.369s-9.968 7.12-18.655 7.12H132.79c-8.686 0-11.534-1.139-18.654-7.12s-9.399-9.398-9.399-18.369zm13.67 25.775c0 2.848.998 4.699 4.985 8.116 2.99 2.563 5.126 3.702 9.398 3.702h10.822c4.272 0 6.408-1.139 9.398-3.702 3.988-3.417 4.985-5.268 4.985-8.116V78.685c0-2.848-.997-4.7-4.985-8.117-2.99-2.563-5.126-3.702-9.398-3.702H132.79c-4.272 0-6.408 1.14-9.398 3.702-3.987 3.418-4.984 5.27-4.984 8.117zm106.366-28.338v44.428c0 4.7-.996 9.4-6.834 9.4-5.839 0-6.835-4.7-6.835-9.4V74.84c0-2.278.284-6.55-3.276-6.55-1.566 0-2.563 1.282-3.702 2.278l-5.98 5.554v44.428c0 4.7-.997 9.4-6.836 9.4-5.838 0-6.835-4.7-6.835-9.4V62.88c0-4.842 1.282-9.684 7.12-9.684 3.418 0 5.696 2.278 6.55 5.411l1.14-.854c3.559-2.706 5.696-4.557 10.394-4.557 5.27 0 9.4 2.563 12.532 6.835l1.14-1.14c4.271-4.271 5.98-5.695 11.96-5.695 4.558 0 8.687 1.993 11.392 5.553 3.418 4.415 3.133 8.402 3.276 13.67l1.424 47.278c.141 4.841-.57 10.252-6.693 10.252-5.553 0-6.692-4.7-6.835-9.256l-1.425-45.14c-.142-2.421.57-7.263-3.133-7.263-1.992 0-4.556 3.418-5.695 4.699zm62.365-9.256c-3.986 0-9.398-.855-9.398-6.835 0-5.839 4.841-6.835 9.398-6.835h18.797c7.12 0 12.246.712 17.657 6.123 5.269 5.269 5.98 9.399 6.123 16.233l1.425 46.423c.141 3.986-1.851 7.974-6.409 7.974-3.56 0-7.12-2.99-6.977-6.835l-9.399 4.841c-3.845 1.994-3.986 1.994-8.4 1.994h-13.102c-6.122 0-10.536-.712-15.52-4.841-5.697-4.7-7.12-9.683-7.12-16.804v-5.98c0-6.55 1.566-10.68 6.693-15.237 4.699-4.13 9.967-5.127 15.947-5.127h29.334v-3.133c0-10.252-2.278-11.96-12.104-11.96zm-.142 28.765c-3.702 0-9.113.997-9.113 5.98v9.114c0 4.557 5.553 5.553 8.828 5.553h15.094l15.094-7.831v-2.99c0-7.548-2.136-9.826-9.683-9.826zm122.793-28.765h-3.845c-3.987 0-9.398-.855-9.398-6.835 0-5.839 4.842-6.835 9.398-6.835h3.845v-1.851c0-7.832.427-13.528 6.55-19.509 6.55-6.265 12.673-6.835 21.075-6.835h9.256c4.699 0 9.968.427 9.968 6.835 0 5.839-4.699 6.835-9.399 6.835H436.56c-9.256 0-13.101 1.851-13.101 11.82v2.705h12.103c4.558 0 9.4.996 9.4 6.835 0 5.98-5.412 6.835-9.4 6.835H423.46v53.684c0 4.7-.997 9.4-6.835 9.4-5.839 0-6.835-4.7-6.835-9.4zm88.567 9.256v44.428c0 4.7-.998 9.4-6.836 9.4-5.839 0-6.835-4.7-6.835-9.4V74.84c0-2.278.285-6.55-3.274-6.55-1.568 0-2.564 1.282-3.703 2.278l-5.982 5.554v44.428c0 4.7-.996 9.4-6.834 9.4-5.839 0-6.835-4.7-6.835-9.4V62.88c0-4.842 1.281-9.684 7.12-9.684 3.418 0 5.696 2.278 6.55 5.411l1.14-.854c3.56-2.706 5.695-4.557 10.394-4.557 5.27 0 9.398 2.563 12.531 6.835l1.14-1.14c4.271-4.271 5.98-5.695 11.96-5.695 4.558 0 8.687 1.993 11.393 5.553 3.417 4.415 3.132 8.402 3.275 13.67l1.424 47.278c.143 4.841-.57 10.252-6.693 10.252-5.553 0-6.692-4.7-6.835-9.256l-1.424-45.14c-.142-2.421.57-7.263-3.132-7.263-1.994 0-4.558 3.418-5.697 4.699z" style="fill:red"/></svg>
```
## neteasecloudmusic

- why: dark red mark; existing monochrome is black too
- viewBox: `0 0 1024 1024`
- current colours: #DD001B
- current size: 2091 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/neteasecloudmusic/icon.svg
- output 1: `music_assistant/providers/neteasecloudmusic/icon_dark.svg`
- output 2: `music_assistant/providers/neteasecloudmusic/icon_monochrome.svg` — exists and is fine (white, 1939 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/neteasecloudmusic/icon_monochrome.svg

```svg
<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg t="1775808516095" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5352" xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200"><path d="M512 32c265.12 0 480 214.88 480 480 0 265.088-214.88 480-480 480-265.088 0-480-214.912-480-480C32 246.848 246.912 32 512 32z m82.08 173.568c-51.84 17.152-76.736 65.44-61.856 120.32l5.344 20.192c-11.2 2.432-22.208 5.696-32.928 9.824-50.656 19.52-90.848 62.816-104.896 113.024a153.696 153.696 0 0 0-5.088 55.04 137.92 137.92 0 0 0 57.536 100.576 121.504 121.504 0 0 0 103.264 17.6 120.96 120.96 0 0 0 63.68-42.56c24.736-32.288 32.096-74.752 20.8-119.52-4.16-16.32-9.344-34.368-14.4-51.904l-5.376-18.976c21.44 5.376 41.184 16.032 57.44 31.04 56 52.288 66.784 142.368 25.088 209.536-36.608 59.008-107.936 97.088-181.664 97.088a225.76 225.76 0 0 1-225.536-225.472c0-28.992 5.696-57.696 16.832-84.448a221.664 221.664 0 0 1 41.856-65.6 223.712 223.712 0 0 1 81.408-56.416A31.712 31.712 0 0 0 412.064 256a299.52 299.52 0 0 0-25.696 11.808 289.504 289.504 0 0 0-100 86.432 286.56 286.56 0 0 0-54.304 167.136c0 159.296 129.6 288.896 288.96 288.896 95.2 0 187.648-49.856 235.552-127.072 58.304-93.888 43.232-215.584-35.712-289.344-32.32-30.208-74.368-47.872-118.784-51.776-2.304-8.96-5.888-22.592-8.64-32.832-2.08-7.584-3.104-16.16-0.864-23.808a31.808 31.808 0 0 1 38.4-21.44c4.416 1.184 8.608 3.264 12.256 6.048 3.84 2.88 6.848 6.624 10.368 9.888a31.744 31.744 0 0 0 49.856-37.664l-0.64-1.056a65.312 65.312 0 0 0-14.4-16.448 100.48 100.48 0 0 0-53.376-23.392 96.128 96.128 0 0 0-40.96 4.224z m-40.224 201.92c3.36 12.416 7.04 25.344 10.752 38.176 4.928 17.28 9.888 34.432 13.824 49.92 4.576 18.176 6.624 44.192-9.664 65.472a57.056 57.056 0 0 1-30.24 19.936 58.464 58.464 0 0 1-50.144-8.544 73.92 73.92 0 0 1-30.528-53.952 89.6 89.6 0 0 1 2.944-32.416c8.8-31.36 34.304-58.528 66.624-71.008 8.672-3.36 17.536-5.856 26.432-7.584z" fill="#DD001B" p-id="5353"></path></svg>
```
## nugs

- why: red + black + white + grey mark
- viewBox: `0 0 200 200`
- current colours: #000, #a8a8a8, #fff, red
- current size: 2618 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/nugs/icon.svg
- output 1: `music_assistant/providers/nugs/icon_dark.svg`
- output 2: `music_assistant/providers/nugs/icon_monochrome.svg` — none exists: create one
- official assets: site SVG logo is white + gradient: https://cdn.nugsdev.net/images/logo-xl.svg (site asset, not a published download)

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" fill="none" viewBox="0 0 200 200"><mask id="a" width="148" height="35" x="0" y="0" maskUnits="userSpaceOnUse"><path fill="#fff" fill-rule="evenodd" d="M0 34.485h148V0H0Z" clip-rule="evenodd"/></mask><g mask="url(#a)" transform="translate(12.94 9.505)scale(5.23404)"><mask id="b" width="34" height="35" x="0" y="0" maskUnits="userSpaceOnUse"><path fill="#fff" fill-rule="evenodd" d="M0 .204h33.267v34.171H0Z" clip-rule="evenodd"/></mask><g mask="url(#b)"><path fill="red" fill-rule="evenodd" d="M0 17.29c0 9.437 7.446 17.086 16.633 17.086s16.634-7.65 16.634-17.086S25.82.204 16.633.204 0 7.854 0 17.29" clip-rule="evenodd"/></g><path fill="#000" fill-rule="evenodd" d="M26.585 9.528c-.215-1.603-1.117-3.052-2.382-3.87-1.236-.8-3.111-.618-4.478-.48-.678.068-1.395.222-2.111.425-1.11.02-2.35.482-3.367.809-.811.262-2.194.639-2.879 1.143-.471.349-.761.77-.94 1.238-.952 1.67-.93 3.123-1.047 5.286-.04.746-1.203 3.836.302 4.378q.236.084.495.135c.18.447.4.876.675 1.274.028.042.062.078.09.118.156.404.019.01.156.404.615 1.775-1.154 2.281 1.747 2.478a13 13 0 0 0 2.28-.046c1.832-.065 3.645-.46 4.492.988.358 2.164-1.357 2.678-3.468 3.033-1.319.154-2.905.234-4.822.234H3l1.215 1.623h7.113c11.06 0 12.48-2.8 13.505-7.408l.02-.09v-.123c.843-1.377 2.926-2.538 2.99-4.365-.668.67-1.234-7.002-1.258-7.184" clip-rule="evenodd"/><path fill="#000" fill-rule="evenodd" d="M23.735 24.037q.028-.181-.003-.371-.008.185.003.37" clip-rule="evenodd"/><path fill="#fff" fill-rule="evenodd" d="M9.233 14.351c1.116-.246 2.308-.585 3.219-1.36.41-.349 1.147-1.253 1.74-1.16 1.086.172.44 1.471-.23 1.721-.457.17-.99.041-1.457.144-.46.101-.894.345-1.338.518-.554.216-1.35.647-1.934.326" clip-rule="evenodd"/><path fill="#a8a8a8" fill-rule="evenodd" d="M15.876 4.808c-.756.171-1.287.621-1.662 1.472l.007.132c2.235-.114 6.092.919 7.27 3.497l1.485-.716c-1.282-2.805-4.537-4.063-7.1-4.385" clip-rule="evenodd"/><path fill="#fff" fill-rule="evenodd" d="M28.858 13.366c0 2.66-1.954 4.814-4.366 4.814-2.41 0-4.364-2.155-4.364-4.814 0-2.658 1.954-4.814 4.364-4.814s4.366 2.156 4.366 4.814" clip-rule="evenodd"/><path fill="#000" fill-rule="evenodd" d="M24.494 9.036c-2.148 0-3.895 1.942-3.895 4.33s1.747 4.33 3.894 4.33 3.895-1.942 3.895-4.33-1.747-4.33-3.895-4.33m0 9.627c-2.666 0-4.835-2.376-4.835-5.297s2.169-5.297 4.835-5.297 4.836 2.376 4.836 5.297-2.17 5.297-4.836 5.297" clip-rule="evenodd"/><path fill="#000" fill-rule="evenodd" d="M26.985 13.442c0 .881-.649 1.596-1.448 1.596s-1.447-.715-1.447-1.596.649-1.596 1.447-1.596c.8 0 1.448.715 1.448 1.596" clip-rule="evenodd"/></g></svg>
```
## theaudiodb

- why: grey #454545 body + white; decide whether to lighten the grey or go white
- viewBox: `0 0 916 916`
- current colours: #454545, #fff
- current size: 4421 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/theaudiodb/icon.svg
- output 1: `music_assistant/providers/theaudiodb/icon_dark.svg`
- output 2: `music_assistant/providers/theaudiodb/icon_monochrome.svg` — exists but is an embedded PNG (22168 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/theaudiodb/icon_monochrome.svg
- official assets: site header SVG is white + blue, suited to dark: https://www.theaudiodb.com/images/logo_simple.svg (8.5 KB, site asset)

```svg
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   viewBox="0 0 916 916"
   version="1.1"
   id="svg2"
   sodipodi:docname="tadb-optimized-5kb.svg"
   inkscape:version="1.3.2 (091e20e, 2023-11-25, custom)"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs2" />

  <path
     fill="#454545"
     fill-rule="evenodd"
     d="M248.0 721.5L209.0 718.5L184.0 713.5L164.0 707.5L126.0 690.5L110.0 680.5L92.0 666.5L66.5 639.0L55.5 622.0L47.5 605.0L39.5 574.0L38.5 554.0L41.5 530.0L47.5 510.0L58.5 488.0L74.5 466.0L91.0 449.5L110.0 434.5L126.0 424.5L146.0 414.5L178.5 403.0L186.5 365.0L199.5 330.0L219.5 293.0L247.5 256.0L270.0 233.5L299.0 210.5L325.0 194.5L360.0 178.5L401.0 166.5L425.0 162.5L452.0 160.5L494.0 162.5L518.0 166.5L559.0 178.5L578.0 186.5L611.0 204.5L647.0 231.5L672.5 257.0L701.5 296.0L719.5 330.0L727.5 350.0L734.5 372.0L740.5 402.0L748.0 406.5L773.0 414.5L795.0 425.5L826.0 447.5L851.5 475.0L860.5 489.0L872.5 513.0L878.5 537.0L878.5 579.0L870.5 608.0L857.5 632.0L842.5 652.0L826.0 668.5L812.0 679.5L795.0 690.5L768.0 703.5L744.0 711.5L721.0 716.5L696.0 718.5L688.0 720.5L671.0 719.5L668.5 717.0L668.5 383.0L665.5 366.0L659.5 347.0L648.5 325.0L631.5 302.0L604.0 276.5L581.0 261.5L561.0 251.5L537.0 242.5L519.0 237.5L490.0 232.5L439.0 231.5L400.0 237.5L373.0 245.5L338.0 261.5L322.0 271.5L304.0 285.5L287.5 302.0L270.5 325.0L262.5 340.0L254.5 362.0L249.5 389.0L249.5 718.0L248.0 721.5Z"
     id="path1" />
  <path
     fill="#fff"
     fill-rule="evenodd"
     d="M285.0 757.5L233.0 757.5L214.0 755.5L182.0 749.5L146.0 738.5L120.0 727.5L85.0 706.5L67.0 692.5L44.5 670.0L25.5 644.0L14.5 623.0L6.5 601.0L1.5 575.0L1.5 541.0L4.5 523.0L10.5 503.0L22.5 477.0L33.5 460.0L49.5 440.0L75.0 416.5L105.0 395.5L124.0 387.5L146.5 375.0L154.5 343.0L165.5 313.0L177.5 288.0L197.5 256.0L216.5 232.0L245.0 203.5L264.0 187.5L301.0 163.5L356.0 139.5L402.0 128.5L434.0 124.5L484.0 124.5L531.0 131.5L573.0 143.5L616.0 162.5L652.0 186.5L673.0 203.5L701.5 232.0L720.5 256.0L740.5 288.0L752.5 313.0L763.5 343.0L771.5 377.0L812.0 396.5L844.0 418.5L871.5 445.0L882.5 459.0L894.5 478.0L903.5 497.0L909.5 515.0L914.5 540.0L914.5 574.0L910.5 600.0L894.5 639.0L875.5 666.0L846.0 694.5L822.0 711.5L787.0 730.5L749.0 744.5L720.0 751.5L682.0 756.5L633.0 756.5L632.5 383.0L624.5 354.0L609.5 328.0L592.0 308.5L569.0 290.5L545.0 277.5L514.0 266.5L480.0 260.5L459.0 259.5L424.0 262.5L405.0 266.5L381.0 274.5L360.0 284.5L340.0 297.5L327.0 308.5L309.5 328.0L301.5 340.0L290.5 365.0L286.5 383.0L285.5 396.0L285.0 757.5ZM248.5 721.0L249.5 391.0L251.5 389.0L251.5 380.0L255.5 361.0L261.5 344.0L273.5 322.0L284.5 307.0L299.0 291.5L318.0 275.5L338.0 262.5L365.0 249.5L388.0 241.5L427.0 233.5L466.0 231.5L505.0 235.5L531.0 241.5L549.0 247.5L581.0 262.5L605.0 278.5L620.0 291.5L634.5 307.0L651.5 332.0L662.5 358.0L668.5 386.0L668.5 717.0L671.0 719.5L689.0 720.5L719.0 717.5L747.0 711.5L765.0 705.5L805.0 685.5L833.0 663.5L845.5 650.0L858.5 632.0L869.5 611.0L875.5 594.0L879.5 574.0L879.5 542.0L875.5 522.0L869.5 505.0L858.5 484.0L845.5 466.0L824.0 444.5L795.0 424.5L775.0 414.5L741.5 403.0L734.5 370.0L727.5 348.0L717.5 324.0L703.5 298.0L684.5 270.0L665.5 248.0L645.0 228.5L626.0 213.5L603.0 198.5L571.0 182.5L530.0 168.5L500.0 162.5L481.0 160.5L427.0 161.5L402.0 165.5L375.0 172.5L341.0 185.5L310.0 202.5L292.0 214.5L272.0 230.5L245.5 257.0L229.5 277.0L215.5 298.0L198.5 331.0L191.5 348.0L183.5 374.0L179.5 392.0L179.5 401.0L177.0 403.5L154.0 410.5L130.0 421.5L106.0 436.5L92.0 447.5L73.5 466.0L59.5 485.0L48.5 506.0L41.5 527.0L38.5 545.0L38.5 570.0L41.5 588.0L46.5 604.0L56.5 625.0L63.5 636.0L73.5 649.0L92.0 667.5L123.0 689.5L140.0 698.5L162.0 707.5L186.0 714.5L212.0 719.5L232.0 721.5L248.5 721.0Z"
     id="path2" />
</svg>
```
## deezer

- why: single brand colour #A238FF, too dark on #121212
- viewBox: `0 0 48 48`
- current colours: #A238FF
- current size: 2016 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/deezer/icon.svg
- output 1: `music_assistant/providers/deezer/icon_dark.svg`
- output 2: `music_assistant/providers/deezer/icon_monochrome.svg` — exists and is fine (white, 2013 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/deezer/icon_monochrome.svg
- official assets: brand rule: logo is white on dark / black on light; press-kit zip may hold the white file: https://newsroom-deezer.com/wp-content/uploads/2025/07/DEEZER-LOGO.zip

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd" >
<path fill-rule="evenodd" clip-rule="evenodd" d="M41.0955 7.32313C41.5396 4.74914 42.1912 3.13054 42.913 3.12744H42.9146C44.2606 3.13208 45.3517 8.7454 45.3517 15.6759C45.3517 22.6063 44.259 28.2243 42.9115 28.2243C42.3591 28.2243 41.8494 27.2704 41.4389 25.6719C40.7903 31.5233 39.4443 35.5459 37.8862 35.5459C36.6806 35.5459 35.5986 33.1296 34.8722 29.3188C34.3762 36.5662 33.1279 41.708 31.6689 41.708C30.7533 41.708 29.9185 39.6705 29.3005 36.3529C28.5573 43.2014 26.8405 48 24.8382 48C22.836 48 21.1162 43.2029 20.376 36.3529C19.7625 39.6705 18.9278 41.708 18.0075 41.708C16.5486 41.708 15.3033 36.5662 14.8043 29.3188C14.0779 33.1296 12.999 35.5459 11.7903 35.5459C10.2337 35.5459 8.88621 31.5249 8.23763 25.6719C7.83017 27.2751 7.31741 28.2243 6.76497 28.2243C5.41745 28.2243 4.32478 22.6063 4.32478 15.6759C4.32478 8.7454 5.41745 3.12744 6.76497 3.12744C7.48833 3.12744 8.13538 4.75068 8.58405 7.32313C9.30283 2.88473 10.4703 0 11.7903 0C13.3576 0 14.7158 4.07975 15.3583 10.0038C15.987 5.69216 16.9408 2.94348 18.0091 2.94348C19.5061 2.94348 20.7789 8.34964 21.2505 15.8908C22.1371 12.0243 23.4205 9.59876 24.8413 9.59876C26.2621 9.59876 27.5455 12.0259 28.4306 15.8908C28.9037 8.34964 30.1749 2.94348 31.672 2.94348C32.7387 2.94348 33.691 5.69216 34.3228 10.0038C34.9637 4.07975 36.3219 0 37.8892 0C39.2047 0 40.3767 2.88628 41.0955 7.32313ZM0.837891 14.4417C0.837891 11.3436 1.45748 8.83142 2.22204 8.83142C2.9866 8.83142 3.60619 11.3436 3.60619 14.4417C3.60619 17.5397 2.9866 20.0519 2.22204 20.0519C1.45748 20.0519 0.837891 17.5397 0.837891 14.4417ZM46.0693 14.4417C46.0693 11.3436 46.6888 8.83142 47.4534 8.83142C48.218 8.83142 48.8376 11.3436 48.8376 14.4417C48.8376 17.5397 48.218 20.0519 47.4534 20.0519C46.6888 20.0519 46.0693 17.5397 46.0693 14.4417Z" fill="#A238FF"/>
</svg>
```
## filesystem_onedrive

- why: single brand colour #0078D4
- viewBox: `0 0 24 24`
- current colours: #0078D4
- current size: 1403 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/filesystem_onedrive/icon.svg
- output 1: `music_assistant/providers/filesystem_onedrive/icon_dark.svg`
- output 2: `music_assistant/providers/filesystem_onedrive/icon_monochrome.svg` — exists and is fine (white, 1403 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/filesystem_onedrive/icon_monochrome.svg
- official assets: Microsoft: icon must be used in full colour; no white variant public

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="#0078D4" d="M18.21 10.29Q19 10.34 19.7 10.68 20.39 11 20.9 11.57 21.41 12.12 21.71 12.83 22 13.54 22 14.34 22 15.18 21.68 15.92 21.36 16.66 20.8 17.21 20.25 17.76 19.5 18.08 18.78 18.41 17.94 18.41H7Q5.97 18.41 5.06 18 4.15 17.61 3.47 16.94 2.79 16.26 2.4 15.35 2 14.44 2 13.41 2 12.59 2.26 11.83 2.5 11.08 3 10.45 3.44 9.82 4.08 9.35 4.72 8.88 5.5 8.63 5.87 8.5 6.21 8.5 6.56 8.43 6.93 8.41H6.94Q7.37 7.75 7.95 7.23 8.5 6.71 9.2 6.34 9.87 6 10.62 5.78 11.37 5.59 12.16 5.59 13.22 5.59 14.2 5.94 15.18 6.29 16 6.91 16.8 7.53 17.37 8.39 17.95 9.26 18.21 10.29M12.16 6.84Q11.05 6.84 10.06 7.3 9.06 7.75 8.36 8.6 8.73 8.7 9.07 8.85 9.4 9 9.73 9.2L13.71 11.58L16 10.62Q16.21 10.53 16.44 10.45 16.67 10.38 16.92 10.33 16.68 9.55 16.21 8.91 15.74 8.27 15.11 7.81 14.5 7.35 13.73 7.1 13 6.84 12.16 6.84M4 15.66L12.27 12.18L9.08 10.26Q8.59 9.97 8.06 9.81 7.5 9.66 6.95 9.66 6.19 9.66 5.5 9.96 4.84 10.26 4.34 10.77 3.84 11.29 3.54 11.97 3.25 12.65 3.25 13.41 3.25 14 3.45 14.59 3.64 15.19 4 15.66M17.94 17.16Q18.41 17.16 18.84 17 19.27 16.86 19.64 16.58L13.61 13L5.03 16.59Q5.47 16.86 5.97 17 6.47 17.16 7 17.16M20.45 15.61Q20.75 15 20.75 14.34 20.75 13.7 20.5 13.17 20.26 12.65 19.85 12.28 19.43 11.91 18.88 11.71 18.32 11.5 17.7 11.5 17.35 11.5 17 11.6 16.66 11.68 16.33 11.81 16 11.93 15.67 12.08 15.35 12.23 15.04 12.37Z" />
</svg>
```
## storytel

- why: single brand colour #ff501c
- viewBox: `92.57 211.12 134.5 150`
- current colours: #ff501c
- current size: 477 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/storytel/icon.svg
- output 1: `music_assistant/providers/storytel/icon_dark.svg`
- output 2: `music_assistant/providers/storytel/icon_monochrome.svg` — exists and is fine (white, 474 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/storytel/icon_monochrome.svg

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="92.57 211.12 134.5 150">
  <defs>
    <style>
      .cls-2 {         fill: #ff501c;       }
    </style>
  </defs>
  <path class="cls-2" d="M226.16,283.12c5.73-31.35-13.38-59.4-43.28-68.71-53.09-16.54-90.72,32.1-90.31,81.14.36,39.62,8.83,65.97,8.86,65.97-.39-1.17,10.03-6.65,11.23-7.29,4.08-2.1,8.35-3.8,12.71-5.25,8.94-2.96,18.22-4.86,27.41-6.96,28.75-6.57,59.63-18.94,70.61-48.79,1.23-3.35,2.15-6.76,2.77-10.17v.06Z"/>
</svg>
```
## bbc_sounds

- why: orange tones
- viewBox: `0 0 246 246`
- current colours: #a03207, #d24716, #f96200, #f96306, #fa6200
- current size: 4012 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/bbc_sounds/icon.svg
- output 1: `music_assistant/providers/bbc_sounds/icon_dark.svg`
- output 2: `music_assistant/providers/bbc_sounds/icon_monochrome.svg` — none exists: create one
- official assets: BBC requires written consent for any logo use; no assets published
## pandora

- why: blue tones
- viewBox: `10.5 8 32 32`
- current colours: #0288d1, #3231c7, #b11e93, #db1a58, #e4273e, #f2494c
- current size: 2642 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/pandora/icon.svg
- output 1: `music_assistant/providers/pandora/icon_dark.svg`
- output 2: `music_assistant/providers/pandora/icon_monochrome.svg` — exists but is an embedded PNG (9097 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/pandora/icon_monochrome.svg

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="10.5 8 32 32"><path fill="#f2494c" d="M36.5 28.2a13 13 0 0 1-3 2.1l-.1.1a11 11 0 0 1-3.1 1q-1 .2-2.1.2h-4l-.4-.3q-.3-1-1.4-2.2l-.6-.6a8 8 0 0 0-2.7-2q-.5 0-.8-.4-.9-.4-1.9-1.5c-1.2-1.1-1.5-1.9-2-2.7a8 8 0 0 0-1.4-2.2V9q.1-1 1.1-1.1h3l.7 1.4q.4 1 2 2.7c1.5 1.7 1.9 1.5 2.6 1.9q1.1.3 2.7 1.9t2 2.7a8 8 0 0 0 1.8 2.7q1.7 1.5 2.8 1.9t2.7 1.9q1.5 1.7 1.9 2.7z"/><path fill="#db1a58" d="M13 8v32h8a2 2 0 0 0 2-2v-6h6s11-1 11-11S34 8 29 8z"/><path fill="#3231c7" d="M16.5 40H13v-2.3c1.2 1.2 2 1.5 2.8 2q.3 0 .7.3"/><path fill="#e4273e" d="M39.8 23c0 .3-.3 5.8-7.7 8.3-.5-.3-1.9-.8-2.5-1.4-1.2-1.2-1.5-2-2-2.7a9 9 0 0 0-4.5-4.6l-.5-.3q-.9-.4-2.2-1.6-1.6-1.7-2-2.7t-1.8-2.7q-1.7-1.6-2.8-2L13 13V8h10.6c1.2 1.2 2 1.6 2.8 2s1.5.7 2.7 1.9 1.5 2 2 2.7q.3 1 1.8 2.7c1.2 1.2 2 1.5 2.7 2q1.1.3 2.7 1.8l1.5 2"/><path fill="#f2494c" d="M36.7 28.8C33.9 31 31.9 32 29 32l-4.9-.1a13 13 0 0 0-2.3-3.4 8 8 0 0 0-2.7-2q-.5 0-.8-.4c-.6-.3-.5-1.6-1.3-2.3q-1.6-1.7-2.2-2.7c-.3-.7-1-.5-1.8-1.4V8h4l.8 1.4q.4 1 2 2.7c1.5 1.7 1.9 1.5 2.6 1.9q1.1.3 2.7 1.9t2 2.7a8 8 0 0 0 1.8 2.7q1.7 1.5 2.8 1.9t2.7 1.9q1.5 1.7 1.9 2.7z"/><path fill="#b11e93" d="M23 38a2 2 0 0 1-2 2h-8V28l1 1q.8 1.1 1.1 2 .4 1.1 2 2.7c1 1.2 1.9 1.6 2.6 2q1.1.3 2.7 1.8z"/><path fill="#3231c7" d="M23 35.6V38a2 2 0 0 1-2 2s.8-1.8-.5-3q-.6-.6-1.4-1l-1.7-1.4a11 11 0 0 1-2.7-4.2l-.5-1c-.1-.3-1-1.1-1.2-1.4l1.6 1.1 1.1 1.7.1.2q1.2 1.5 2.6 2.3h.1q.8.6 1.5.8a9 9 0 0 1 3 1.5"/><path fill="#3231c7" d="M40 21c0 .2 0 2.3-.6 4l-.3-.4-.6-.9-1.3-1.6q-.5-.8-1.4-1.3L34 19.6a11 11 0 0 1-2.9-3.7l-.5-1.4-.3-.6q-.4-1-1-1.8l1.4 1.5 1 1.5.2.3q1.2 1.5 2.9 2.4l.2.2 2 .7q1.2.6 2.1 1.4c.4.2.9.9.9.9"/><path fill="#3231c7" d="M37.7 27.8c-.1.1-1.3 1.3-2.3 2l-.3-.7-.7-1.4a9 9 0 0 0-2.2-2.4l-1.6-1.1a10 10 0 0 1-2.4-3.1l-.4-1q-.1-.5-.4-.8l-.8-1.6q.7.7 1.2 1.5l1 1.3v.2a9 9 0 0 0 2.8 2.4l1.4.6 1.9 1 1.5 1.4q.8.8 1.3 1.7"/><path fill="#e4273e" d="M28.4 29.4Q27 28 26 27.7c-.7-.4-.8-1-1.8-2-1-1.1-1.8-2.7-2.1-3.4s-.4-1-1.4-2.1q-1.4-1.4-2.4-1.7t-2.7-1.8a9 9 0 0 1-1.9-2.3L13 13v8q.7.5 1.3.7l2 1.8.2.2c1 1 1.5 2.7 1.9 3.4q.3 1 1.7 2.4t2.4 1.7l.8.7 3.7.1h3c-.3-.5-.9-2-1.6-2.6"/><path fill="#0288d1" d="M27 32h-4v.2l-.5-.4q-1-.5-1.8-1.3-1.5-1.5-2.4-3.4l-.2-.6-.5-1.3-.8-1.2-.3-.4L18 25q.7.8 1.2 1.7l.4.5a10 10 0 0 0 2.7 2.2l1.2.5q1 .3 2 1z"/><path fill="#0288d1" d="M33.3 31c-.8.6-3 1-3.3 1l-.2-.4a9 9 0 0 0-2.5-2.6l-1.8-1.3a12 12 0 0 1-2.7-3.6l-.5-1.2q0-.4-.3-.7l-1-1.8 1.5 1.5 1 1.6.2.2q1.2 1.6 3 2.5l1.8.8a9 9 0 0 1 3.8 2.8z"/><path fill="#b11e93" d="M38.9 14.4a10 10 0 0 0-4.3-5c.5 1 .8 2 2.3 3.4q1.1 1.2 2 1.6"/><path fill="#3231c7" d="M16.4 40H13v-2.5q1.6 1.8 2.6 2z"/></svg>
```
## yandex_station

- why: purple-to-blue gradient
- viewBox: `0 0 370 370`
- current colours: #4A26FF, #C926FF, url
- current size: 671 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/yandex_station/icon.svg
- output 1: `music_assistant/providers/yandex_station/icon_dark.svg`
- output 2: `music_assistant/providers/yandex_station/icon_monochrome.svg` — none exists: create one
- official assets: Yandex: white badge exists but gated to certified devices

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 370 370" width="370" height="370">
  <defs>
    <linearGradient x1="0%" y1="100%" x2="100%" y2="0%" id="g">
      <stop stop-color="#C926FF" offset="0%"/>
      <stop stop-color="#4A26FF" offset="100%"/>
    </linearGradient>
  </defs>
  <path fill="url(#g)" fill-rule="nonzero" d="M185,370 C82.827,370 0,287.173 0,185 C0,82.827 82.827,0 185,0 C287.173,0 370,82.827 370,185 C370,287.173 287.173,370 185,370 Z M100.288,244.708 C113.569,257.924 148.946,265.86 185,265.999 C221.053,265.86 256.431,257.924 269.712,244.708 C302.709,211.874 222.5,86.08 185.041,85.897 C147.5,86.08 67.291,211.874 100.288,244.708 Z"/>
</svg>
```
## ibroadcast

- why: dark brown + greys
- viewBox: `0 0 40 40`
- current colours: rgb
- current size: 3620 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/ibroadcast/icon.svg
- output 1: `music_assistant/providers/ibroadcast/icon_dark.svg`
- output 2: `music_assistant/providers/ibroadcast/icon_monochrome.svg` — exists and is fine (white, 3682 B): keep it
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/ibroadcast/icon_monochrome.svg
- official assets: official dark 'Powered by' SVG (multi-grey, no modification allowed): https://help.ibroadcast.com/ibroadcast-dark-compact-powered.svg — candidate for icon_dark; monochrome must still be white

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 40 40" version="1.1">
<g id="surface1">
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(12.156863%,7.843137%,5.882353%);fill-opacity:1;" d="M 0 0 C 13.199219 0 26.398438 0 40 0 C 40 13.199219 40 26.398438 40 40 C 26.800781 40 13.601562 40 0 40 C 0 26.800781 0 13.601562 0 0 Z M 0 0 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(81.176471%,81.960784%,81.960784%);fill-opacity:1;" d="M 16.300781 8.300781 C 28.957031 8.300781 28.957031 8.300781 31 10.101562 C 31.058594 10.144531 31.117188 10.191406 31.175781 10.234375 C 31.914062 10.875 32.53125 12.082031 32.683594 13.046875 C 32.796875 14.652344 32.660156 16.140625 31.699219 17.5 C 31.242188 18.019531 30.746094 18.472656 30.199219 18.898438 C 30.289062 18.9375 30.375 18.976562 30.46875 19.019531 C 31.875 19.664062 32.964844 20.589844 33.53125 22.0625 C 34.136719 23.761719 33.878906 25.832031 33.125 27.445312 C 32.21875 29.089844 30.761719 30.183594 29 30.800781 C 25.082031 31.898438 19.320312 31.199219 16.300781 31.199219 C 16.300781 23.644531 16.300781 16.085938 16.300781 8.300781 Z M 16.300781 8.300781 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(81.568627%,82.352941%,82.352941%);fill-opacity:1;" d="M 7.601562 18.398438 C 9.316406 18.398438 11.03125 18.398438 12.800781 18.398438 C 12.800781 22.625 12.800781 26.847656 12.800781 31.199219 C 11.085938 31.199219 9.367188 31.199219 7.601562 31.199219 C 7.601562 26.976562 7.601562 22.753906 7.601562 18.398438 Z M 7.601562 18.398438 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(44.705882%,44.313725%,46.27451%);fill-opacity:1;" d="M 11.675781 10.5625 C 12.46875 11.050781 12.910156 11.734375 13.199219 12.601562 C 13.328125 13.628906 13.058594 14.394531 12.4375 15.21875 C 11.867188 15.839844 11.257812 16.109375 10.417969 16.152344 C 9.644531 16.167969 9.046875 16.039062 8.398438 15.601562 C 8.308594 15.539062 8.214844 15.480469 8.117188 15.417969 C 7.503906 14.804688 7.175781 14.058594 7.148438 13.1875 C 7.164062 12.375 7.445312 11.730469 7.960938 11.105469 C 8.941406 10.175781 10.460938 9.996094 11.675781 10.5625 Z M 11.675781 10.5625 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(12.54902%,8.235294%,6.27451%);fill-opacity:1;" d="M 22.300781 21.898438 C 22.9375 21.890625 23.574219 21.882812 24.230469 21.875 C 24.429688 21.871094 24.628906 21.867188 24.832031 21.863281 C 25.890625 21.851562 26.84375 21.855469 27.707031 22.542969 C 28.125 23.097656 28.179688 23.617188 28.101562 24.300781 C 27.925781 24.925781 27.65625 25.347656 27.101562 25.699219 C 26.171875 26.136719 25.132812 26.03125 24.136719 26.019531 C 23.53125 26.011719 22.925781 26.007812 22.300781 26 C 22.300781 24.648438 22.300781 23.292969 22.300781 21.898438 Z M 22.300781 21.898438 "/>
<path style=" stroke:none;fill-rule:nonzero;fill:rgb(13.72549%,9.411765%,7.45098%);fill-opacity:1;" d="M 22.300781 13.398438 C 23.0625 13.382812 23.0625 13.382812 23.835938 13.367188 C 23.996094 13.363281 24.152344 13.359375 24.316406 13.355469 C 25.289062 13.34375 26.042969 13.453125 26.761719 14.15625 C 27.011719 14.777344 27 15.421875 26.773438 16.050781 C 26.398438 16.585938 26.070312 16.828125 25.425781 16.953125 C 25.089844 17 24.769531 17.011719 24.429688 17.007812 C 24.316406 17.007812 24.203125 17.007812 24.089844 17.007812 C 23.949219 17.007812 23.808594 17.007812 23.664062 17.007812 C 22.988281 17.003906 22.988281 17.003906 22.300781 17 C 22.300781 15.8125 22.300781 14.625 22.300781 13.398438 Z M 22.300781 13.398438 "/>
</g>
</svg>
```
## gpodder

- why: dark grey + purple + white
- viewBox: `0 0 64 64`
- current colours: #4d4d4d, #974fa4, #fff
- current size: 5184 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/gpodder/icon.svg
- output 1: `music_assistant/providers/gpodder/icon_dark.svg`
- output 2: `music_assistant/providers/gpodder/icon_monochrome.svg` — none exists: create one
## lrclib

- why: embedded PNG, mostly near-black: needs re-drawing as a vector
- viewBox: `0 0 200 200`
- current colours: n/a
- current size: 8050 B (embedded PNG)
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/lrclib/icon.svg
- output 1: `music_assistant/providers/lrclib/icon_dark.svg`
- output 2: `music_assistant/providers/lrclib/icon_monochrome.svg` — none exists: create one
## musicme

- why: embedded PNG, dark: needs re-drawing as a vector
- viewBox: `0 0 96 96`
- current colours: n/a
- current size: 3228 B (embedded PNG)
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/musicme/icon.svg
- output 1: `music_assistant/providers/musicme/icon_dark.svg`
- output 2: `music_assistant/providers/musicme/icon_monochrome.svg` — exists but is an embedded PNG (3883 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/musicme/icon_monochrome.svg
## internet_archive

- why: embedded PNG, near-black: needs re-drawing as a vector
- viewBox: `0 0 135.46665 135.46665`
- current colours: n/a
- current size: 5434 B (embedded PNG)
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/internet_archive/icon.svg
- output 1: `music_assistant/providers/internet_archive/icon_dark.svg`
- output 2: `music_assistant/providers/internet_archive/icon_monochrome.svg` — exists but is an embedded PNG (26877 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/internet_archive/icon_monochrome.svg
- official assets: official colour-agnostic glyph: https://raw.githubusercontent.com/internetarchive/ia-icons/master/svg/ia-logo.svg (AGPL-3.0 repo) — recolour that rather than redraw
## radioparadise

- why: embedded PNG, dark: needs re-drawing as a vector
- viewBox: `0 0 135.46666 135.46667`
- current colours: n/a
- current size: 151616 B (embedded PNG)
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/radioparadise/icon.svg
- output 1: `music_assistant/providers/radioparadise/icon_dark.svg`
- output 2: `music_assistant/providers/radioparadise/icon_monochrome.svg` — exists but is an embedded PNG (13500 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/radioparadise/icon_monochrome.svg
- official assets: single-colour sigil mask exists: https://radioparadise.com/safari-pinned-tab.svg (#000, recolour to white)
## musiccast

- why: embedded PNG, dark: needs re-drawing as a vector
- viewBox: `0 0 135.46665 135.46665`
- current colours: n/a
- current size: 4538 B (embedded PNG)
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/musiccast/icon.svg
- output 1: `music_assistant/providers/musiccast/icon_dark.svg`
- output 2: `music_assistant/providers/musiccast/icon_monochrome.svg` — exists but is an embedded PNG (29623 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/musiccast/icon_monochrome.svg
- official assets: Yamaha: logos only on request (requestforlogos@yamaha.com)
## mpd

- why: embedded PNG, mid-dark: needs re-drawing as a vector
- viewBox: `0 0 41.010416 41.010417`
- current colours: n/a
- current size: 5290 B (embedded PNG)
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/mpd/icon.svg
- output 1: `music_assistant/providers/mpd/icon_dark.svg`
- output 2: `music_assistant/providers/mpd/icon_monochrome.svg` — exists but is an embedded PNG (118548 B): replace with a vector
- current monochrome file: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/mpd/icon_monochrome.svg

# Part 2 — monochrome only

These providers keep their icon.svg and need only `icon_monochrome.svg`: pure white on transparent, vector, <= 5 KB, same viewBox as icon.svg. The current file (if any) is unusable for the reason given.

## ai_radio

- current monochrome: missing — none
- viewBox: `-5 -5 34 34`
- icon colours: #18bcf2, #efb04d, #f7d562, #ffffff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/ai_radio/icon.svg
- output: `music_assistant/providers/ai_radio/icon_monochrome.svg`

## amplipi

- current monochrome: colour — #000000, #c01824, #f0f0f0, #ffffff, 1882 B
- viewBox: `0 0 320 320`
- icon colours: #000000, #c01824, #f0f0f0
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/amplipi/icon.svg
- output: `music_assistant/providers/amplipi/icon_monochrome.svg`

## ariacast_receiver

- current monochrome: missing — none
- viewBox: `0 0 24 24`
- icon colours: #010101, #4a6097, #4c6298, #50649a, #50659b, #fafafa, #fff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/ariacast_receiver/icon.svg
- output: `music_assistant/providers/ariacast_receiver/icon_monochrome.svg`

## builtin

- current monochrome: colour — #18bcf2, #f2f4f9, #ffffff, 11360 B
- viewBox: `0 0 240 240`
- icon colours: #18bcf2, #f2f4f9, #ffffff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/builtin/icon.svg
- output: `music_assistant/providers/builtin/icon_monochrome.svg`

## coverartarchive

- current monochrome: colour — #20656c, #264346, #579ca0, #d3562c, #eb743b, #fffedb, 28026 B
- viewBox: `-2.5 5 150 150`
- icon colours: #20656c, #264346, #579ca0, #d3562c, #eb743b, #fffedb
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/coverartarchive/icon.svg
- output: `music_assistant/providers/coverartarchive/icon_monochrome.svg`

## filesystem_nfs

- current monochrome: colour — #000000, #1a1a1a, #4d4d4d, #595959, #676767, #696969, #737373, #878787, #999999, #a9a9a9, #b2b4b7, #b3b3b3, #cecece, #d7d7d7, #d8d8d8, #d9d9d9, #ebdba6, #f2d26a, #f3af61, #f4f4f4, #f6b650, #fc8723, #ff7512, #ff841f, #ff8521, #ff8a36, #ff9445, #ffab43, #ffb047, #ffb06c, #ffdbaa, #ffdd70, #fff3cc, #ffffff, url(#xmlid_10_), url(#xmlid_11_), url(#xmlid_12_), url(#xmlid_13_), url(#xmlid_14_), url(#xmlid_15_), url(#xmlid_16_), url(#xmlid_17_), url(#xmlid_18_), url(#xmlid_19_), url(#xmlid_1_), url(#xmlid_20_), url(#xmlid_21_), url(#xmlid_22_), url(#xmlid_23_), url(#xmlid_25_), url(#xmlid_26_), url(#xmlid_2_), url(#xmlid_3_), url(#xmlid_4_), url(#xmlid_5_), url(#xmlid_6_), url(#xmlid_7_), url(#xmlid_8_), url(#xmlid_9_), 24586 B
- viewBox: `0 0 128 128`
- icon colours: #262626, #464646, #515151, #737373, #aeaeae, #f3af61, #fff, gray
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/filesystem_nfs/icon.svg
- output: `music_assistant/providers/filesystem_nfs/icon_monochrome.svg`

## filesystem_smb

- current monochrome: colour — #000000, #1a1a1a, #4d4d4d, #595959, #676767, #696969, #737373, #878787, #999999, #a9a9a9, #b2b4b7, #b3b3b3, #cecece, #d7d7d7, #d8d8d8, #d9d9d9, #ebdba6, #f2d26a, #f3af61, #f4f4f4, #f6b650, #fc8723, #ff7512, #ff841f, #ff8521, #ff8a36, #ff9445, #ffab43, #ffb047, #ffb06c, #ffdbaa, #ffdd70, #fff3cc, #ffffff, url(#xmlid_10_), url(#xmlid_11_), url(#xmlid_12_), url(#xmlid_13_), url(#xmlid_14_), url(#xmlid_15_), url(#xmlid_16_), url(#xmlid_17_), url(#xmlid_18_), url(#xmlid_19_), url(#xmlid_1_), url(#xmlid_20_), url(#xmlid_21_), url(#xmlid_22_), url(#xmlid_23_), url(#xmlid_25_), url(#xmlid_26_), url(#xmlid_2_), url(#xmlid_3_), url(#xmlid_4_), url(#xmlid_5_), url(#xmlid_6_), url(#xmlid_7_), url(#xmlid_8_), url(#xmlid_9_), 24586 B
- viewBox: `0 0 128 128`
- icon colours: #262626, #2dcaf2, #464646, #515151, #737373, #aeaeae, #b3f2ff, #fff, gray
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/filesystem_smb/icon.svg
- output: `music_assistant/providers/filesystem_smb/icon_monochrome.svg`

## hass

- current monochrome: colour — #18bcf2, #f2f4f9, #ffffff, 2671 B
- viewBox: `0 0 240 240`
- icon colours: #18BCF2, #F2F4F9
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/hass/icon.svg
- output: `music_assistant/providers/hass/icon_monochrome.svg`

## hass_players

- current monochrome: colour — #18bcf2, #f2f4f9, #ffffff, 2671 B
- viewBox: `0 0 240 240`
- icon colours: #18BCF2, #F2F4F9
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/hass_players/icon.svg
- output: `music_assistant/providers/hass_players/icon_monochrome.svg`

## itunes_artwork

- current monochrome: missing — none
- viewBox: `0 0 512 512`
- icon colours: #17c9ff, #2da8ff, #a04cff, #e5e3e3, #ff4f63, #ff5b57, url
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/itunes_artwork/icon.svg
- output: `music_assistant/providers/itunes_artwork/icon_monochrome.svg`

## itunes_podcasts

- current monochrome: colour — #832bc1, #f452ff, #ffffff, url(#xmlid_2_), 5913 B
- viewBox: `0 0 512 512`
- icon colours: #832BC1, #F452FF, #ffffff, url
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/itunes_podcasts/icon.svg
- output: `music_assistant/providers/itunes_podcasts/icon_monochrome.svg`

## jellyfin

- current monochrome: colour — #00a4dc, #aa5cc3, #ffffff, url(#linear, 2658 B
- viewBox: `0 0 512 512`
- icon colours: #00a4dc, #aa5cc3, url
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/jellyfin/icon.svg
- output: `music_assistant/providers/jellyfin/icon_monochrome.svg`

## listenbrainz_scrobble

- current monochrome: missing — none
- viewBox: `9 0 144 144`
- icon colours: #353070, #eb743b, #fffedb
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/listenbrainz_scrobble/icon.svg
- output: `music_assistant/providers/listenbrainz_scrobble/icon_monochrome.svg`

## musicbrainz

- current monochrome: oversize — white, 6285 B
- viewBox: `-2.5 5 150 150`
- icon colours: #9d356d, #ba478f, #d3562c, #eb743b, #fffedb
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/musicbrainz/icon.svg
- output: `music_assistant/providers/musicbrainz/icon_monochrome.svg`

## nts

- current monochrome: missing — none
- viewBox: `0 0 26 26`
- icon colours: #000, #fff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/nts/icon.svg
- output: `music_assistant/providers/nts/icon_monochrome.svg`

## openai_compatible

- current monochrome: missing — none
- viewBox: `0 0 24 24`
- icon colours: #7c5cff, #ffffff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/openai_compatible/icon.svg
- output: `music_assistant/providers/openai_compatible/icon_monochrome.svg`

## plex

- current monochrome: colour — #282a2d, #e5a00d, #ffffff, 1649 B
- viewBox: `0 0 122.88 122.88`
- icon colours: #282A2D, #E5A00D
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/plex/icon.svg
- output: `music_assistant/providers/plex/icon_monochrome.svg`

## plex_connect

- current monochrome: colour — #18b6d2, #282a2d, #e5a00d, #ffffff, 3225 B
- viewBox: `0 0 122.88 122.88`
- icon colours: #18B6D2, #282A2D, #E5A00D
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/plex_connect/icon.svg
- output: `music_assistant/providers/plex_connect/icon_monochrome.svg`

## radiobrowser

- current monochrome: oversize — white, 10001 B
- viewBox: `0 0 135.46666 135.46667`
- icon colours: n/a
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/radiobrowser/icon.svg
- output: `music_assistant/providers/radiobrowser/icon_monochrome.svg`

## roku_media_assistant

- current monochrome: colour — #4e2270, #652c90, #fefefe, #ffffff, 60961 B
- viewBox: `0 0 512 512`
- icon colours: #50206f, #662d91, #7b3bb0, #fff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/roku_media_assistant/icon.svg
- output: `music_assistant/providers/roku_media_assistant/icon_monochrome.svg`

## smart_playlist

- current monochrome: missing — none
- viewBox: `0 0 24 24`
- icon colours: #18bcf2, #ffffff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/smart_playlist/icon.svg
- output: `music_assistant/providers/smart_playlist/icon_monochrome.svg`

## soundcloud

- current monochrome: colour — #f30, #f80, #ffffff, url(#a), 3720 B
- viewBox: `0 0 2499.9979999999996 1386.6950000000002`
- icon colours: #f30, #f80, url
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/soundcloud/icon.svg
- output: `music_assistant/providers/soundcloud/icon_monochrome.svg`

## tunein

- current monochrome: colour — #14d8cc, #1c203c, #ffffff, 2846 B
- viewBox: `0 0 122.88 122.88`
- icon colours: #14D8CC, #1C203C
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/tunein/icon.svg
- output: `music_assistant/providers/tunein/icon_monochrome.svg`

## webdav

- current monochrome: colour — #000000, #1a1a1a, #4d4d4d, #595959, #676767, #696969, #737373, #878787, #999999, #a9a9a9, #b2b4b7, #b3b3b3, #cecece, #d7d7d7, #d8d8d8, #d9d9d9, #ebdba6, #f2d26a, #f3af61, #f4f4f4, #f6b650, #fc8723, #ff7512, #ff841f, #ff8521, #ff8a36, #ff9445, #ffab43, #ffb047, #ffb06c, #ffdbaa, #ffdd70, #fff3cc, #ffffff, url(#xmlid_10_), url(#xmlid_11_), url(#xmlid_12_), url(#xmlid_13_), url(#xmlid_14_), url(#xmlid_15_), url(#xmlid_16_), url(#xmlid_17_), url(#xmlid_18_), url(#xmlid_19_), url(#xmlid_1_), url(#xmlid_20_), url(#xmlid_21_), url(#xmlid_22_), url(#xmlid_23_), url(#xmlid_25_), url(#xmlid_26_), url(#xmlid_2_), url(#xmlid_3_), url(#xmlid_4_), url(#xmlid_5_), url(#xmlid_6_), url(#xmlid_7_), url(#xmlid_8_), url(#xmlid_9_), 24597 B
- viewBox: `0 0 128 128`
- icon colours: #262626, #464646, #515151, #737373, #aeaeae, #b57aff, #c998f5, #fff, gray
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/webdav/icon.svg
- output: `music_assistant/providers/webdav/icon_monochrome.svg`

## yandex_smarthome

- current monochrome: missing — none
- viewBox: `0 0 33.866665 33.866667`
- icon colours: n/a
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/yandex_smarthome/icon.svg
- output: `music_assistant/providers/yandex_smarthome/icon_monochrome.svg`

## ytmusic

- current monochrome: colour — #ff0000, #ffffff, 1954 B
- viewBox: `0 0 24 24`
- icon colours: #FF0000, white
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/ytmusic/icon.svg
- output: `music_assistant/providers/ytmusic/icon_monochrome.svg`
