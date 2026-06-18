#!/usr/bin/env python3
"""Inline lane JSON files into shipment-dashboard.html so it opens pre-populated.

Usage:
    python3 embed-data.py [file1.json file2.json ...]
With no args, embeds every *.json in ~/Downloads that looks like a lane file.
Re-run any time to refresh the baked-in data.
"""
import json, sys, glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "shipment-dashboard.html")
TOKEN = '"__EMBEDDED_DATA__"'

def looks_like_lane(path):
    try:
        with open(path) as f:
            j = json.load(f)
        return isinstance(j.get("data"), list) and j["data"] and "legs" in j["data"][0]
    except Exception:
        return False

def main():
    args = sys.argv[1:]
    if args:
        files = args
    else:
        files = [p for p in glob.glob(os.path.expanduser("~/Downloads/*.json")) if looks_like_lane(p)]
    files = sorted(files)
    if not files:
        print("No lane JSON files found. Pass file paths as arguments.")
        return 1

    bundle = {}
    for p in files:
        with open(p) as f:
            bundle[os.path.basename(p)] = json.load(f)
        print(f"  + {os.path.basename(p)}  ({len(bundle[os.path.basename(p)]['data'])} options)")

    data_js = json.dumps(bundle, separators=(",", ":"))
    data_js = data_js.replace("</", "<\\/")  # keep it safe inside <script>

    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    # Replace the token (raw or already-embedded) with the fresh bundle.
    if TOKEN in html:
        html = html.replace(TOKEN, data_js, 1)
    else:
        html = re.sub(r'window\.EMBEDDED_LANES = .*?;</script>',
                      f'window.EMBEDDED_LANES = {data_js};</script>', html, count=1, flags=re.S)

    out = os.path.join(HERE, "shipment-dashboard.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nEmbedded {len(files)} lanes into {out}")
    print("Open it in your browser — it loads with everything ready.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
