// Checks South_Island_Safari_2027.ics (written by gen_ics.py via build.py) against stops.js:
// one all-day event per hub spanning the nights there, stable UIDs, and RFC 5545 plumbing
// (CRLF line endings, lines folded at 75 octets, escaped text) so iPhone/Google/Outlook all take it.
// Usage: node ics_test.js   (exits non-zero on any failure)
const fs = require('fs'), vm = require('vm');

const ctx = {};
vm.runInNewContext(fs.readFileSync('stops.js', 'utf8') + '\nthis.STOPS = STOPS;', ctx);
const STOPS = ctx.STOPS;
if (!fs.existsSync('South_Island_Safari_2027.ics')) {
  console.log('FAIL: South_Island_Safari_2027.ics missing — run python build.py');
  process.exit(1);
}
const raw = fs.readFileSync('South_Island_Safari_2027.ics', 'utf8');

let fails = 0;
const check = (ok, msg) => { if (!ok) { fails++; console.log('FAIL:', msg); } };

// --- plumbing ---
check(raw.includes('\r\n') && !/[^\r]\n/.test(raw), 'every line ends in CRLF');
const physical = raw.split('\r\n');
const long = physical.filter(l => Buffer.byteLength(l, 'utf8') > 75);
check(long.length === 0, `lines folded at 75 octets (${long.length} too long, e.g. ${JSON.stringify(long[0])})`);
const lines = raw.replace(/\r\n[ \t]/g, '').split('\r\n').filter(Boolean);   // unfold
check(lines[0] === 'BEGIN:VCALENDAR' && lines[lines.length - 1] === 'END:VCALENDAR', 'wrapped in VCALENDAR');
check(lines.includes('VERSION:2.0'), 'VERSION:2.0');
check(lines.some(l => l.startsWith('PRODID:')), 'has PRODID');
check(lines.includes('X-WR-CALNAME:VT South Island Safari 2027'), 'calendar is named for subscribers');
check(lines.some(l => l.startsWith('REFRESH-INTERVAL')), 'subscribers are told to refresh');

// --- events ---
const events = [];
let cur = null;
for (const l of lines) {
  if (l === 'BEGIN:VEVENT') cur = {};
  else if (l === 'END:VEVENT') { events.push(cur); cur = null; }
  else if (cur) {
    const i = l.indexOf(':');
    cur[l.slice(0, i).split(';')[0]] = { params: l.slice(0, i), value: l.slice(i + 1) };
  }
}
check(events.length === STOPS.length, `one event per hub (${events.length} vs ${STOPS.length})`);

const unescape = v => v.replace(/\\n/gi, '\n').replace(/\\([,;\\])/g, '$1');
const ymd = s => {   // "Mon 1 Feb" -> "20270201"
  const [, day, mon] = s.split(' ');
  return '2027' + ({ Feb: '02', Mar: '03' })[mon] + day.padStart(2, '0');
};
const uids = new Set();
let nights = 0;
STOPS.forEach((s, i) => {
  const e = events[i] || {};
  const tag = `hub ${s.n} ${s.name}`;
  const get = k => (e[k] || {}).value || '';
  check(e.DTSTART && e.DTSTART.params === 'DTSTART;VALUE=DATE' && get('DTSTART') === ymd(s.arr), `${tag}: all-day start = arrival ${ymd(s.arr)} (got ${get('DTSTART')})`);
  check(e.DTEND && e.DTEND.params === 'DTEND;VALUE=DATE' && get('DTEND') === ymd(s.dep), `${tag}: all-day end = departure ${ymd(s.dep)} (got ${get('DTEND')})`);
  const sum = unescape(get('SUMMARY'));
  check(sum.includes(s.name) && sum.includes(`${s.nights} night${s.nights > 1 ? 's' : ''}`), `${tag}: summary names hub and nights (${sum})`);
  const desc = unescape(get('DESCRIPTION'));
  check(desc.includes(s.blurb), `${tag}: description has the blurb`);
  check(desc.includes('Site ID: ' + s.ids), `${tag}: description has Site ID ${s.ids}`);
  check(desc.includes('https://zombiez4git.github.io/van-trampers-safari/'), `${tag}: description links back to the map`);
  if (s.note) check(desc.includes(s.note), `${tag}: description has the hub note`);
  for (const k of ['SUMMARY', 'DESCRIPTION', 'LOCATION'])
    check(!/(^|[^\\])[,;]/.test(get(k)), `${tag}: ${k} commas/semicolons escaped`);
  check(unescape(get('LOCATION')).startsWith(s.name), `${tag}: location is the hub`);
  check(get('GEO') === `${s.lat};${s.lng}`, `${tag}: GEO is the pin position`);
  check(get('TRANSP') === 'TRANSPARENT', `${tag}: doesn't block people's calendars as busy`);
  const uid = get('UID');
  check(uid === `safari2027-hub${String(s.n).padStart(2, '0')}@zombiez4git.github.io`, `${tag}: stable UID (got ${uid})`);
  uids.add(uid);
  check(!!get('DTSTAMP'), `${tag}: has DTSTAMP`);
  nights += (Date.UTC(2027, +get('DTEND').slice(4, 6) - 1, +get('DTEND').slice(6)) -
             Date.UTC(2027, +get('DTSTART').slice(4, 6) - 1, +get('DTSTART').slice(6))) / 864e5;
});
check(uids.size === STOPS.length, 'UIDs unique');
check(nights === 40, `events cover 40 nights (got ${nights})`);

console.log(fails ? `${fails} check(s) failed` : `ICS OK — ${events.length} events, ${nights} nights`);
process.exit(fails ? 1 : 0);
