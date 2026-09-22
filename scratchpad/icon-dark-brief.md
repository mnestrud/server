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
## bbc_sounds

- why: orange tones
- viewBox: `0 0 246 246`
- current colours: #a03207, #d24716, #f96200, #f96306, #fa6200
- current size: 4012 B
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/bbc_sounds/icon.svg
- output 1: `music_assistant/providers/bbc_sounds/icon_dark.svg`
- output 2: `music_assistant/providers/bbc_sounds/icon_monochrome.svg` — none exists: create one
- official assets: BBC requires written consent for any logo use; no assets published
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

## nugs

- current monochrome: missing — none
- viewBox: `0 0 200 200`
- icon colours: #000, #a8a8a8, #fff, red
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/nugs/icon.svg
- output: `music_assistant/providers/nugs/icon_monochrome.svg`
- official assets: site SVG logo is white + gradient: https://cdn.nugsdev.net/images/logo-xl.svg (site asset, not a published download)

## openai_compatible

- current monochrome: missing — none
- viewBox: `0 0 24 24`
- icon colours: #7c5cff, #ffffff
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/openai_compatible/icon.svg
- output: `music_assistant/providers/openai_compatible/icon_monochrome.svg`

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

## soundcloud

- current monochrome: colour — #f30, #f80, #ffffff, url(#a), 3720 B
- viewBox: `0 0 2499.9979999999996 1386.6950000000002`
- icon colours: #f30, #f80, url
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/soundcloud/icon.svg
- output: `music_assistant/providers/soundcloud/icon_monochrome.svg`

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

## yandex_station

- current monochrome: missing — none
- viewBox: `0 0 370 370`
- icon colours: #4A26FF, #C926FF, url
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/yandex_station/icon.svg
- output: `music_assistant/providers/yandex_station/icon_monochrome.svg`
- official assets: Yandex: white badge exists but gated to certified devices

## ytmusic

- current monochrome: colour — #ff0000, #ffffff, 1954 B
- viewBox: `0 0 24 24`
- icon colours: #FF0000, white
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/ytmusic/icon.svg
- output: `music_assistant/providers/ytmusic/icon_monochrome.svg`
