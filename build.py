#!/usr/bin/env python3
"""Assemble the final website (and a locally-testable variant) from the template.

Usage:  python3 build.py
Inputs: site_template.html, stops.js, logo_b64.txt, nz_polys_min.json, favicon_b64.txt, appletouch_b64.txt
Output: South_Island_Safari_Map.html  (single-file site, CDN assets — ship this)
        test_local.html               (same, but local leaflet/fonts from node_modules
                                       for offline/headless testing; needs `npm install`)
        South_Island_Safari_2027.ics  (calendar feed, via gen_ics.py — ship with the site)
"""
import safari_data, gen_ics
safari_data.validate()   # date chain / totals sanity check on stops.js before anything is built

tpl = open('site_template.html').read()
stops = open('stops.js').read()
logo = open('logo_b64.txt').read().strip()
nz = open('nz_polys_min.json').read()
favicon = open('favicon_b64.txt').read().strip()
appletouch = open('appletouch_b64.txt').read().strip()

final = (tpl.replace('__STOPS__', stops).replace('__LOGO__', logo).replace('__NZ__', nz)
            .replace('__FAVICON__', favicon).replace('__APPLETOUCH__', appletouch))
open('South_Island_Safari_Map.html', 'w').write(final)

test = final.replace('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css',
                     'node_modules/leaflet/dist/leaflet.css')
test = test.replace('https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js',
                    'node_modules/leaflet/dist/leaflet.js')
test = test.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '')
test = test.replace('<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Special+Elite&family=Nunito+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">',
 '<link rel="stylesheet" href="node_modules/@fontsource/oswald/index.css">'
 '<link rel="stylesheet" href="node_modules/@fontsource/oswald/600.css">'
 '<link rel="stylesheet" href="node_modules/@fontsource/oswald/700.css">'
 '<link rel="stylesheet" href="node_modules/@fontsource/special-elite/index.css">'
 '<link rel="stylesheet" href="node_modules/@fontsource/nunito-sans/index.css">'
 '<link rel="stylesheet" href="node_modules/@fontsource/nunito-sans/700.css">')
open('test_local.html', 'w').write(test)
print('Built South_Island_Safari_Map.html and test_local.html')

gen_ics.write()          # the "Add to my calendar" feed, from the same stops.js
