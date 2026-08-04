#!/usr/bin/env python3
"""Generate the A4 landscape fridge-map HTML (vector SVG map + summary table)."""
import json, math, base64

# ---------- data ----------
STOPS = [
 dict(n=1,  name="Reefton", tag="START", lat=-42.117, lng=171.867, nights=3, dates="Feb 1–3",  acts="DTH"),
 dict(n=2,  name="Denniston", lat=-41.738, lng=171.800, nights=2, dates="Feb 4–5", acts="DH"),
 dict(n=3,  name="Westport", lat=-41.754, lng=171.601, nights=2, dates="Feb 6–7", acts="D"),
 dict(n=4,  name="Fox River", lat=-42.018, lng=171.373, nights=3, dates="Feb 8–10", acts="DT"),
 dict(n=5,  name="Greymouth", lat=-42.450, lng=171.207, nights=2, dates="Feb 11–12", acts="DH"),
 dict(n=6,  name="Lake Kaniere", lat=-42.840, lng=171.152, nights=2, dates="Feb 13–14", acts="DT"),
 dict(n=7,  name="Arthur's Pass 1", lat=-42.942, lng=171.564, nights=2, dates="Feb 15–16", acts="DT"),
 dict(n=8,  name="Arthur's Pass 2", lat=-42.942, lng=171.564, nights=2, dates="Feb 17–18", acts="DT"),
 dict(n=9,  name="Arthur's Pass 3", lat=-42.942, lng=171.564, nights=2, dates="Feb 19–20", acts="D"),
 dict(n=10, name="Oxford", lat=-43.297, lng=172.193, nights=7, dates="Feb 21–27", acts="DT"),
 dict(n=11, name="Lake Coleridge", lat=-43.363, lng=171.531, nights=3, dates="Feb 28 – Mar 2", acts="DH"),
 dict(n=12, name="Methven", lat=-43.626, lng=171.648, nights=1, dates="Mar 3", acts="D"),
 dict(n=13, name="Mt Somers", lat=-43.706, lng=171.392, nights=5, dates="Mar 4–8", acts="DT"),
 dict(n=14, name="Peel Forest", lat=-43.900, lng=171.256, nights=2, dates="Mar 9–10", acts="D"),
 dict(n=15, name="Geraldine", tag="FINISH", lat=-44.097, lng=171.243, nights=3, dates="Mar 11–13", acts="DH"),
]
ROUTE = [
 (-42.117,171.867),(-41.995,171.900),(-41.855,171.960),(-41.800,171.760),(-41.760,171.610),
 (-41.754,171.601),(-41.722,171.740),(-41.738,171.800),
 (-41.722,171.740),(-41.754,171.601),
 (-41.900,171.440),(-42.018,171.373),
 (-42.110,171.338),(-42.280,171.270),(-42.450,171.207),
 (-42.620,171.070),(-42.717,170.967),(-42.840,171.152),
 (-42.717,170.967),(-42.628,171.180),(-42.755,171.400),(-42.830,171.560),(-42.942,171.564),
 (-43.100,171.680),(-43.200,171.700),(-43.330,171.925),(-43.385,172.020),(-43.297,172.193),
 (-43.385,172.020),(-43.470,171.930),(-43.420,171.700),(-43.363,171.531),
 (-43.470,171.750),(-43.530,171.650),(-43.626,171.648),
 (-43.706,171.392),
 (-43.820,171.300),(-43.900,171.256),
 (-44.000,171.240),(-44.097,171.243),
]

# ---------- projection ----------
W, H = 640, 742
MINLON, MAXLON = 166.3, 174.45
MINLAT, MAXLAT = -46.95, -40.45
KX = math.cos(math.radians(-43.7))
def proj(lat, lon):
    x = (lon - MINLON) * KX
    y = (MAXLAT - lat)
    return x, y
maxx, maxy = proj(MINLAT, MAXLON)
S = min(W / maxx, H / maxy)
def XY(lat, lon):
    x, y = proj(lat, lon)
    return round(x * S, 1), round(y * S, 1)

# ---------- coastline ----------
polys = json.load(open('nz_polys_min.json'))
coast = []
for p in polys:
    for ring in p:
        pts = ' '.join(f"{XY(y,x)[0]},{XY(y,x)[1]}" for x, y in ring)
        coast.append(f'<polygon points="{pts}" class="land"/>')

# ---------- route ----------
rpts = ' '.join(f"{XY(a,b)[0]},{XY(a,b)[1]}" for a, b in ROUTE)

ICON = {'D':'🥾','T':'⛺','H':'🏛️'}
def icons(acts): return ' '.join(ICON[c] for c in acts)

# ---------- pins + label cards ----------
# absolute card top-left positions (planned against projected pin coords to avoid overlaps)
LAB = {
 1:(458,168,'l'), 2:(460,104,'l'), 3:(282,120,'r'), 4:(264,158,'r'), 5:(251,203,'r'),
 6:(247,248,'r'), 7:(445,238,'l'), 10:(484,296,'l'), 11:(277,306,'r'), 12:(452,336,'l'),
 13:(266,342,'r'), 14:(255,380,'r'), 15:(420,402,'l'),
}
svg_pins = []
CARD_W = 118
for s in STOPS:
    if s['n'] in (8, 9):
        continue
    x, y = XY(s['lat'], s['lng'])
    multi = s['n'] == 7
    label = '7–9' if multi else str(s['n'])
    LX, LY, anch = LAB[s['n']]
    if multi:
        nm, dt, ic = "Arthur's Pass ×3", "Feb 15–20 · 6 nights", icons('DT')
    else:
        nights = f"{s['nights']} night" + ('s' if s['nights'] > 1 else '')
        nm, dt, ic = s['name'], f"{s['dates']} · {nights}", icons(s['acts'])
    if s.get('tag'): nm += f" ({s['tag'].title()})"
    lx, ly = LX, LY
    # leader line to nearest card edge midpoint
    ex = lx if anch == 'l' else lx + CARD_W
    svg_pins.append(f'<line x1="{x}" y1="{y}" x2="{ex}" y2="{ly+14}" class="leader"/>')
    pin_cls = 'pin-g' if s.get('tag') else 'pin-r'
    rw = 34 if multi else 22
    svg_pins.append(
      f'<g><rect x="{lx}" y="{ly}" width="{CARD_W}" height="30" rx="5" class="card"/>'
      f'<text x="{lx+7}" y="{ly+12}" class="cardname">{nm}</text>'
      f'<text x="{lx+7}" y="{ly+24}" class="carddt">{dt}</text>'
      f'<text x="{lx+CARD_W-6}" y="{ly+13}" text-anchor="end" class="cardic">{ic}</text></g>')
    svg_pins.append(
      f'<g><rect x="{x-rw/2}" y="{y-11}" width="{rw}" height="22" rx="11" class="{pin_cls}"/>'
      f'<text x="{x}" y="{y+4.5}" text-anchor="middle" class="pintxt">{label}</text></g>')

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="{W}" height="{H}" fill="#cfe0dc"/>
  {''.join(coast)}
  <text x="60" y="95" class="sea">TASMAN&#160;&#160;SEA</text>
  <text x="455" y="520" class="sea">PACIFIC OCEAN</text>
  <text x="185" y="470" class="alps" transform="rotate(40 185 470)">S O U T H E R N&#160;&#160;&#160;A L P S</text>
  <polyline points="{rpts}" class="route-case"/>
  <polyline points="{rpts}" class="route"/>
  {''.join(svg_pins)}
  <g transform="translate(36,{H-64})">
    <circle r="24" class="comp"/><text y="-8" text-anchor="middle" class="compN">N</text>
    <path d="M 0 -4 L 5 12 L 0 8 L -5 12 Z" fill="#a93a2c"/>
  </g>
</svg>'''

logo = open('logo_b64.txt').read().strip()

rows = []
for s in STOPS:
    tag = f' <span class="ttag">({s["tag"].title()})</span>' if s.get('tag') else ''
    nights = f"{s['nights']}"
    rows.append(f'<tr><td class="c1">{s["n"]}</td><td class="c2">{s["name"]}{tag}</td>'
                f'<td class="c3">{s["dates"]}</td><td class="c4">{nights}</td>'
                f'<td class="c5">{icons(s["acts"])}</td></tr>')

FD = '/home/claude/safari/node_modules/@fontsource'
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'Oswald'; font-weight:600; src:url('file://{FD}/oswald/files/oswald-latin-600-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Oswald'; font-weight:700; src:url('file://{FD}/oswald/files/oswald-latin-700-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Special Elite'; font-weight:400; src:url('file://{FD}/special-elite/files/special-elite-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:400; src:url('file://{FD}/nunito-sans/files/nunito-sans-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:700; src:url('file://{FD}/nunito-sans/files/nunito-sans-latin-700-normal.woff2') format('woff2'); }}
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
.right {{ flex:1; display:flex; flex-direction:column; gap:3mm; }}
.land {{ fill:#ece1c2; stroke:#8a7452; stroke-width:1; }}
.sea {{ font-family:'Nunito Sans',sans-serif; font-style:italic; letter-spacing:4px; font-size:13px; fill:#7d9a94; }}
.alps {{ font-family:'Oswald',sans-serif; font-size:12px; letter-spacing:3px; fill:#a09274; }}
.route-case {{ fill:none; stroke:#fdf6e6; stroke-width:5.5; stroke-linejoin:round; }}
.route {{ fill:none; stroke:var(--red); stroke-width:2.6; stroke-dasharray:6 5; stroke-linejoin:round; }}
.leader {{ stroke:#8a7452; stroke-width:1; stroke-dasharray:2 2; }}
.card {{ fill:var(--cream); stroke:var(--ochre); stroke-width:1.1; }}
.cardname {{ font-family:'Oswald',sans-serif; font-weight:600; font-size:9.5px; fill:var(--navy); }}
.carddt {{ font-family:'Special Elite',cursive; font-size:8px; fill:var(--red); }}
.cardic {{ font-size:7px; }}
.pin-r {{ fill:var(--red); stroke:#fdf6e6; stroke-width:2; }}
.pin-g {{ fill:var(--green); stroke:#fdf6e6; stroke-width:2; }}
.pintxt {{ font-family:'Oswald',sans-serif; font-weight:600; font-size:11px; fill:#fff; }}
.comp {{ fill:rgba(250,245,232,.92); stroke:var(--navy); stroke-width:1.6; }}
.compN {{ font-family:'Oswald',sans-serif; font-weight:700; font-size:11px; fill:var(--navy); }}
.masthead {{ text-align:center; padding:2mm 3mm 2.5mm 22mm; background:var(--cream); border:1.2mm solid var(--navy); border-radius:3mm; position:relative; }}
.masthead img {{ position:absolute; left:2.5mm; top:50%; transform:translateY(-50%); width:17mm; }}
.kick {{ font-family:'Special Elite',cursive; font-size:8.5pt; letter-spacing:2px; color:var(--green); text-transform:uppercase; }}
h1 {{ font-family:'Oswald',sans-serif; font-size:21pt; line-height:1; color:var(--navy); text-transform:uppercase; letter-spacing:1px; }}
h1 .saf {{ color:var(--red); }}
.ribbon {{ display:inline-block; margin-top:1.5mm; background:var(--red); color:#fdf6e6; font-family:'Oswald',sans-serif;
  font-size:8pt; letter-spacing:1px; padding:1mm 5mm; text-transform:uppercase; white-space:nowrap;
  clip-path:polygon(8px 0, calc(100% - 8px) 0, 100% 50%, calc(100% - 8px) 100%, 8px 100%, 0 50%); }}
.tablebox {{ background:var(--cream); border:1.2mm solid var(--navy); border-radius:3mm; padding:2mm 3mm; flex:1; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ font-family:'Oswald',sans-serif; text-transform:uppercase; letter-spacing:1px; font-size:7.5pt; color:var(--cream);
  background:var(--navy); padding:1.2mm 1.5mm; text-align:left; }}
td {{ font-size:8.6pt; padding:1.5mm; border-bottom:0.3mm dashed #cbb98e; }}
tr:last-child td {{ border-bottom:none; }}
.c1 {{ font-family:'Oswald',sans-serif; font-weight:600; color:var(--red); width:6mm; }}
.c2 {{ font-weight:700; color:var(--navy); }}
.ttag {{ font-family:'Special Elite',cursive; font-size:7pt; color:var(--red); font-weight:400; }}
.c3 {{ font-family:'Special Elite',cursive; font-size:7.8pt; color:#6b4a2c; white-space:nowrap; }}
.c4 {{ text-align:center; width:9mm; font-family:'Oswald',sans-serif; }}
.c5 {{ font-size:7pt; white-space:nowrap; }}
.foot {{ background:var(--cream); border:1.2mm solid var(--navy); border-radius:3mm; padding:2mm 3mm; }}
.foot h3 {{ font-family:'Oswald',sans-serif; color:var(--red); text-transform:uppercase; letter-spacing:1.5px; font-size:9pt;
  border-bottom:0.5mm solid var(--ochre); display:inline-block; margin-bottom:1mm; }}
.foot p {{ font-size:7.6pt; line-height:1.5; }}
.legend {{ display:flex; gap:4mm; margin-top:1mm; font-size:7.6pt; align-items:center; flex-wrap:wrap; }}
.stamp {{ text-align:center; font-family:'Special Elite',cursive; font-size:8pt; color:var(--green); margin-top:1mm; }}
</style></head><body>
<div class="sheet">
  <div class="left">{svg}</div>
  <div class="right">
    <div class="masthead">
      <img src="data:image/png;base64,{logo}">
      <div class="kick">The Van Trampers Present</div>
      <h1>South Island <span class="saf">Safari</span></h1>
      <div class="ribbon">1 Feb – 14 Mar 2027 • 15 Hubs • 41 Nights</div>
    </div>
    <div class="tablebox">
      <table>
        <tr><th>#</th><th>Hub</th><th>Dates (nights there)</th><th>Nts</th><th>Options</th></tr>
        {''.join(rows)}
      </table>
      <div class="legend"><span>🥾 Day walks</span><span>⛺ Overnight tramp</span><span>🏛️ Heritage &amp; history</span></div>
      <div class="stamp" style="text-align:left; margin-top:2mm;">Coming soon: the Safari Handbook, hub-by-hub walk guides, DOC brochures &amp; GPX files on the shared drive.</div>
    </div>
    <div class="foot">
      <h3>How We Roll</h3>
      <p>Everything is optional — your safari, your choice. Happy Hour each evening to plan the next day.
      Weather calls the shots, WhatsApp keeps us together, and the taxi-van is $4 a leg (TBC).
      Route is approximate — stops &amp; order may change.</p>
      <div class="stamp">Good company · shared adventure · freedom to roam — it's your trip! 🚐</div>
    </div>
  </div>
</div>
</body></html>'''

open('fridge.html', 'w').write(html)
print('written', len(html))
