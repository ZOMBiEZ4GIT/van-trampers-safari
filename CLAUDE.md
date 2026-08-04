# Van Trampers — South Island Safari 2027

Interactive animated itinerary map + printable A4 "fridge map" PDF for Roland's
Aunty C's campervan trip around the NZ South Island (Van Trampers club, Upper
North Island chapter). She'll send the link/printouts to the group in **early
December 2026**.

## Source of truth

`source/South_Island_Safari_1_Feb__14_Mar_Summary_Draft_5.07.26.docx` — Aunty C's
Word summary table. **1 Feb – 14 Mar 2027, 15 hubs, 41 nights.**

⚠️ Her earlier AI-generated draft maps (`source/*.png`) show *different* dates
(2 Feb – 31 Mar, different hub list). The Word doc was used everywhere. Roland
was going to confirm with Aunty C that the Word doc is current — check before
final publish.

Date format decision (agreed with Aunty C's suggestion): show the **nights
occupied** as a range, e.g. Arr Feb 1 / Dep Feb 4 → "Feb 1–3 · 3 nights".
Verified programmatically: every hub's range matches arr/dep, chain is
continuous (each dep = next arr), totals 41 nights = Feb 1 → Mar 14.

## Deliverables (built, tested)

- `South_Island_Safari_Map.html` — single-file interactive site (same file as
  `docs/index.html`). Leaflet + Esri World Topo tiles (sepia CSS filter for the
  vintage look), OSM fallback, plus an inline vector NZ coastline underlay so
  the map is never blank. Numbered pins (Arthur's Pass hubs 7–9 share one
  combined pin/popup), dashed route with animated "marching ants", clickable
  itinerary sidebar, **▶ Play the Safari** animated van tour (van drives the
  route, pauses at each hub ∝ nights, opens popups, 1×/2×/4× speed,
  pause/replay/reset, auto-plays ~3 s after load unless the user interacts
  first or prefers reduced motion; camera gently follows the van; zooms to 8
  on start, refits at end), countdown-of-sleeps widget in the header,
  day-walk/tramp/heritage icons, "How We Roll" notes. Mobile responsive
  (≤900 px the tour controls are a full-width strip *below* the map, route
  note a caption under that — nothing overlays the pins). Meta/OG tags for
  WhatsApp unfurls + inline favicon/apple-touch icons. Itinerary rows are
  real `<button>`s (keyboard + screen-reader friendly), focus-visible styles
  throughout. Vintage safari theme: parchment #f2e9d4, navy #1e3a5f,
  red #a93a2c, green #3e6b4f; fonts Oswald / Special Elite / Nunito Sans.
- `South_Island_Safari_Fridge_Map.pdf` — A4 landscape print companion, same
  theme: vector SVG map with label cards + summary table + legend + notes.
- `og-image.jpg` — 1200×630 link-preview image (`node og_shot.js` regenerates
  it from a headless screenshot; og:image URL in the template is absolute).
- `docs/` — the folder GitHub Pages serves (index.html, PDF, og-image.jpg,
  .nojekyll). Copy fresh builds in; don't edit in place.

## Build pipeline

- `python3 build.py` → assembles `South_Island_Safari_Map.html` (+ `test_local.html`)
  from `site_template.html` + `stops.js` + `logo_b64.txt` + `nz_polys_min.json`
  + `favicon_b64.txt` + `appletouch_b64.txt`. Placeholders in template:
  `__STOPS__`, `__LOGO__`, `__NZ__`, `__FAVICON__`, `__APPLETOUCH__`.
- `python3 gen_fridge.py` → writes `fridge.html`; then `node pdf.js` → prints it
  to `South_Island_Safari_Fridge_Map.pdf` via headless Chromium. The fridge
  generator has its own copy of the stops/route data and hand-placed label-card
  positions (LAB dict, planned against projected pin coords to avoid overlaps).
  PDF embeds fonts via @fontsource woff2 (needs `npm install`).
- Itinerary data lives in `stops.js` (site) and duplicated at the top of
  `gen_fridge.py` (PDF). **If dates change, update both**, then rebuild both.
- `nz_polys_min.json` = simplified South Island coastline, extracted from npm
  `@geo-maps/countries-coastline-2km5` (see git-less provenance in extraction
  code comments; rounding to 3 dp, islets < 12 pts dropped).
- Tests: `npm install` first (leaflet + @fontsource fonts + playwright is
  preinstalled in Cowork; in Claude Code run `npx playwright install chromium`
  if needed). `node shot.js` (desktop+mobile screenshots), `node tour_test.js`
  / `tour_test2.js` (plays the animated tour end-to-end, checks ticker/errors),
  `node tour_test3.js` (mobile viewport: reset mid-tour, replay, countdown).
  Screenshot scripts set `window.__NO_AUTOPLAY` via addInitScript so stills
  aren't taken mid-tour. Note: in the Cowork sandbox, CDN/tile requests are
  blocked, hence `test_local.html`; in normal environments the shipped file
  just works.

## Publishing status

**Live** since Aug 2026 at https://zombiez4git.github.io/van-trampers-safari/ —
GitHub Pages, public repo `ZOMBiEZ4GIT/van-trampers-safari`, deploy from
branch `main`, folder `/docs`. To ship changes: rebuild, copy outputs into
`docs/`, commit, push. ⚠️ Still confirm with Aunty C that the Word doc dates
are current before she sends the link to the group.

## Ideas / possible next steps (discussed or floated)

- Hub detail pages or expanded popups: per-hub walk lists from the shared
  drive Aunty C will circulate (DoC brochures, walk refs — the 4-digit numbers
  in popups/table are her walk reference IDs from that collection).
- GPX downloads per hub / route GPX for the GPS-app users (mentioned in her
  "What's Coming" list — she'll supply files later).
- ~~Auto-play on load, camera follow, countdown widget~~ — built Aug 2026.
- Live weather per hub closer to the date.
- Printable per-hub one-pagers once her walk selections firm up.
- Photo memento version after the trip (swap blurbs for group photos).

## House style for this project

Australian English. Roland prefers approach/strategy first, then implementation;
skip basics, give context for technical detail. Warm, a bit playful — this is a
family holiday project, keep it fun (van emoji earns its keep).
