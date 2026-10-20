# Drama Vault – static site (no dependencies)
Needs only Python 3.9+. No database, no npm.

## Build
    SITE_URL=https://yourdomain.com SITE_NAME="Your Brand" python3 build.py
Output is the `dist/` folder: upload it to any static host (Cloudflare Pages, Netlify, GitHub Pages, shared hosting).
Preview locally: `cd dist && python3 -m http.server 8000`.

## Add a drama
Edit `content/data.json`. Set `"status":"published"` only when you have at least one entry in `sources` (url, note, checked date). The build fails otherwise. `fixture` and `draft` records are noindex and left out of the sitemap.
Source format: `{"url":"https://...","note":"what it confirms","checked":"2026-10-20"}`.
Viewing link format: `{"label":"Official channel","url":"https://...","owner":"Broadcaster","checked":"2026-10-20"}` – add only if you confirmed it is authorized.

## Before launch
1. Replace the 3 fixture dramas with verified records. 2. Fill in the draft legal pages (contact email, privacy, terms) and get them reviewed. 3. Set SITE_URL, rebuild, upload `dist/`. 4. Submit `/sitemap.xml` in Google Search Console and Bing Webmaster Tools. 5. On Cloudflare Pages: build command `python3 build.py`, output directory `dist`, env var SITE_URL.
## Not included
Ads, analytics, accounts, Urdu interface, images. Add them only after updating the privacy page.

## Images
Covers, logo and hero are original SVG artwork made for this site (no third-party images). To use a real licensed image for a drama, put the file in `static/img/` and add to its record:
`"image":{"file":"/img/waris.jpg","alt":"...","width":600,"height":400,"credit":"Photographer/source","license":"CC BY 4.0 / permission granted"}`
