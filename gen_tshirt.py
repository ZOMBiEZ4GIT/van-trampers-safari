#!/usr/bin/env python3
"""T-shirt merch artwork + mock-up for the screen printer.

Writes into tshirt/:
  back_artwork_navy_tee.svg / back_artwork_sand_tee.svg  — print-ready back graphic (300 × 400 mm, 2 spot colours)
  back_artwork_*.html, mockup.html                        — intermediates; `node tshirt_pdf.js` turns them into
  South_Island_Safari_Tshirt_Mockup.pdf (+ PNG previews) and back_artwork_*.pdf
"""
import os, re, pathlib
from safari_data import STOPS, TRIP, HERE, validate
from safari_svg import Proj, coast_polygons, route_points, pins_svg

validate()
OUT = os.path.join(HERE, 'tshirt'); os.makedirs(OUT, exist_ok=True)
FD = pathlib.Path(HERE, 'node_modules', '@fontsource').as_uri()  # file:/// URL on Windows too
LOGO = open(os.path.join(HERE, 'logo_b64.txt')).read().strip()

# Brand palette (hex — the printer matches to their nearest Pantone / plastisol stock)
NAVY, RED, CREAM, SAND = '#1e3a5f', '#a93a2c', '#f2e9d4', '#d9cdb0'

COLOURWAYS = {
  'navy_tee': dict(title='Navy tee', shirt=NAVY, ink=CREAM, red='#c9533f', ink_name='Cream', red_name='Safari red (lighter)'),
  'sand_tee': dict(title='Sand / natural tee', shirt=SAND, ink=NAVY, red=RED, ink_name='Navy', red_name='Safari red'),
}

FONT_CSS = f'''
@font-face {{ font-family:'Oswald'; font-weight:600; src:url('{FD}/oswald/files/oswald-latin-600-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Oswald'; font-weight:700; src:url('{FD}/oswald/files/oswald-latin-700-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Special Elite'; src:url('{FD}/special-elite/files/special-elite-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:400; src:url('{FD}/nunito-sans/files/nunito-sans-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:700; src:url('{FD}/nunito-sans/files/nunito-sans-latin-700-normal.woff2') format('woff2'); }}
'''

# ---------- the back graphic: 300 x 400 mm, 1 user unit = 1 mm ----------
def back_svg(cw, bg=None, uid='a'):
    ink, red, shirt = cw['ink'], cw['red'], cw['shirt']
    MW, MH = 172, 176
    P = Proj(MW, MH)
    mx = (300 - MW) / 2
    pins = pins_svg(P, pin_w=6.2, pin_h=6.2, font=3.6, cls_r=f'pr{uid}', cls_g=f'pr{uid}', cls_t=f'pt{uid}')
    # tour-dates list, rock-poster style: two columns
    rows = []
    left, right = STOPS[:8], STOPS[8:]
    for col, xs, xe in ((left, 22, 142), (right, 158, 278)):
        for i, s in enumerate(col):
            y = 306 + i * 10
            rows.append(f'<text x="{xs}" y="{y}" class="num{uid}">{s["n"]:02d}</text>'
                        f'<text x="{xs+12}" y="{y}" class="hub{uid}">{s["name"].upper()}</text>'
                        f'<text x="{xe}" y="{y}" text-anchor="end" class="dt{uid}">{s["dates"].upper()}</text>')
    bgrect = f'<rect width="300" height="400" fill="{bg}"/>' if bg else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400" width="300mm" height="400mm">
<style>
  .kick{uid}{{font-family:'Special Elite';font-size:6.2px;letter-spacing:1.2px;fill:{ink}}}
  .t1{uid}{{font-family:'Oswald';font-weight:700;font-size:31px;letter-spacing:1px;fill:{ink}}}
  .t2{uid}{{font-family:'Oswald';font-weight:700;font-size:46px;letter-spacing:3px;fill:{red}}}
  .rib{uid}{{fill:{red}}} .ribt{uid}{{font-family:'Oswald';font-weight:600;font-size:7.2px;letter-spacing:1.6px;fill:{shirt}}}
  .land{uid}{{fill:none;stroke:{ink};stroke-width:.55;stroke-linejoin:round}}
  .route-case{uid}{{fill:none;stroke:{shirt};stroke-width:2.6;stroke-linejoin:round}}
  .route{uid}{{fill:none;stroke:{red};stroke-width:1.3;stroke-dasharray:2.4 1.8;stroke-linejoin:round}}
  .pr{uid}{{fill:{red};stroke:{shirt};stroke-width:.7}} .pt{uid}{{font-family:'Oswald';font-weight:600;font-size:3.6px;fill:{shirt}}}
  .sea{uid}{{font-family:'Nunito Sans';font-style:italic;font-size:4.2px;letter-spacing:1.4px;fill:{ink};opacity:.75}}
  .num{uid}{{font-family:'Oswald';font-weight:700;font-size:6.4px;fill:{red}}}
  .hub{uid}{{font-family:'Oswald';font-weight:600;font-size:6.4px;letter-spacing:.4px;fill:{ink}}}
  .dt{uid}{{font-family:'Special Elite';font-size:5px;fill:{red}}}
  .foot{uid}{{font-family:'Special Elite';font-size:5.6px;letter-spacing:1.2px;fill:{ink}}}
  .rule{uid}{{stroke:{ink};stroke-width:.4;stroke-dasharray:1.5 1.5}}
</style>
{bgrect}
<text x="150" y="14" text-anchor="middle" class="kick{uid}">THE VAN TRAMPERS PRESENT</text>
<text x="150" y="45" text-anchor="middle" class="t1{uid}">SOUTH ISLAND</text>
<text x="150" y="89" text-anchor="middle" class="t2{uid}">SAFARI</text>
<polygon points="48,96 252,96 258,103 252,110 48,110 42,103" class="rib{uid}"/>
<text x="150" y="105.6" text-anchor="middle" class="ribt{uid}">{TRIP['ribbon'].upper().replace('–','–')}</text>
<g transform="translate({mx},115)">
  <text x="8" y="22" class="sea{uid}">TASMAN SEA</text>
  <text x="118" y="132" class="sea{uid}">PACIFIC OCEAN</text>
  {coast_polygons(P, cls=f'land{uid}', south_only=True)}
  <polyline points="{route_points(P)}" class="route-case{uid}"/>
  <polyline points="{route_points(P)}" class="route{uid}"/>
  {pins}
</g>
<line x1="22" y1="296" x2="278" y2="296" class="rule{uid}"/>
{''.join(rows)}
<line x1="22" y1="382" x2="278" y2="382" class="rule{uid}"/>
<text x="150" y="394" text-anchor="middle" class="foot{uid}">GOOD COMPANY · SHARED ADVENTURE · FREEDOM TO ROAM</text>
</svg>'''

# ---------- a T-shirt silhouette for the mock-up (400 x 440 box; body 172 units ≈ 560 mm wide) ----------
TEE_PATH = 'M150,40 Q200,30 250,40 L340,80 L372,172 L286,200 L286,418 Q200,428 114,418 L114,200 L28,172 L60,80 Z'
def tee_svg(cw, side, uid):
    shirt, ink = cw['shirt'], cw['ink']
    dark = shirt == NAVY
    seam = 'rgba(255,255,255,.35)' if dark else 'rgba(0,0,0,.25)'
    shade = 'rgba(0,0,0,.18)' if dark else 'rgba(0,0,0,.08)'
    neck = (f'<path d="M150,40 Q200,92 250,40" fill="{shirt}" stroke="{seam}" stroke-width="2"/>'
            f'<path d="M150,40 Q200,80 250,40" fill="none" stroke="{seam}" stroke-width="1.2"/>') if side == 'front' else \
           f'<path d="M150,40 Q200,62 250,40" fill="{shirt}" stroke="{seam}" stroke-width="2"/>'
    # print: 300 x 400 mm back graphic = 92 x 123 units; 90 mm wide front logo = 27.6 units (wearer's left chest)
    if side == 'back':
        art = f'<svg x="154" y="74" width="92" height="123" viewBox="0 0 300 400">{back_svg(cw, uid=uid)[back_svg(cw, uid=uid).index("<style>"):-6]}</svg>'
    else:
        art = f'<image x="214" y="80" width="27.6" height="28.9" href="data:image/png;base64,{LOGO}"/>'
    return f'''<svg viewBox="0 0 400 440" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <path d="{TEE_PATH}" fill="{shirt}" stroke="{seam}" stroke-width="2" stroke-linejoin="round"/>
  <path d="M114,200 L60,80" stroke="{seam}" stroke-width="1"/><path d="M286,200 L340,80" stroke="{seam}" stroke-width="1"/>
  <path d="M114,200 L114,418" stroke="{shade}" stroke-width="6" opacity=".5"/><path d="M286,200 L286,418" stroke="{shade}" stroke-width="6" opacity=".5"/>
  {neck}
  {art}
</svg>'''

def page(title, body, note=''):
    return f'''<section class="page"><div class="hd"><div><div class="kick">Van Trampers · South Island Safari 2027 · merch mock-up</div><h2>{title}</h2></div><div class="note">{note}</div></div>{body}</section>'''

pages = []
for key, cw in COLOURWAYS.items():
    body = f'''<div class="two">
      <figure><div class="tee">{tee_svg(cw, 'front', key+'f')}</div><figcaption>FRONT — Van Trampers logo, 90 mm wide, left chest (wearer's left)</figcaption></figure>
      <figure><div class="tee">{tee_svg(cw, 'back', key+'b')}</div><figcaption>BACK — Safari route &amp; tour dates, 300 × 400 mm, centred, top ~60 mm below collar</figcaption></figure>
    </div>'''
    pages.append(page(f'Colourway: {cw["title"]}', body,
                      f'Inks: <b>{cw["ink_name"]}</b> + <b>{cw["red_name"]}</b> on a {cw["title"].lower()} · logo full colour (or 1-colour {cw["ink_name"].lower()})'))

specs = f'''<div class="two spec">
  <figure><div class="art">{back_svg(COLOURWAYS['sand_tee'], bg=SAND, uid='s')}</div><figcaption>Back graphic at 50 % — 300 mm wide × 400 mm tall (fits a standard A3 screen / 35 × 45 cm platen)</figcaption></figure>
  <div class="txt">
    <h3>Print spec (for the screen printer)</h3>
    <ul>
      <li><b>Back:</b> 300 × 400 mm, centred, top edge ~60 mm below the back collar. Two spot colours.</li>
      <li><b>Front:</b> Van Trampers logo, 90 mm wide, left chest (wearer's left), ~75 mm below the shoulder seam. Full-colour logo as supplied, or a 1-colour version in the main ink if we keep it to a simple print.</li>
      <li><b>Colours (hex, match to nearest Pantone/stock):</b> navy {NAVY} · safari red {RED} · cream {CREAM}. Navy tee uses cream + red; sand tee uses navy + red. Pin numbers and ribbon text knock out to the shirt colour.</li>
      <li><b>Files:</b> <code>back_artwork_navy_tee.svg / .pdf</code> and <code>back_artwork_sand_tee.svg / .pdf</code> (vector, 1 unit = 1 mm, fonts embedded — ask the printer to outline text if their RIP needs it). Logo: <code>source/Van_Trampers_Logo_FINAL.jpg</code>.</li>
      <li><b>Fonts:</b> Oswald (titles, hub names), Special Elite (typewriter dates), Nunito Sans (sea labels) — all Google Fonts, OFL-licensed.</li>
      <li><b>Garment:</b> suggest a heavyweight cotton tee — navy, or sand/natural for the lighter look that matches the fridge map.</li>
    </ul>
    <h3>Tour dates (back)</h3>
    <div class="dates">{''.join(f'<span><b>{s["n"]:02d}</b> {s["name"].upper()} <i>{s["dates"].upper()}</i></span>' for s in STOPS)}</div>
  </div>
</div>'''
pages.append(page('Back artwork &amp; print spec', specs, f'{TRIP["ribbon"]}'))

mock = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FONT_CSS}
@page {{ size: A4 landscape; margin: 0; }}
:root {{ --parch:#f2e9d4; --ink:#3d3020; --navy:#1e3a5f; --red:#a93a2c; --green:#3e6b4f; --ochre:#b07c2a; --cream:#faf5e8; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Nunito Sans',sans-serif; color:var(--ink); background:#fff; }}
.page {{ width:297mm; height:210mm; padding:8mm 10mm; background:var(--parch); page-break-after:always; display:flex; flex-direction:column; gap:4mm; overflow:hidden;
  background-image:radial-gradient(ellipse at 25% 15%, rgba(255,252,240,.6), transparent 55%); }}
.hd {{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px double var(--navy); padding-bottom:2mm; }}
.kick {{ font-family:'Special Elite'; font-size:8pt; letter-spacing:2px; color:var(--green); text-transform:uppercase; }}
h2 {{ font-family:'Oswald'; font-weight:700; font-size:18pt; color:var(--navy); text-transform:uppercase; letter-spacing:1px; }}
.note {{ font-family:'Special Elite'; font-size:9pt; color:var(--red); text-align:right; max-width:120mm; }}
.two {{ flex:1; display:grid; grid-template-columns:1fr 1fr; gap:8mm; min-height:0; }}
figure {{ display:flex; flex-direction:column; min-height:0; }}
.tee, .art {{ flex:1; min-height:0; display:flex; align-items:center; justify-content:center; }}
.tee svg {{ max-height:150mm; }}
.art svg {{ width:150mm; height:200mm; border:1px dashed var(--navy); box-shadow:0 2px 8px rgba(0,0,0,.2); }}
.spec .art {{ align-items:flex-start; }} .spec .art svg {{ width:120mm; height:160mm; }}
figcaption {{ font-family:'Special Elite'; font-size:8.5pt; color:var(--green); text-align:center; margin-top:2mm; }}
.txt h3 {{ font-family:'Oswald'; color:var(--red); text-transform:uppercase; letter-spacing:1.5px; font-size:11pt; border-bottom:0.5mm solid var(--ochre); display:inline-block; margin:1mm 0 2mm; }}
.txt ul {{ list-style:none; }} .txt li {{ font-size:8.6pt; line-height:1.4; padding:1mm 0 1mm 5mm; position:relative; }}
.txt li::before {{ content:"✦"; position:absolute; left:0; color:var(--ochre); }}
code {{ font-family:'Special Elite'; font-size:8pt; color:var(--navy); }}
.dates {{ display:grid; grid-template-columns:1fr 1fr; gap:.5mm 4mm; font-size:8pt; font-family:'Oswald'; color:var(--navy); }}
.dates b {{ color:var(--red); }} .dates i {{ font-family:'Special Elite'; font-style:normal; color:var(--red); font-size:7.5pt; }}
</style></head><body>{''.join(pages)}</body></html>'''
open(os.path.join(OUT, 'mockup.html'), 'w').write(mock)

for key, cw in COLOURWAYS.items():
    svg = back_svg(cw, uid='p')
    open(os.path.join(OUT, f'back_artwork_{key}.svg'), 'w').write(svg)
    # print-ready page at exact size, on the shirt colour so the knockouts preview correctly
    open(os.path.join(OUT, f'back_artwork_{key}.html'), 'w').write(
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FONT_CSS}@page{{size:300mm 400mm;margin:0}}'
        f'body{{margin:0;width:300mm;height:400mm;background:{cw["shirt"]}}} svg{{display:block}}</style></head><body>{svg}</body></html>')
print('written tshirt/mockup.html + back_artwork_*.svg/.html')
