# Anchal & Divyank — wedding invitation

Run locally: `python3 -m http.server 8000` in this folder, open http://localhost:8000
(or double-click `start-windows.bat`). No npm, no build step.

## Deploy

1. Upload this whole folder to Netlify / Vercel / Cloudflare Pages, or to `public_html`
   on cPanel hosting. Caching rules for all three are already included
   (`_headers`, `vercel.json`, `.htaccess`).
2. Stamp your live domain into the link-preview tags — **required**, WhatsApp needs
   absolute URLs and the preview card will not appear until you do this:

       python3 set-domain.py your-domain.com

3. If you share the link before step 2, re-scrape it at
   https://developers.facebook.com/tools/debug/ to clear WhatsApp's cached preview.

## Link preview

`og-preview.jpg` (1200×630) is the card shown when the link is pasted or forwarded in
WhatsApp, Instagram DMs, iMessage or Facebook. It is composed from the invitation's own
rendered artwork — the jhalar toran, the jewelled mandala and the star frieze are the
same canvas ornaments the site draws — so the preview and the page match exactly.
To change it, replace the file, keeping the name and the 1200×630 dimensions.

The page is `noindex, nofollow` so it stays out of Google. That does not block WhatsApp
or Facebook previews — those still work.

## Editing the details

Everything guests see lives in `wedding-config.js`: names, parents, dates, events,
programme times, venue, RSVP numbers, music. Edit and reload — no rebuild.

Per-guest links: `?to=Guest%20Name` (e.g. `...netlify.app/?to=Sharma%20Family`).

## Still to confirm

- **10 December venue** is showing "Venue to be confirmed" — fill in `events[0].venue`.
- **Vidai time** on 12 December is blank — set `events[2].start` if there is one.
- Hindi spellings are transliterations; check them with the family, especially
  श्री देवेंद्र सिंह कलखंडे.
- RSVP WhatsApp uses +91 92196 09999. Confirm it is WhatsApp-enabled.
- Music is "Din Shagna Da" (instrumental). It is a copyrighted composition — for a
  public link, consider swapping in a royalty-free track via `music.file`.

## Performance and animation notes

The ornament artwork is drawn on canvas by an engine in the bundle. Changes made:

- Frame scheduling is locked to the display's refresh rate with an adaptive integer
  cadence, instead of a fixed 31 ms timer that produced an uneven ~32 fps and beat
  against vsync. Ornament redraw measured 30 fps → 57 fps.
- Canvases whose appearance has not changed skip their repaint, with the threshold
  relaxing automatically when the device is under load.
- The sheen and lamp-glow gradients are rendered once into sprites rather than rebuilt
  every frame.
- `--sheen` is written to the document ~7× less often; it was invalidating style on
  every element on every frame.
- Canvas resolution adapts to the device instead of a fixed cap.
- Every looping CSS animation now moves only `transform` and `opacity`. The music-button
  pulse and the "happening now" chip were animating `box-shadow`; the phone-number
  underline was animating `background-size`.
- `backdrop-filter` is gone from the four fixed elements (language switch, music button,
  dock, toast). Blurring a backdrop behind a fixed element re-runs on every scroll frame
  and was the single biggest cause of scroll stutter on phones.
- The Google Maps iframe and its 7-function colour filter are promoted to their own
  layer, so the filter result is cached instead of recomputed while scrolling.
- Audio no longer downloads during page load; it warms up 300 ms after the page is
  ready, so 639 KB is off the critical path. Playback still starts on the gate tap.

Measured on an emulated Pixel 7 (software renderer, so a real phone will be better):
scroll jitter fell from 12.3 ms to 6.7 ms standard deviation, and dropped frames from
107/188 to 36/188. Idle is a steady 60 fps.

Google Fonts and Google Maps need an internet connection. Reduced-motion preferences
are respected throughout.
