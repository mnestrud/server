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

## musicme

- current monochrome: png-dark — svg-wrapped PNG, luminance 0.18, 3883 B
- viewBox: `0 0 96 96`
- icon colours: n/a
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/musicme/icon.svg
- output: `music_assistant/providers/musicme/icon_monochrome.svg`

## nugs

- current monochrome: missing — none
- viewBox: `0 0 200 200`
- icon colours: #000, #a8a8a8, #fff, red
- source: https://raw.githubusercontent.com/mnestrud/server/review/provider-dark-icons/music_assistant/providers/nugs/icon.svg
- output: `music_assistant/providers/nugs/icon_monochrome.svg`
- official assets: site SVG logo is white + gradient: https://cdn.nugsdev.net/images/logo-xl.svg (site asset, not a published download)

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
