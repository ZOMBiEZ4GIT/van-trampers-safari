# Van Trampers — South Island Safari 2027 🚐

Interactive animated map of the Safari itinerary (1 Feb – 13 Mar 2027, 15 hubs, 40 nights),
the printable A4 fridge map, and the tour-tee merch artwork.

**Live site:** https://zombiez4git.github.io/van-trampers-safari/

## What's on the site

- Real topo map with the route, numbered hub pins and tap-for-details popups
  (hubs 7–9 around Arthur's Pass share a pin until you zoom in)
- **▶ Play the Safari** — an animated van drives the whole route (auto-plays on load),
  pausing at each hub, with the camera following along, 🐢 ½× / 1× / 2× / 4× speed and replay
- Countdown of sleeps until departure
- Full itinerary panel (scrolls with the page on phones), "How We Roll" notes, icon guide
- Footer link to download/print the A4 fridge map PDF

## Rebuilding

```sh
npm install                      # leaflet, fonts, playwright (dev)
npx playwright install chromium  # once, for tests/PDF/screenshots (or set CHROMIUM_PATH to an existing browser)

python3 build.py                 # -> South_Island_Safari_Map.html + test_local.html (validates stops.js first)
python3 gen_fridge.py && node pdf.js      # -> South_Island_Safari_Fridge_Map.pdf
python3 gen_og.py && node og_shot.js      # -> og-image.jpg (link-preview image)
python3 gen_tshirt.py && node tshirt_pdf.js   # -> tshirt/ mock-up PDF, PNG previews, print-ready back artwork

node shot.js                     # desktop + mobile screenshots
node tour_test.js                # plays the tour end-to-end, checks for errors
node tour_test3.js               # mobile viewport: reset mid-tour + replay
```

Itinerary data lives in `stops.js` — the Python generators read it via `safari_data.py`, so edit
it once, then rebuild everything and copy the outputs into `docs/` (which is what GitHub Pages serves).

Source of truth: Aunty C's post-reccie summary, `source/VT_South_Island_Safari_2027_Summary_VT_VERSION.pdf`.
