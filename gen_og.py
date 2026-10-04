#!/usr/bin/env python3
"""Build og.html — the 1200×630 link-preview card (WhatsApp/Facebook unfurls).
`node og_shot.js` screenshots it to og-image.jpg. Vector map, so no tiles/network needed."""
import os
from safari_data import STOPS, TRIP, HERE, validate
from safari_svg import Proj, coast_polygons, route_points, pins_svg

validate()
W, H = 420, 470
P = Proj(W, H)
svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
  {coast_polygons(P)}
  <polyline points="{route_points(P)}" class="route-case"/>
  <polyline points="{route_points(P)}" class="route"/>
  {pins_svg(P, pin_w=19, pin_h=19, font=10)}
</svg>'''
logo = open(os.path.join(HERE, 'logo_b64.txt')).read().strip()
FD = os.path.join(HERE, 'node_modules', '@fontsource')
def row(s):
    tag = f' <span class="tag">{s["tag"].title()}</span>' if s.get('tag') else ''
    return f'<div class="r"><span class="b{" g" if s.get("tag") else ""}">{s["n"]}</span><span class="nm">{s["name"]}{tag}</span><span class="dt">{s["dates"]}</span></div>'
rows = ''.join(row(s) for s in STOPS)
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'Oswald'; font-weight:600; src:url('file://{FD}/oswald/files/oswald-latin-600-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Oswald'; font-weight:700; src:url('file://{FD}/oswald/files/oswald-latin-700-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Special Elite'; src:url('file://{FD}/special-elite/files/special-elite-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:400; src:url('file://{FD}/nunito-sans/files/nunito-sans-latin-400-normal.woff2') format('woff2'); }}
@font-face {{ font-family:'Nunito Sans'; font-weight:700; src:url('file://{FD}/nunito-sans/files/nunito-sans-latin-700-normal.woff2') format('woff2'); }}
:root {{ --parch:#f2e9d4; --ink:#3d3020; --navy:#1e3a5f; --red:#a93a2c; --green:#3e6b4f; --ochre:#b07c2a; --cream:#faf5e8; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1200px; height:630px; overflow:hidden; font-family:'Nunito Sans',sans-serif; color:var(--ink);
  background:var(--parch); border:6px solid var(--navy); }}
header {{ display:flex; align-items:center; gap:18px; padding:14px 26px 12px; background:linear-gradient(180deg,#f7f0dd,#f0e6cc); border-bottom:3px double var(--navy); height:150px; }}
header img {{ width:104px; }}
.tb {{ flex:1; text-align:center; }}
.kick {{ font-family:'Special Elite'; font-size:15px; letter-spacing:2px; color:var(--green); text-transform:uppercase; }}
h1 {{ font-family:'Oswald'; font-weight:700; font-size:56px; line-height:1; color:var(--navy); text-transform:uppercase; letter-spacing:1px; }}
h1 span {{ color:var(--red); }}
.ribbon {{ display:inline-block; margin-top:8px; padding:5px 24px; background:var(--red); color:#fdf6e6; font-family:'Oswald'; font-weight:600; letter-spacing:2px; font-size:17px; text-transform:uppercase;
  clip-path:polygon(10px 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 10px 100%, 0 50%); }}
.van {{ width:104px; text-align:center; font-size:48px; filter:sepia(.3); }}
.main {{ display:flex; height:468px; }}
.map {{ width:470px; background:#cfe0dc; border-right:3px solid var(--navy); display:flex; align-items:center; justify-content:center; overflow:hidden; }}
.land {{ fill:#ece1c2; stroke:#8a7452; stroke-width:.8; }}
.route-case {{ fill:none; stroke:#fdf6e6; stroke-width:5; stroke-linejoin:round; }}
.route {{ fill:none; stroke:var(--red); stroke-width:2.4; stroke-dasharray:5 4; stroke-linejoin:round; }}
.pin-r {{ fill:var(--red); stroke:#fdf6e6; stroke-width:1.8; }}
.pin-g {{ fill:var(--green); stroke:#fdf6e6; stroke-width:1.8; }}
.pintxt {{ font-family:'Oswald'; font-weight:600; font-size:10px; fill:#fff; }}
.list {{ flex:1; padding:16px 22px; display:grid; grid-template-columns:1fr 1fr; grid-auto-rows:52px; column-gap:22px; align-content:start; background:var(--cream); }}
.r {{ display:flex; align-items:center; gap:10px; border-bottom:1px dashed #cbb98e; }}
.b {{ width:30px; height:30px; border-radius:50%; background:var(--red); color:#fff; font-family:'Oswald'; font-weight:600; font-size:15px; display:flex; align-items:center; justify-content:center; border:2px solid #7d2a1f; flex:none; }}
.b.g {{ background:var(--green); border-color:#2c4d39; }}
.nm {{ font-weight:700; color:var(--navy); font-size:17px; flex:1; }}
.tag {{ font-family:'Special Elite'; color:var(--red); font-size:11px; }}
.dt {{ font-family:'Special Elite'; color:var(--red); font-size:15px; white-space:nowrap; }}
.foot {{ grid-column:1 / -1; font-family:'Special Elite'; color:var(--green); font-size:15px; text-align:center; padding-top:10px; }}
</style></head><body>
<header><img src="data:image/png;base64,{logo}"><div class="tb"><div class="kick">The Van Trampers Present</div><h1>South Island <span>Safari</span></h1><div class="ribbon">{TRIP['ribbon']}</div></div><div class="van">🚐</div></header>
<div class="main"><div class="map">{svg}</div><div class="list">{rows}<div class="foot">Tap to explore the route, play the animated safari tour &amp; print the fridge map 🥾🚐⛰️</div></div></div>
</body></html>'''
open(os.path.join(HERE, 'og.html'), 'w').write(html)
print('written og.html')
