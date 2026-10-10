#!/usr/bin/env python3
"""Build South_Island_Safari_2027.ics — the subscribable calendar behind the site's
"Add to my calendar" button: one all-day event per hub, spanning the nights there.

build.py runs this, so the calendar can't drift from the site. Subscribers (webcal / Google
"add by URL") re-fetch it about daily, so a stops.js change + push updates everyone's
calendars; the fixed per-hub UIDs make that an update rather than a duplicate.
Checked by `node ics_test.js`.
"""
import os
from safari_data import STOPS, HERE

SITE = 'https://zombiez4git.github.io/van-trampers-safari/'
OUT = 'South_Island_Safari_2027.ics'
# RFC 5545 requires a DTSTAMP; fixed so rebuilds without data changes are byte-identical
DTSTAMP = '20261011T000000Z'

ACT = {'tramp': '⛺ Overnight tramp options', 'heritage': '🏛️ Heritage & history'}
FUN = {'bike': '🚲 Bring the bikes', 'pie': '🥧 Famous pie stop'}


def ymd(s):
    """'Mon 1 Feb' -> '20270201'."""
    _, day, mon = s.split()
    return '2027%s%02d' % ({'Feb': '02', 'Mar': '03'}[mon], int(day))


def esc(text):
    """Escape a TEXT value (backslash, comma, semicolon, newline)."""
    return (text.replace('\\', '\\\\').replace(',', '\\,').replace(';', '\\;')
                .replace('\n', '\\n'))


def fold(line):
    """Fold to 75-octet lines (continuations start with a space), never splitting a UTF-8 char."""
    out, cur, limit = [], b'', 75
    for ch in line:
        b = ch.encode('utf-8')
        if len(cur) + len(b) > limit:
            out.append(cur.decode('utf-8'))
            cur, limit = b'', 74          # the leading space takes one octet
        cur += b
    out.append(cur.decode('utf-8'))
    return '\r\n '.join(out)


def event(s):
    nights = f"{s['nights']} night" + ('s' if s['nights'] > 1 else '')
    tag = f" ({s['tag'].title()})" if s.get('tag') else ''
    options = ['🥾 Day walks'] + [ACT[a] for a in s['acts']] + [FUN[f] for f in s.get('fun', [])]
    desc = '\n'.join(
        [s['blurb'], '',
         f"Arrive {s['arr']} · depart {s['dep']}",
         'On the menu: ' + ' · '.join(options),
         'Site ID: ' + s['ids']]
        + ([s['note']] if s.get('note') else [])
        + ['', 'Map & full itinerary: ' + SITE])
    return [
        'BEGIN:VEVENT',
        f"UID:safari2027-hub{s['n']:02d}@zombiez4git.github.io",
        'DTSTAMP:' + DTSTAMP,
        'DTSTART;VALUE=DATE:' + ymd(s['arr']),
        'DTEND;VALUE=DATE:' + ymd(s['dep']),
        'SUMMARY:' + esc(f"🚐 Safari #{s['n']} · {s['name']}{tag} — {nights}"),
        'LOCATION:' + esc(f"{s['name']}, New Zealand"),
        f"GEO:{s['lat']};{s['lng']}",
        # exact pin for Apple Maps (plain LOCATION text can geocode to the wrong "Cass")
        f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-RADIUS=1000;X-TITLE="{s["name"]}":'
        f"geo:{s['lat']},{s['lng']}",
        'DESCRIPTION:' + esc(desc),
        'URL:' + SITE,
        'TRANSP:TRANSPARENT',
        'END:VEVENT',
    ]


def build():
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Van Trampers//South Island Safari 2027//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        'X-WR-CALNAME:VT South Island Safari 2027',
        'X-WR-CALDESC:' + esc('Van Trampers South Island Safari · 1 Feb – 13 Mar 2027 · '
                              '15 hubs · 40 nights. ' + SITE),
        'X-WR-TIMEZONE:Pacific/Auckland',
        'REFRESH-INTERVAL;VALUE=DURATION:P1D',
        'X-PUBLISHED-TTL:P1D',
    ]
    for s in STOPS:
        lines += event(s)
    lines.append('END:VCALENDAR')
    return ''.join(fold(l) + '\r\n' for l in lines)


def write():
    with open(os.path.join(HERE, OUT), 'w', encoding='utf-8', newline='') as f:
        f.write(build())
    print('Built', OUT)


if __name__ == '__main__':
    write()
