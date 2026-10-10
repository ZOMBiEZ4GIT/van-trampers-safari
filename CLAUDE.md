# Van Trampers — South Island Safari 2027

Interactive animated itinerary map + printable A4 "fridge map" PDF for Roland's
Aunty C's campervan trip around the NZ South Island (Van Trampers club, Upper
North Island chapter). She'll send the link/printouts to the group in **early
December 2026**.

## Source of truth

`source/VT_South_Island_Safari_2027_Summary_VT_VERSION.docx` — Aunty C's latest
summary (received 11 Oct 2026). It updates the post-reccie PDF of the same name
(text in `source/summary_VT_VERSION_extracted.txt`) in two ways: the overnight tramp
is dropped from Reefton, and Cass is confirmed as **1 night** (the PDF wrongly said 2).
**1 Feb – 13 Mar 2027, 15 hubs, 40 nights.** Both replace the Word doc Draft 5.07.26
(which had Arthur's Pass ×3 and Peel Forest; now Arthur's Pass / Hawdon Valley / Cass
and Hakatere, trip one day shorter). The 4-digit numbers are her **Site IDs**.

Date format decision (agreed with Aunty C's suggestion): show the **nights
occupied** as a range, e.g. Arr Feb 1 / Dep Feb 4 → "Feb 1–3 · 3 nights".
`safari_data.validate()` (run by build.py) checks every hub's range matches
arr/dep, weekdays are right, the chain is continuous and the total is 40.

Aunty C's Oct 2026 edit list (all done): phone-friendly/scrollable; no "Coming soon"
wording; no Day Walks icon (every hub has day walks — tramp + heritage icons stay);
no icons on the fridge-map label cards except 🚲 on Westport & Cass and 🥧 on
Reefton & Oxford; full "How We Roll" text with the closing line visible at the
bottom; a slower tour option (🐢 ½×, and 1× is slower than before).
Second round (11 Oct 2026, done): ⛺ removed from Reefton; the fridge map's
"Southern Alps" label (it ran the wrong way, through Otago) replaced with her line
"More great cycling and tramping down here…" in the empty south of the island.

## Deliverables (built, tested)

- `South_Island_Safari_Map.html` — single-file interactive site (same file as
  `docs/index.html`). Leaflet + Esri World Topo tiles (sepia CSS filter for the
  vintage look), OSM fallback, plus an inline vector NZ coastline underlay so
  the map is never blank. Numbered pins (Arthur's Pass hubs 7–9 share one
  combined pin/popup), dashed route with animated "marching ants", clickable
  itinerary sidebar, **▶ Play the Safari** animated van tour (van drives the
  route, pauses at each hub ∝ nights, opens popups, 1×/2×/4× speed,
  pause/replay/reset, ½×/1×/2×/4× speed, auto-plays ~3 s after load unless
  the user interacts first or prefers reduced motion; camera gently follows
  the van; zooms to 8 on start, refits at end), countdown-of-sleeps widget in
  the header, tramp/heritage + bike/pie icons, "How We Roll" notes. Hubs 7–9
  (Arthur's Pass, Hawdon Valley, Cass — all within 20 km) share a "7–9" pin
  below zoom 8, split to "7" + "8–9" at 8–10, and to three pins from zoom 10;
  tour and itinerary clicks open popups anchored to the hub itself so they
  work at any zoom. Mobile responsive (≤900 px the tour controls are a
  full-width strip *below* the map, route note a caption under that, and the
  itinerary scrolls with the page — no nested scroll box). Meta/OG tags for
  WhatsApp unfurls + inline favicon/apple-touch icons. Itinerary rows are
  real `<button>`s (keyboard + screen-reader friendly), focus-visible styles
  throughout. Vintage safari theme: parchment #f2e9d4, navy #1e3a5f,
  red #a93a2c, green #3e6b4f; fonts Oswald / Special Elite / Nunito Sans.
- `South_Island_Safari_Fridge_Map.pdf` — A4 landscape print companion, same
  theme: vector SVG map with label cards + summary table + legend + notes.
- `og-image.jpg` — 1200×630 link-preview image (`python3 gen_og.py && node og_shot.js`
  renders it from a vector map — no tiles/network needed; og:image URL in the
  template is absolute).
- `tshirt/` — merch mock-up for Aunty C's screen printer: `South_Island_Safari_Tshirt_Mockup.pdf`
  (navy and sand colourways, front logo + back "tour dates" graphic, print spec page),
  PNG previews, and print-ready `back_artwork_*.svg/.pdf` (300 × 400 mm, 2 spot colours).
  `python3 gen_tshirt.py && node tshirt_pdf.js`.
- `docs/` — the folder GitHub Pages serves (index.html, PDF, og-image.jpg,
  .nojekyll). Copy fresh builds in; don't edit in place.

## Build pipeline

- `python3 build.py` → assembles `South_Island_Safari_Map.html` (+ `test_local.html`)
  from `site_template.html` + `stops.js` + `logo_b64.txt` + `nz_polys_min.json`
  + `favicon_b64.txt` + `appletouch_b64.txt`. Placeholders in template:
  `__STOPS__`, `__LOGO__`, `__NZ__`, `__FAVICON__`, `__APPLETOUCH__`.
- `python3 gen_fridge.py` → writes `fridge.html`; then `node pdf.js` → prints it
  to `South_Island_Safari_Fridge_Map.pdf` via headless Chromium. Label-card
  positions are hand-placed (LAB dict, planned against the projected pin coords
  that `python3 safari_svg.py` prints, to avoid overlaps). Hubs 8–9 share one
  nudged pin on the whole-island map; cards carry the hub number. PDF embeds
  fonts via @fontsource woff2 (needs `npm install`); emoji need a colour emoji
  font on the machine (Noto Color Emoji works).
- On Roland's Windows machine: use `python` (no `python3`) and set `PYTHONUTF8=1`,
  or the generators die writing emoji in cp1252. Check a PDF rebuild actually
  embedded Oswald / Special Elite / Nunito Sans — if the fonts fail to load,
  Chromium silently falls back to Arial and Comic Sans.
- Itinerary data lives in `stops.js` **only**. `safari_data.py` parses it for the
  Python generators and validates the date chain; `safari_svg.py` is the shared
  vector-map drawing (projection, coastline, route, pins) used by the fridge
  map, og image and T-shirt. **If dates change, edit stops.js, then rebuild all.**
- `nz_polys_min.json` = simplified South Island coastline, extracted from npm
  `@geo-maps/countries-coastline-2km5` (see git-less provenance in extraction
  code comments; rounding to 3 dp, islets < 12 pts dropped).
- Tests: `npm install` first (leaflet + @fontsource fonts + playwright is
  preinstalled in Cowork; in Claude Code run `npx playwright install chromium`
  if needed). `node shot.js` (desktop+mobile screenshots), `node tour_test.js`
  / `tour_test2.js` (plays the animated tour end-to-end, checks ticker/errors),
  `node tour_test3.js` (mobile viewport: reset mid-tour, replay, countdown).
  All scripts launch Chromium through `pw_launch.js`, which falls back to a
  preinstalled browser (`CHROMIUM_PATH` or `/opt/pw-browsers/chromium`) when
  Playwright's own download is blocked. Screenshot and tour scripts set
  `window.__NO_AUTOPLAY` via addInitScript so they aren't racing the auto-play. Note: in the Cowork sandbox, CDN/tile requests are
  blocked, hence `test_local.html`; in normal environments the shipped file
  just works.

## Publishing status

**Live** since Aug 2026 at https://zombiez4git.github.io/van-trampers-safari/ —
GitHub Pages, public repo `ZOMBiEZ4GIT/van-trampers-safari`, deploy from
branch `main`, folder `/docs`. To ship changes: rebuild, copy outputs into
`docs/`, commit, push.

## Ideas / possible next steps (discussed or floated)

- Hub detail pages or expanded popups: per-hub walk lists from the shared
  drive Aunty C will circulate (DoC brochures, walk refs — the 4-digit numbers
  in popups/table are her walk reference IDs from that collection).
- GPX downloads per hub / route GPX for the GPS-app users (mentioned in her
  "What's Coming" list — she'll supply files later).
- ~~Auto-play on load, camera follow, countdown widget~~ — built Aug 2026.
- ~~T-shirt merch mock-up~~ — built Oct 2026 (`tshirt/`); printer may want the
  logo as a 1-colour version — ask Aunty C if she has a vector logo.
- Live weather per hub closer to the date.
- Printable per-hub one-pagers once her walk selections firm up.
- Photo memento version after the trip (swap blurbs for group photos).

## House style for this project

Australian English. Roland prefers approach/strategy first, then implementation;
skip basics, give context for technical detail. Warm, a bit playful — this is a
family holiday project, keep it fun (van emoji earns its keep).
