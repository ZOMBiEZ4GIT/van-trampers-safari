"""Shared itinerary data for the Python generators (fridge map PDF, T-shirt artwork, link preview).

Mirrors stops.js (the website's copy). build.py checks the two stay in sync.
Source of truth: Aunty C's "VT South Island Safari 2027 Summary VT VERSION.pdf".
"""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))

TRIP = dict(start="1 Feb", finish="13 Mar", year=2027, hubs=15, nights=40,
            ribbon="1 Feb – 13 Mar 2027 • 15 Hubs • 40 Nights")

def _load_js():
    """Parse STOPS/ROUTE out of stops.js so there is one hand-edited itinerary."""
    src = open(os.path.join(HERE, 'stops.js'), encoding='utf-8').read()
    def block(name):
        m = re.search(r'const %s = (\[.*?\n\]);' % name, src, re.S)
        body = m.group(1)
        body = re.sub(r'//[^\n]*', '', body)                 # strip comments
        body = re.sub(r'(\{|,)\s*([A-Za-z_]\w*)\s*:', r'\1"\2":', body)  # quote keys
        body = re.sub(r',\s*([\]\}])', r'\1', body)          # trailing commas
        return json.loads(body)
    return block('STOPS'), block('ROUTE')

STOPS, ROUTE = _load_js()

def validate():
    """Date-chain and totals sanity check (raises on mismatch)."""
    import datetime as d
    def parse(s):
        day, mon = s.split()[1:3]
        return d.date(TRIP['year'], {'Feb':2,'Mar':3}[mon], int(day))
    total = 0
    for i, s in enumerate(STOPS):
        a, b = parse(s['arr']), parse(s['dep'])
        assert (b - a).days == s['nights'], f"{s['name']}: arr/dep span {(b-a).days} != nights {s['nights']}"
        assert a.strftime('%a') == s['arr'].split()[0] and b.strftime('%a') == s['dep'].split()[0], f"{s['name']}: weekday"
        if i: assert parse(STOPS[i-1]['dep']) == a, f"{s['name']}: chain broken"
        total += s['nights']
    assert total == TRIP['nights'], f"total nights {total} != {TRIP['nights']}"
    assert len(STOPS) == TRIP['hubs']
    assert STOPS[0]['arr'].endswith(TRIP['start']) and STOPS[-1]['dep'].endswith(TRIP['finish'])
    return total

if __name__ == '__main__':
    print(f"{len(STOPS)} hubs, {validate()} nights, {len(ROUTE)} route points — OK")
