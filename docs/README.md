# Published site folder

This folder is served by GitHub Pages (Settings → Pages → main branch, `/docs`).

- `index.html` — the interactive Safari map (single file, built by `../build.py`)
- `South_Island_Safari_Fridge_Map.pdf` — printable A4 fridge map (built by `../gen_fridge.py` + `../pdf.js`)
- `og-image.jpg` — 1200×630 link-preview image for WhatsApp/social unfurls (built by `../og_shot.js`)
- `.nojekyll` — tells Pages to serve files as-is

Don't edit `index.html` here directly — change the source in the repo root and rebuild,
then copy the outputs in. See the root README.
