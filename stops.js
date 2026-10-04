// Van Trampers South Island Safari — 1 Feb to 13 Mar 2027 (15 hubs, 40 nights)
// Source of truth: Aunty C's "VT South Island Safari 2027 Summary VT VERSION.pdf" (post-reccie, Sep/Oct 2026)
// dates = nights occupied (e.g. Arr Feb 1 / Dep Feb 4 -> "Feb 1–3", 3 nights)
// acts: tramp = overnight/multi-day tramp options, heritage = heritage & history
//       (day walks are on the menu at every hub, so they're not flagged individually)
// fun:  bike = a ride worth packing the bikes for, pie = a famous bakery pie
// ids:  Aunty C's Site IDs from the shared-drive walk collection
const STOPS = [
  {n:1,  name:"Reefton", tag:"START", lat:-42.117, lng:171.867, nights:3, dates:"Feb 1–3",  arr:"Mon 1 Feb", dep:"Thu 4 Feb", acts:["tramp","heritage"], fun:["pie"], ids:"6531", blurb:"Gold-rush town — first place in NZ lit by electric light, and home to a legendary bakery pie."},
  {n:2,  name:"Denniston", lat:-41.738, lng:171.800, nights:2, dates:"Feb 4–5", arr:"Thu 4 Feb", dep:"Sat 6 Feb", acts:["heritage"], fun:[], ids:"6455", blurb:"Historic coal plateau and the famous Denniston Incline."},
  {n:3,  name:"Westport", lat:-41.754, lng:171.601, nights:2, dates:"Feb 6–7", arr:"Sat 6 Feb", dep:"Mon 8 Feb", acts:[], fun:["bike"], ids:"6479", blurb:"Buller River port town — Cape Foulwind seals, and the Kawatiri Coastal Trail for the bikes.", note:"We roll out on Mon 8 Feb — Waitangi Day (observed)."},
  {n:4,  name:"Fox River", lat:-42.018, lng:171.373, nights:2, dates:"Feb 8–9", arr:"Mon 8 Feb", dep:"Wed 10 Feb", acts:["tramp"], fun:[], ids:"6507", blurb:"Paparoa limestone country — river gorges, caves and the Inland Pack Track."},
  {n:5,  name:"Greymouth", lat:-42.450, lng:171.207, nights:2, dates:"Feb 10–11", arr:"Wed 10 Feb", dep:"Fri 12 Feb", acts:["heritage"], fun:[], ids:"6635", blurb:"The Coast's big smoke — history, breweries and beaches."},
  {n:6,  name:"Lake Kaniere", lat:-42.840, lng:171.152, nights:2, dates:"Feb 12–13", arr:"Fri 12 Feb", dep:"Sun 14 Feb", acts:["tramp"], fun:[], ids:"6727", blurb:"Bush-fringed lake near Hokitika — water race walkway."},
  {n:7,  name:"Arthur's Pass", lat:-42.942, lng:171.564, nights:2, dates:"Feb 14–15", arr:"Sun 14 Feb", dep:"Tue 16 Feb", acts:["tramp"], fun:[], ids:"7682", blurb:"Alpine village — Devils Punchbowl Falls, valley tramps and cheeky kea."},
  {n:8,  name:"Hawdon Valley", lat:-42.988, lng:171.748, nights:4, dates:"Feb 16–19", arr:"Tue 16 Feb", dep:"Sat 20 Feb", acts:["tramp"], fun:[], ids:"7676", blurb:"Grassy flats beside a braided river off Mt White Road — gateway to Hawdon Hut and the Edwards."},
  {n:9,  name:"Cass", lat:-43.031, lng:171.758, nights:1, dates:"Feb 20", arr:"Sat 20 Feb", dep:"Sun 21 Feb", acts:[], fun:["bike"], ids:"7680", blurb:"Tiny railway halt immortalised by Rita Angus — high-country gravel roads made for a pedal."},
  {n:10, name:"Oxford", lat:-43.297, lng:172.193, nights:7, dates:"Feb 21–27", arr:"Sun 21 Feb", dep:"Sun 28 Feb", acts:["tramp"], fun:["pie"], ids:"7488 / 7480", blurb:"A whole week in the Canterbury foothills — forest walks, a Sunday market and a pie worth the drive."},
  {n:11, name:"Lake Coleridge", lat:-43.363, lng:171.531, nights:3, dates:"Feb 28 – Mar 2", arr:"Sun 28 Feb", dep:"Wed 3 Mar", acts:["heritage"], fun:[], ids:"7695 / 7694", blurb:"High-country hydro village — power station running since 1914."},
  {n:12, name:"Methven", lat:-43.626, lng:171.648, nights:1, dates:"Mar 3", arr:"Wed 3 Mar", dep:"Thu 4 Mar", acts:[], fun:[], ids:"7730", blurb:"Quick overnighter beneath Mt Hutt."},
  {n:13, name:"Mt Somers", lat:-43.706, lng:171.392, nights:3, dates:"Mar 4–6", arr:"Thu 4 Mar", dep:"Sun 7 Mar", acts:["tramp"], fun:[], ids:"7828 / 7813 / 7810 / 7807", blurb:"Three nights for Woolshed Creek, canyon country and the subalpine Mt Somers track."},
  {n:14, name:"Hakatere", lat:-43.683, lng:171.103, nights:3, dates:"Mar 7–9", arr:"Sun 7 Mar", dep:"Wed 10 Mar", acts:[], fun:[], ids:"8014", blurb:"Ashburton Lakes high country — 1860s station buildings, tussock basins and Mt Sunday (aka Edoras)."},
  {n:15, name:"Geraldine", tag:"FINISH", lat:-44.097, lng:171.243, nights:3, dates:"Mar 10–12", arr:"Wed 10 Mar", dep:"Sat 13 Mar", acts:["heritage"], fun:[], ids:"7880", blurb:"Berries, bakeries and a well-earned finish-line toast."},
];

// Approximate road route (SH6/SH67 down the Coast, SH73 over the pass, SH72 inland scenic).
// Out-and-back legs: Westport<->Denniston, Hokitika<->Lake Kaniere, Cass<->Hawdon Valley (Mt White Rd),
// Mt Somers<->Hakatere (Ashburton Gorge Rd).
const ROUTE = [
  [-42.117,171.867],[-41.995,171.900],[-41.855,171.960],[-41.800,171.760],[-41.760,171.610],
  [-41.754,171.601],[-41.722,171.740],[-41.738,171.800], // Reefton->Westport turnoff->Denniston
  [-41.722,171.740],[-41.754,171.601], // back to Westport
  [-41.900,171.440],[-42.018,171.373], // Charleston -> Fox River
  [-42.110,171.338],[-42.280,171.270],[-42.450,171.207], // Punakaiki -> Greymouth
  [-42.620,171.070],[-42.717,170.967],[-42.840,171.152], // Hokitika -> Lake Kaniere
  [-42.717,170.967],[-42.628,171.180],[-42.755,171.400],[-42.830,171.560],[-42.942,171.564], // SH73 -> Arthur's Pass
  [-42.985,171.610],[-43.025,171.690],[-43.031,171.758], // SH73 east past Cass
  [-43.034,171.775],[-43.003,171.785],[-42.988,171.748], // Mt White Rd over the bridge -> Hawdon Valley
  [-43.003,171.785],[-43.034,171.775],[-43.031,171.758], // back to Cass
  [-43.090,171.780],[-43.200,171.700],[-43.330,171.925],[-43.385,172.020],[-43.297,172.193], // Lake Pearson, Porters Pass, Springfield -> Oxford
  [-43.385,172.020],[-43.470,171.930],[-43.420,171.700],[-43.363,171.531], // -> Lake Coleridge
  [-43.470,171.750],[-43.530,171.650],[-43.626,171.648], // Rakaia Gorge -> Methven
  [-43.706,171.392], // Mt Somers
  [-43.690,171.300],[-43.672,171.200],[-43.683,171.103], // Ashburton Gorge Rd -> Hakatere
  [-43.672,171.200],[-43.690,171.300],[-43.706,171.392], // back to Mt Somers
  [-43.828,171.415],[-43.990,171.300],[-44.097,171.243], // SH72 Mayfield, Arundel -> Geraldine
];
