// Van Trampers South Island Safari — 1 Feb to 14 Mar 2027
// Source of truth: Aunty C's Word summary table (Draft 5.07.26)
// dates = nights occupied (e.g. Arr Feb 1 / Dep Feb 4 -> "Feb 1–3", 3 nights)
const STOPS = [
  {n:1,  name:"Reefton", tag:"START", lat:-42.117, lng:171.867, nights:3, dates:"Feb 1–3",  arr:"Mon 1 Feb", dep:"Thu 4 Feb", acts:["day","tramp","heritage"], refs:"6531", blurb:"Gold-rush town — first place in NZ lit by electric light."},
  {n:2,  name:"Denniston", lat:-41.738, lng:171.800, nights:2, dates:"Feb 4–5", arr:"Thu 4 Feb", dep:"Sat 6 Feb", acts:["day","heritage"], refs:"6465", blurb:"Historic coal plateau and the famous Denniston Incline."},
  {n:3,  name:"Westport", lat:-41.754, lng:171.601, nights:2, dates:"Feb 6–7", arr:"Sat 6 Feb", dep:"Mon 8 Feb", acts:["day"], refs:"6479 / 6476", blurb:"Buller River port town — gateway to Cape Foulwind."},
  {n:4,  name:"Fox River", lat:-42.018, lng:171.373, nights:3, dates:"Feb 8–10", arr:"Mon 8 Feb", dep:"Thu 11 Feb", acts:["day","tramp"], refs:"6507", blurb:"Paparoa limestone country — river gorges and caves."},
  {n:5,  name:"Greymouth", lat:-42.450, lng:171.207, nights:2, dates:"Feb 11–12", arr:"Thu 11 Feb", dep:"Sat 13 Feb", acts:["day","heritage"], refs:"6625 / 6627 / 6635", blurb:"The Coast's big smoke — history, breweries and beaches."},
  {n:6,  name:"Lake Kaniere", lat:-42.840, lng:171.152, nights:2, dates:"Feb 13–14", arr:"Sat 13 Feb", dep:"Mon 15 Feb", acts:["day","tramp"], refs:"6727", blurb:"Bush-fringed lake near Hokitika — water race walkway."},
  {n:7,  name:"Arthur's Pass 1", lat:-42.942, lng:171.564, nights:2, dates:"Feb 15–16", arr:"Mon 15 Feb", dep:"Wed 17 Feb", acts:["day","tramp"], refs:"7670 / 7681 / 7682", blurb:"Alpine village, waterfalls — and cheeky kea."},
  {n:8,  name:"Arthur's Pass 2", lat:-42.942, lng:171.564, nights:2, dates:"Feb 17–18", arr:"Wed 17 Feb", dep:"Fri 19 Feb", acts:["day","tramp"], refs:"7676", blurb:"Second stint in the pass — valley tramps and viewpoints."},
  {n:9,  name:"Arthur's Pass 3", lat:-42.942, lng:171.564, nights:2, dates:"Feb 19–20", arr:"Fri 19 Feb", dep:"Sun 21 Feb", acts:["day"], refs:"7680", blurb:"Last of the alpine leg before dropping to the plains."},
  {n:10, name:"Oxford", lat:-43.297, lng:172.193, nights:7, dates:"Feb 21–27", arr:"Sun 21 Feb", dep:"Sun 28 Feb", acts:["day","tramp"], refs:"7478 / 7480", blurb:"A whole week in the Canterbury foothills — forest walks aplenty."},
  {n:11, name:"Lake Coleridge", lat:-43.363, lng:171.531, nights:3, dates:"Feb 28 – Mar 2", arr:"Sun 28 Feb", dep:"Wed 3 Mar", acts:["day","heritage"], refs:"7695 / 7694", blurb:"High-country hydro village — power station running since 1914."},
  {n:12, name:"Methven", lat:-43.626, lng:171.648, nights:1, dates:"Mar 3", arr:"Wed 3 Mar", dep:"Thu 4 Mar", acts:["day"], refs:"7730", blurb:"Quick overnighter beneath Mt Hutt."},
  {n:13, name:"Mt Somers", lat:-43.706, lng:171.392, nights:5, dates:"Mar 4–8", arr:"Thu 4 Mar", dep:"Tue 9 Mar", acts:["day","tramp"], refs:"7828 / 7813 / 7810 / 7807", blurb:"Five nights for the subalpine circuit and canyon country."},
  {n:14, name:"Peel Forest", lat:-43.900, lng:171.256, nights:2, dates:"Mar 9–10", arr:"Tue 9 Mar", dep:"Thu 11 Mar", acts:["day"], refs:"7846", blurb:"Ancient tōtara and kahikatea — big trees, easy walks."},
  {n:15, name:"Geraldine", tag:"FINISH", lat:-44.097, lng:171.243, nights:3, dates:"Mar 11–13", arr:"Thu 11 Mar", dep:"Sun 14 Mar", acts:["day","heritage"], refs:"7880 / 7858 / 7855", blurb:"Berries, bakeries and a well-earned finish-line toast."},
];

// Approximate road route (SH6/SH67 down the Coast, SH73 over the pass, SH72 inland scenic)
const ROUTE = [
  [-42.117,171.867],[-41.995,171.900],[-41.855,171.960],[-41.800,171.760],[-41.760,171.610],
  [-41.754,171.601],[-41.722,171.740],[-41.738,171.800], // Reefton->Westport turnoff->Denniston
  [-41.722,171.740],[-41.754,171.601], // back to Westport
  [-41.900,171.440],[-42.018,171.373], // Charleston -> Fox River
  [-42.110,171.338],[-42.280,171.270],[-42.450,171.207], // Punakaiki -> Greymouth
  [-42.620,171.070],[-42.717,170.967],[-42.840,171.152], // Hokitika -> Lake Kaniere
  [-42.717,170.967],[-42.628,171.180],[-42.755,171.400],[-42.830,171.560],[-42.942,171.564], // SH73 -> Arthur's Pass
  [-43.100,171.680],[-43.200,171.700],[-43.330,171.925],[-43.385,172.020],[-43.297,172.193], // -> Oxford
  [-43.385,172.020],[-43.470,171.930],[-43.420,171.700],[-43.363,171.531], // -> Lake Coleridge
  [-43.470,171.750],[-43.530,171.650],[-43.626,171.648], // Rakaia Gorge -> Methven
  [-43.706,171.392], // Mt Somers
  [-43.820,171.300],[-43.900,171.256], // Peel Forest
  [-44.000,171.240],[-44.097,171.243], // Geraldine
];
