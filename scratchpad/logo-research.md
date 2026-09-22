# Official logo assets — do the brand owners publish a dark / monochrome variant?

Researched 2026-09-22. "verified" = the URL was fetched; otherwise seen in search results only.
Purpose: don't redraw what the owner already ships. Anything reused still has to land as a
plain vector SVG ≤ 5 KB in the provider folder.

## Batch 1

| provider | official asset page | dark-bg variant | monochrome | direct file | terms |
|---|---|---|---|---|---|
| airplay, airplay_receiver | https://developer.apple.com/design/resources/ (verified); HIG https://developer.apple.com/design/human-interface-guidelines/airplay | yes — HIG: use the white AirPlay icon on dark backgrounds; black/white/custom-colour icon, shipped as PDF glyph in a .dmg, no SVG | yes (same glyph) | https://devimages-cdn.apple.com/design/resources/download/Glyph-AirPlay.dmg (not fetched); unofficial black SVG on Commons: https://upload.wikimedia.org/wikipedia/commons/6/64/AirPlay_Audio_logo.svg | Apple trademark guidelines; "Works with AirPlay" badge is MFi-only |
| fastmcp_server | https://github.com/jlowin/fastmcp/tree/main/docs/assets/brand (verified) | yes — `wordmark-white.png` (PNG only), `favicon-dark.svg` | effectively yes (white wordmark) | https://raw.githubusercontent.com/jlowin/fastmcp/main/docs/assets/brand/favicon-dark.svg | Apache-2.0 repo, trademark excluded |
| nicovideo | https://blog.nicovideo.jp/niconews/188110.html → Niconi Commons logo pack; guideline PDF https://site.nicovideo.jp/term/guideline/commons/logo/niconico/guideline_niconico.pdf (exists, not parsed) | unverified (JS site, PDF unparsed) | unverified | material page https://commons.nicovideo.jp/works/nc296557 | Niconi Commons licence + guideline PDF |
| orf_radiothek | none — app renamed "ORF Sound" 2022-09-13 (https://sound.orf.at); no press/logo page found | no | no | unofficial old wordmark: https://upload.wikimedia.org/wikipedia/commons/4/43/ORF_RADIOTHEK.svg | nothing published |
| wikipedia | https://foundation.wikimedia.org/wiki/Legal:Wikimedia_trademarks (verified) → Commons Category:Logos of Wikimedia | yes, SVG: `Wikipedia_logo_v2_(white).svg`, `Wikipedia-logo-v2-en-negative-white.svg` | yes: `Wikipedia-logo-v2-bw_(White).svg`; `Wikipedia's_W.svg` (black W) | https://upload.wikimedia.org/wikipedia/commons/f/fe/Wikipedia-logo-v2-bw_%28White%29.svg ; https://upload.wikimedia.org/wikipedia/commons/5/5a/Wikipedia%27s_W.svg (verified) | CC BY-SA 3.0; WMF trademark policy |
| fully_kiosk | none (https://www.fully-kiosk.com/ verified, no brand section) | no | no | app icon PNG only | nothing published |
| siriusxm | https://corporate.siriusxm.com/media-assets (verified) | no — black and blue wordmark/icon, PNG only | black PNG icon | `.../SiriusXM ICON BLACK RGB.png` (not fetched); stray old SVG https://www.siriusxm.com/sxm/uxstyleguide/svg/Sirius_XM_Radio_Logo.svg | trademarks, no licence on site |
| lastfm_recommendations, lastfm_scrobble | none — /about/resources redirects, /about/press 404 (verified) | no | no | footer logo PNG only | nothing published |
| heos | https://assets.denon.com/heosbuiltin/index.html (verified) — one PNG | no white/reversed set | no | https://assets.denon.com/heosbuiltin/heos_logo1.png | no terms on page |

## Batch 3

| provider | official asset page | dark-bg variant | monochrome | direct file | terms |
|---|---|---|---|---|---|
| yandex_station | corporate logo rules https://yandex.com/company/general_info/logotype_rules (verified); "Works with Alice" badge rules https://yandex.ru/dev/dialogs/smart-home/doc/en/works-with-alice-rules (verified) | badge has a white-on-transparent version, files not downloadable (certified devices only); no Alice/Station product logo download | badge black version, same gate | unofficial colour Alice icon: https://upload.wikimedia.org/wikipedia/commons/d/d2/Alisa_Yandex.svg | non-commercial with link; badge needs certification |
| ibroadcast | https://help.ibroadcast.com/en/developer/branding (verified) | yes — "Powered by iBroadcast" Light and Dark SVGs | no (multi-grey) | https://help.ibroadcast.com/ibroadcast-dark-compact-powered.svg (verified; fills #58595B/#8C9398/#939598/#DCDDDE) | must be shown unmodified |
| gpodder | none; app icon in repo | no | no (multicolour gradients) | https://raw.githubusercontent.com/gpodder/gpodder/master/share/icons/hicolor/scalable/apps/gpodder.svg (verified) | GPL-3.0 repo icon |
| lrclib | none; homepage repo has only a PNG | no | no | https://raw.githubusercontent.com/tranxuanthang/lrclib-homepage/main/src/assets/lrclib.png (verified, 5.8 KB) | MIT repos |
| internet_archive | no brand page; logos in IA repos https://github.com/internetarchive/ia-icons (AGPL-3.0) and openlibrary; Commons Category:Internet_Archive_logos (verified) | yes — white wide wordmark SVG | yes — all IA logo SVGs are single-colour; ia-icons glyph inherits colour via CSS class | glyph: https://raw.githubusercontent.com/internetarchive/ia-icons/master/svg/ia-logo.svg (verified, 27×30); white wide: https://upload.wikimedia.org/wikipedia/commons/2/2a/Internet_Archive_logo_wide_white.svg | Commons PD-shape + trademark notice; repos AGPL-3.0 |
| musicme | https://www.musicme.com/presse/ (unverified — site returns 403 to every fetch) | unknown | unknown | none | could not verify | <!-- codespell:ignore presse -->
| radioparadise | none (SPA returns the same shell for every path) | no — nav logo is grey #666667 + gold #f0b23e | partial — /safari-pinned-tab.svg is a single-colour (#000) sigil-only mask | https://radioparadise.com/rpassets/images/logo/logo_2022_nav_244x64.svg (verified, 8.4 KB); https://radioparadise.com/safari-pinned-tab.svg (verified) | no published terms |
| musiccast | Yamaha trademark guidelines https://www.yamaha.com/paragon/trademarkguidelines/ (verified); logos only via requestforlogos@yamaha.com or dealer media library | no public white file (page PNGs only, unverified colour) | no | https://www.yamaha.com/US/MusicCast/MC_Updates/images/musiccast_logo.png (page asset, not a sanctioned download) | written permission required |
| mpd | none; logo in source repo | no | no (multicolour #003d88/#00b4ed/#444040 + gradients) | https://raw.githubusercontent.com/MusicPlayerDaemon/MPD/master/mpd.svg (verified) | GPL-2.0 repo logo |

## Batch 2

| provider | official asset page | dark-bg variant | monochrome | direct file | terms |
|---|---|---|---|---|---|
| somafm | https://somafm.com/logos/ + usage guide https://somafm.com/linktous/logos.html (verified) | partial — red-on-transparent is the intended dark form; black or white allowed for B/W "depending on background", but only black PNG published; vector is EPS/PDF only | yes — `SomaFM_logo_black_1000.png` | https://somafm.com/logos/SomaFM-logo-red400trans.png ; https://somafm.com/logos/EPS/SomaFM%20Logo%20Red%20on%20Transparent.eps ; usage PDF https://somafm.com/logos/SomaFM_logousage.pdf | press/media use; registered TM, don't alter |
| neteasecloudmusic | none (music.163.com/about, ir.music.163.com verified — no media kit) | no | no | none | none found |
| nugs | none | site's own SVG logos are white + gradient (drawn for dark UI), not a published asset | no | https://cdn.nugsdev.net/images/logo-xl.svg (site asset) | none published |
| theaudiodb | none (no press page, no attribution requirement) | site header SVG is white + blue #6599cd, suited to dark | no | https://www.theaudiodb.com/images/logo_simple.svg (verified, 8.5 KB) | none published |
| deezer | https://deezerbrand.com/ (Frontify, JS-only) ; press kit https://newsroom-deezer.com/press-kit/ (verified) | likely — press kit "Logos" zip (73 KB, contents not inspected); brand rule: "always white on a dark background or black on a white background" | effectively yes (white/black rule) | https://newsroom-deezer.com/wp-content/uploads/2025/07/DEEZER-LOGO.zip | API apps must show the logo; guidelines https://developers.deezer.com/guidelines/logo mandatory |
| filesystem_onedrive | https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks (verified) → Microsoft 365 trademark guidelines PDF: use the icon in full colour; don't use app icons decoratively | only via FastTrack branding kit (login-gated, unverified) | same | none public | logos need a licence |
| storytel | https://press.storytel.com/logos (verified) — two PNGs ("Storytel logo", "Mofibo logo 1"), originals 403 off-site | unknown | unknown | https://press.storytel.com/page/6565ddd728cee/related-media/download/all?mediaType=image | editorial use only |
| bbc_sounds | https://www.bbc.co.uk/branding/logo-use (verified) — every use goes through a request form; "prior written consent" | not published | not published | none | written consent + licence required |
| pandora | https://developer.pandora.com/docs/developer-resources/brand-assets/ (verified) — Google Drive zip (EPS/PNG/JPG) + guidelines PDF (image-based, unreadable here) | unverified (zip not inspected) | unverified | https://drive.google.com/open?id=1N2_u5exhjLFeb2dCikVf2btC_fc2G365 | follow guidelines; permissions@pandora.com |

## Summary — what can actually be reused

Owner-published, fetchable, vector, and drawn for dark surfaces:
- **wikipedia**: `Wikipedia-logo-v2-bw_(White).svg` (CC BY-SA) — white mono globe; `Wikipedia's_W.svg` for the W.
- **internet_archive**: ia-icons `ia-logo.svg` glyph (colour-agnostic) and the white wide wordmark (Commons / openlibrary).
- **ibroadcast**: official dark "Powered by" SVG, but multi-grey and "no modification" — usable as icon_dark, not as a white monochrome.
- **fastmcp_server**: `favicon-dark.svg` (Apache-2.0 repo).
- **airplay / airplay_receiver**: Apple's white AirPlay glyph exists (PDF in a .dmg); our own white recolour matches its HIG rule.

Everything else is PNG-only, gated (Yandex, Microsoft, Yamaha, BBC), unpublished (Last.fm, NetEase, Fully Kiosk, ORF, HEOS, Storytel, gPodder, LRCLIB, MPD, Radio Paradise, nugs, TheAudioDB) or unverified (Deezer zip, Pandora zip, Niconico pack, MusicMe 403). Those need our own recolour/redraw.
