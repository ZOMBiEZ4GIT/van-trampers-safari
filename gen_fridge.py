#!/usr/bin/env python3
"""Generate the A4 landscape fridge-map HTML (vector SVG map + summary table).
Then `node pdf.js` prints it to South_Island_Safari_Fridge_Map.pdf.
Data comes from stops.js via safari_data.py; the map drawing from safari_svg.py."""
import os, pathlib
from safari_data import STOPS, TRIP, HERE, validate
from safari_svg import Proj, coast_polygons, route_points, pins_svg, pin_positions

validate()

W, H = 640, 742
P = Proj(W, H)

ICON = {'tramp': '⛺', 'heritage': '🏛️'}
FUN = {'bike': '🚲', 'pie': '🥧'}
def icons(s):
    return ' '.join([ICON[a] for a in s['acts']] + [FUN[f] for f in s.get('fun', [])])
def fun_icons(s):
    return ' '.join(FUN[f] for f in s.get('fun', []))

# ---------- label cards ----------
# absolute card top-left positions, planned against the projected pin coords (python3 safari_svg.py
# prints them) so cards, pins and leader lines don't overlap. 'l' = leader meets the card's left
# edge (card sits right of its pin), 'r' = leader meets the right edge (card sits left of its pin).
CARD_W, CARD_H = 124, 30
LAB = {
 1:(458,168,'l'), 2:(460,104,'l'), 3:(282,120,'r'), 4:(264,158,'r'), 5:(251,203,'r'),
 6:(247,248,'r'), 7:(445,234,'l'), 8:(478,268,'l'), 9:(470,340,'l'), 10:(492,306,'l'),
 11:(277,300,'r'), 12:(452,374,'l'), 13:(256,372,'r'), 14:(248,334,'r'), 15:(420,410,'l'),
}
pin_xy = {}
for label, ns, x, y, sf in pin_positions(P):
    for n in ns: pin_xy[n] = (x, y)

cards, leaders = [], []
for s in STOPS:
    x, y = pin_xy[s['n']]
    lx, ly, anch = LAB[s['n']]
    nm = f"{s['n']} · {s['name']}" + (f" ({s['tag'].title()})" if s.get('tag') else '')
    nights = f"{s['nights']} night" + ('s' if s['nights'] > 1 else '')
    dt = f"{s['dates']} · {nights}"
    ex = lx if anch == 'l' else lx + CARD_W
    leaders.append(f'<line x1="{x}" y1="{y}" x2="{ex}" y2="{ly+CARD_H/2}" class="leader"/>')
    fun = fun_icons(s)
    cards.append(
      f'<g><rect x="{lx}" y="{ly}" width="{CARD_W}" height="{CARD_H}" rx="5" class="card"/>'
      f'<text x="{lx+7}" y="{ly+12}" class="cardname">{nm}</text>'
      f'<text x="{lx+7}" y="{ly+24}" class="carddt">{dt}</text>'
      + (f'<text x="{lx+CARD_W-6}" y="{ly+24}" text-anchor="end" class="cardic">{fun}</text>' if fun else '')
      + '</g>')

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="{W}" height="{H}" fill="#cfe0dc"/>
  {coast_polygons(P)}
  <text x="60" y="95" class="sea">TASMAN&#160;&#160;SEA</text>
  <text x="455" y="520" class="sea">PACIFIC OCEAN</text>
  <g transform="rotate(-6 225 556)">
    <text x="225" y="548" text-anchor="middle" class="south">More great cycling</text>
    <text x="225" y="568" text-anchor="middle" class="south">and tramping down here…</text>
  </g>
  <polyline points="{route_points(P)}" class="route-case"/>
  <polyline points="{route_points(P)}" class="route"/>
  {''.join(leaders)}{''.join(cards)}
  {pins_svg(P)}
  <g transform="translate(36,{H-64})">
    <circle r="24" class="comp"/><text y="-8" text-anchor="middle" class="compN">N</text>
    <path d="M 0 -4 L 5 12 L 0 8 L -5 12 Z" fill="#a93a2c"/>
  </g>
</svg>'''

logo = open(os.path.join(HERE, 'logo_b64.txt')).read().strip()

rows = []
for s in STOPS:
    tag = f' <span class="ttag">({s["tag"].title()})</span>' if s.get('tag') else ''
    rows.append(f'<tr><td class="c1">{s["n"]}</td><td class="c2">{s["name"]}{tag}</td>'
                f'<td class="c3">{s["dates"]}</td><td class="c4">{s["nights"]}</td>'
                f'<td class="c5">{icons(s)}</td></tr>')

FD = pathlib.Path(HERE, 'node_modules', '@fontsource').as_uri()  # file:/// URL on Windows too
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'Oswald'; font-weight:600; src:url('{FD}/oswald/files/oswald-latin-600-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Oswald'; font-weight:700; src:url('{FD}/oswald/files/oswald-latin-700-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Special Elite'; font-weight:400; src:url('{FD}/special-elite/files/special-elite-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:400; src:url('{FD}/nunito-sans/files/nunito-sans-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:700; src:url('{FD}/nunito-sans/files/nunito-sans-latin-700-normal.woff2') format('woff2'); }}
@page {{ size: A4 landscape; margin: 0; }}
:root {{ --parch:#f2e9d4; --ink:#3d3020; --navy:#1e3a5f; --red:#a93a2c; --green:#3e6b4f; --ochre:#b07c2a; --cream:#faf5e8; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:297mm; height:210mm; font-family:'Nunito Sans','Segoe UI',sans-serif; color:var(--ink);
  background:var(--parch);
  background-image:radial-gradient(ellipse at 25% 15%, rgba(255,252,240,.6), transparent 55%),
    radial-gradient(ellipse at 85% 90%, rgba(160,120,60,.15), transparent 50%);
  overflow:hidden; }}
.sheet {{ width:100%; height:100%; padding:5mm; display:flex; gap:4mm; }}
.left {{ flex:0 0 172mm; border:1.2mm solid var(--navy); border-radius:3mm; overflow:hidden; background:#cfe0dc; position:relative; }}
.left svg {{ width:100%; height:100%; display:block; }}
.right {{ flex:1; min-width:0; height:100%; display:flex; flex-direction:column; gap:3mm; }}
.land {{ fill:#ece1c2; stroke:#8a7452; stroke-width:1; }}
.sea {{ font-family:'Nunito Sans',sans-serif; font-style:italic; letter-spacing:4px; font-size:13px; fill:#7d9a94; }}
.south {{ font-family:'Special Elite',cursive; font-size:14px; fill:#8a7452; }}
.route-case {{ fill:none; stroke:#fdf6e6; stroke-width:5.5; stroke-linejoin:round; }}
.route {{ fill:none; stroke:var(--red); stroke-width:2.6; stroke-dasharray:6 5; stroke-linejoin:round; }}
.leader {{ stroke:#8a7452; stroke-width:1; stroke-dasharray:2 2; }}
.card {{ fill:var(--cream); stroke:var(--ochre); stroke-width:1.1; }}
.cardname {{ font-family:'Oswald',sans-serif; font-weight:600; font-size:9.5px; fill:var(--navy); }}
.carddt {{ font-family:'Special Elite',cursive; font-size:8px; fill:var(--red); }}
.cardic {{ font-size:8px; }}
.pin-r {{ fill:var(--red); stroke:#fdf6e6; stroke-width:2; }}
.pin-g {{ fill:var(--green); stroke:#fdf6e6; stroke-width:2; }}
.pintxt {{ font-family:'Oswald',sans-serif; font-weight:600; font-size:11px; fill:#fff; }}
.comp {{ fill:rgba(250,245,232,.92); stroke:var(--navy); stroke-width:1.6; }}
.compN {{ font-family:'Oswald',sans-serif; font-weight:700; font-size:11px; fill:var(--navy); }}
.masthead {{ flex:0 0 auto; text-align:center; padding:2mm 3mm 2.5mm 22mm; background:var(--cream); border:1.2mm solid var(--navy); border-radius:3mm; position:relative; }}
.masthead img {{ position:absolute; left:2.5mm; top:50%; transform:translateY(-50%); width:17mm; }}
.kick {{ font-family:'Special Elite',cursive; font-size:8.5pt; letter-spacing:2px; color:var(--green); text-transform:uppercase; }}
h1 {{ font-family:'Oswald',sans-serif; font-size:21pt; line-height:1; color:var(--navy); text-transform:uppercase; letter-spacing:1px; }}
h1 .saf {{ color:var(--red); }}
.ribbon {{ display:inline-block; margin-top:1.5mm; background:var(--red); color:#fdf6e6; font-family:'Oswald',sans-serif;
  font-size:8pt; letter-spacing:1px; padding:1mm 5mm; text-transform:uppercase; white-space:nowrap;
  clip-path:polygon(8px 0, calc(100% - 8px) 0, 100% 50%, calc(100% - 8px) 100%, 8px 100%, 0 50%); }}
.tablebox {{ background:var(--cream); border:1.2mm solid var(--navy); border-radius:3mm; padding:2mm 3mm; flex:1 1 auto; min-height:0; overflow:hidden; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ font-family:'Oswald',sans-serif; text-transform:uppercase; letter-spacing:1px; font-size:7.5pt; color:var(--cream);
  background:var(--navy); padding:1.2mm 1.5mm; text-align:left; }}
td {{ font-size:8.6pt; padding:1.25mm 1.5mm; border-bottom:0.3mm dashed #cbb98e; }}
tr:last-child td {{ border-bottom:none; }}
.c1 {{ font-family:'Oswald',sans-serif; font-weight:600; color:var(--red); width:6mm; }}
.c2 {{ font-weight:700; color:var(--navy); }}
.ttag {{ font-family:'Special Elite',cursive; font-size:7pt; color:var(--red); font-weight:400; }}
.c3 {{ font-family:'Special Elite',cursive; font-size:7.8pt; color:#6b4a2c; white-space:nowrap; }}
.c4 {{ text-align:center; width:9mm; font-family:'Oswald',sans-serif; }}
.c5 {{ font-size:7.5pt; white-space:nowrap; }}
.foot {{ flex:0 0 auto; background:var(--cream); border:1.2mm solid var(--navy); border-radius:3mm; padding:2mm 3mm; }}
.foot h3 {{ font-family:'Oswald',sans-serif; color:var(--red); text-transform:uppercase; letter-spacing:1.5px; font-size:9pt;
  border-bottom:0.5mm solid var(--ochre); display:inline-block; margin-bottom:1mm; }}
.foot p {{ font-size:7.6pt; line-height:1.5; }}
.legend {{ display:flex; gap:3.5mm; margin-top:1.5mm; font-size:7.4pt; align-items:center; flex-wrap:wrap; }}
.stamp {{ text-align:center; font-family:'Special Elite',cursive; font-size:8pt; color:var(--green); margin-top:1mm; }}
.dw {{ font-family:'Special Elite',cursive; font-size:7.4pt; color:var(--green); margin-top:1mm; }}
</style></head><body>
<div class="sheet">
  <div class="left">{svg}</div>
  <div class="right">
    <div class="masthead">
      <img src="data:image/png;base64,{logo}">
      <div class="kick">The Van Trampers Present</div>
      <h1>South Island <span class="saf">Safari</span></h1>
      <div class="ribbon">{TRIP['ribbon']}</div>
    </div>
    <div class="tablebox">
      <table>
        <tr><th>#</th><th>Hub</th><th>Dates (nights there)</th><th>Nts</th><th>Options</th></tr>
        {''.join(rows)}
      </table>
      <div class="legend"><span>⛺ Overnight tramp</span><span>🏛️ Heritage &amp; history</span><span>🚲 Bring the bikes</span><span>🥧 Famous pie</span></div>
      <div class="dw">Day walks are on the menu at every hub — pick what suits you on the day.</div>
    </div>
    <div class="foot">
      <h3>How We Roll</h3>
      <p>Everything is optional — your safari, your choice. Each evening at Happy Hour we plan the next day's
      options and split into groups. Weather calls the shots, WhatsApp keeps us together, and the taxi-van is
      $4 a leg (TBC). Route is approximate — stops &amp; order may change.</p>
      <div class="stamp">Above all: good company · shared adventure · freedom to roam — it's your trip! 🚐</div>
    </div>
  </div>
</div>
</body></html>'''

open(os.path.join(HERE, 'fridge.html'), 'w').write(html)
print('written fridge.html', len(html))
