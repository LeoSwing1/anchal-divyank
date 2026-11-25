#!/usr/bin/env python3
"""Stamp your live domain into the link-preview tags.

    python3 set-domain.py anchal-divyank.netlify.app

Run this once after deploying. WhatsApp and Facebook need absolute URLs,
so the preview card will not appear until this is done.
"""
import io, re, sys, os

def main():
    if len(sys.argv) != 2:
        print(__doc__); return 1
    d = sys.argv[1].strip().rstrip('/')
    d = re.sub(r'^https?://', '', d)
    if not re.match(r'^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$', d):
        print(f"'{d}' does not look like a domain."); return 1
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    s = io.open(p, encoding='utf-8').read()
    if 'SITE_URL' not in s:
        cur = re.search(r'<meta property="og:url" content="([^"]+)"', s)
        print(f"Already stamped ({cur.group(1) if cur else '?'}). Rewriting.")
        s = re.sub(r'(https://)[^/"]+(/(?:og-preview\.jpg)?")', r'\1SITE_URL\2', s)
    n = s.count('SITE_URL')
    s = s.replace('SITE_URL', d)
    io.open(p, 'w', encoding='utf-8').write(s)
    print(f"Done — {n} tags now point at https://{d}/")
    print(f"Preview card: https://{d}/og-preview.jpg")
    print("Re-scrape at https://developers.facebook.com/tools/debug/ to refresh WhatsApp's cache.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
