"""Vector South Island map builder shared by the fridge-map PDF, the link-preview image
and the T-shirt artwork. Pure SVG, no tiles, so it renders identically everywhere."""
import json, math, os
from safari_data import STOPS, ROUTE, HERE

# ---------- projection (whole South Island, equirectangular, scaled to fit W x H) ----------
MINLON, MAXLON = 166.3, 174.45
MINLAT, MAXLAT = -46.95, -40.45
KX = math.cos(math.radians(-43.7))

class Proj:
    def __init__(self, W, H):
        self.W, self.H = W, H
        maxx = (MAXLON - MINLON) * KX
        maxy = (MAXLAT - MINLAT)
        self.S = min(W / maxx, H / maxy)
    def xy(self, lat, lon):
        return round((lon - MINLON) * KX * self.S, 1), round((MAXLAT - lat) * self.S, 1)

_POLYS = json.load(open(os.path.join(HERE, 'nz_polys_min.json')))

def coast_polygons(P, cls='land', south_only=False):
    """south_only drops the North Island (its ring reaches north of 40.3°S)."""
    out = []
    for p in _POLYS:
        for ring in p:
            if south_only and max(y for x, y in ring) > -40.3:
                continue
            pts = ' '.join(f"{P.xy(y, x)[0]},{P.xy(y, x)[1]}" for x, y in ring)
            out.append(f'<polygon points="{pts}" class="{cls}"/>')
    return ''.join(out)

def route_points(P):
    return ' '.join(f"{P.xy(a, b)[0]},{P.xy(a, b)[1]}" for a, b in ROUTE)

# Hubs 8 (Hawdon Valley) and 9 (Cass) are 5 km apart — one pin on a whole-island map.
# Pin groups: (label, [hub numbers], pixel nudge) — nudge keeps 7 and 8–9 from touching.
PIN_GROUPS = [('8–9', [8, 9], (13, 9))]
# single-hub pins that would otherwise touch a neighbour (Denniston/Westport, Methven/Mt Somers)
PIN_NUDGE = {2: (4, -3), 3: (-4, 3), 12: (3, -2)}

def pin_positions(P):
    """Return [(label, [ns], x, y, is_start_finish)] in drawing order."""
    grouped = {n for _, ns, _ in PIN_GROUPS for n in ns}
    out = []
    for s in STOPS:
        if s['n'] in grouped:
            continue
        x, y = P.xy(s['lat'], s['lng'])
        dx, dy = PIN_NUDGE.get(s['n'], (0, 0))
        out.append((str(s['n']), [s['n']], x + dx, y + dy, bool(s.get('tag'))))
    for label, ns, (dx, dy) in PIN_GROUPS:
        ss = [s for s in STOPS if s['n'] in ns]
        lat = sum(s['lat'] for s in ss) / len(ss); lng = sum(s['lng'] for s in ss) / len(ss)
        x, y = P.xy(lat, lng)
        out.append((label, ns, x + dx, y + dy, False))
    out.sort(key=lambda t: t[1][0])
    return out

def pins_svg(P, pin_w=22, pin_h=22, font=11, cls_r='pin-r', cls_g='pin-g', cls_t='pintxt'):
    svg = []
    for label, ns, x, y, sf in pin_positions(P):
        rw = pin_w + (12 if len(ns) > 1 else 0)
        svg.append(
          f'<g><rect x="{x-rw/2:.1f}" y="{y-pin_h/2:.1f}" width="{rw}" height="{pin_h}" rx="{pin_h/2}" class="{cls_g if sf else cls_r}"/>'
          f'<text x="{x}" y="{y+font*0.36:.1f}" text-anchor="middle" class="{cls_t}">{label}</text></g>')
    return ''.join(svg)

if __name__ == '__main__':
    P = Proj(640, 742)
    for s in STOPS:
        print(s['n'], s['name'], P.xy(s['lat'], s['lng']))
    print('pins:', pin_positions(P))
