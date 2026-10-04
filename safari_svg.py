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
# Pin groups: (label, [hub numbers], pixel nudge at the fridge-map scale) — nudges keep 7 and 8–9 apart.
PIN_GROUPS = [('8–9', [8, 9], (13, 9))]
# single-hub pins that would otherwise touch a neighbour (Denniston/Westport, Methven/Mt Somers)
PIN_NUDGE = {2: (4, -3), 3: (-4, 3), 12: (3, -2)}
REF_S = 108.6   # px per degree on the fridge map, which the nudges were planned against

def group_width(pin_w):
    return pin_w + round(pin_w * 0.55)

def pin_positions(P, pin_w=22, pin_h=22, gap=1.5):
    """Return [(label, [ns], x, y, is_start_finish)] in drawing order.
    Starts from the hand-planned nudges (scaled to this map), then pushes any pins that still
    overlap apart, so the same data works on the fridge map, the og image and the T-shirt."""
    k = P.S / REF_S
    grouped = {n for _, ns, _ in PIN_GROUPS for n in ns}
    items = []   # [label, ns, x, y, sf, w]
    for s in STOPS:
        if s['n'] in grouped:
            continue
        x, y = P.xy(s['lat'], s['lng'])
        dx, dy = PIN_NUDGE.get(s['n'], (0, 0))
        items.append([str(s['n']), [s['n']], x + dx * k, y + dy * k, bool(s.get('tag')), pin_w])
    for label, ns, (dx, dy) in PIN_GROUPS:
        ss = [s for s in STOPS if s['n'] in ns]
        lat = sum(s['lat'] for s in ss) / len(ss); lng = sum(s['lng'] for s in ss) / len(ss)
        x, y = P.xy(lat, lng)
        items.append([label, ns, x + dx * k, y + dy * k, False, group_width(pin_w)])
    for _ in range(80):
        moved = False
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                dx, dy = b[2] - a[2], b[3] - a[3]
                need_x, need_y = (a[5] + b[5]) / 2 + gap, pin_h + gap
                if abs(dx) < need_x and abs(dy) < need_y:
                    px, py = need_x - abs(dx), need_y - abs(dy)
                    if px <= py:
                        sx = 1 if dx >= 0 else -1
                        a[2] -= sx * px / 2; b[2] += sx * px / 2
                    else:
                        sy = 1 if dy >= 0 else -1
                        a[3] -= sy * py / 2; b[3] += sy * py / 2
                    moved = True
        if not moved:
            break
    items.sort(key=lambda t: t[1][0])
    return [(l, ns, round(x, 1), round(y, 1), sf) for l, ns, x, y, sf, w in items]

def pins_svg(P, pin_w=22, pin_h=22, font=11, cls_r='pin-r', cls_g='pin-g', cls_t='pintxt'):
    svg = []
    for label, ns, x, y, sf in pin_positions(P, pin_w, pin_h):
        rw = group_width(pin_w) if len(ns) > 1 else pin_w
        svg.append(
          f'<g><rect x="{x-rw/2:.1f}" y="{y-pin_h/2:.1f}" width="{rw}" height="{pin_h}" rx="{pin_h/2}" class="{cls_g if sf else cls_r}"/>'
          f'<text x="{x}" y="{y+font*0.36:.1f}" text-anchor="middle" class="{cls_t}">{label}</text></g>')
    return ''.join(svg)

if __name__ == '__main__':
    P = Proj(640, 742)
    for s in STOPS:
        print(s['n'], s['name'], P.xy(s['lat'], s['lng']))
    print('pins:', pin_positions(P))
