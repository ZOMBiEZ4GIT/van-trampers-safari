# Van Trampers — South Island Safari 2027 🚐

Interactive animated map of the Safari itinerary (1 Feb – 14 Mar 2027, 15 hubs, 41 nights),
plus the printable A4 fridge map.

**Live site:** https://zombiez4git.github.io/van-trampers-safari/

## What's on the site

- Real topo map with the route, numbered hub pins and tap-for-details popups
- **▶ Play the Safari** — an animated van drives the whole route (auto-plays on load),
  pausing at each hub, with the camera following along, 1×/2×/4× speed and replay
- Countdown of sleeps until departure
- Quick-reference itinerary panel, "How We Roll" notes, icon guide
- Footer link to download/print the A4 fridge map PDF

## Rebuilding

```sh
npm install                      # leaflet, fonts, playwright (dev)
npx playwright install chromium  # once, for tests/PDF/screenshots

python3 build.py                 # -> South_Island_Safari_Map.html + test_local.html
python3 gen_fridge.py && node pdf.js   # -> South_Island_Safari_Fridge_Map.pdf
node og_shot.js                  # -> og-image.jpg (link-preview image)

node shot.js                     # desktop + mobile screenshots
node tour_test.js                # plays the tour end-to-end, checks for errors
node tour_test3.js               # mobile viewport: reset mid-tour + replay
```

Itinerary data lives in `stops.js` (site) **and** at the top of `gen_fridge.py` (PDF) —
if dates change, update both and rebuild both, then copy the outputs into `docs/`
(which is what GitHub Pages serves).

Source of truth: Aunty C's Word summary table in `source/` (Draft 5.07.26).
