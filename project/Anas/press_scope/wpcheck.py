"""Which member sites answer the WordPress posts API, and how many posts since 3 Jan 2025 (all categories)?"""
import json, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
def one(r):
    u = r["final"].rstrip("/") + "/wp-json/wp/v2/posts?per_page=1&_fields=id&after=2025-01-03T00:00:00"
    try:
        x = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20)
        return dict(bioguide=r["bioguide"], wp=x.status, total=x.headers.get("X-WP-Total"))
    except urllib.error.HTTPError as e:
        return dict(bioguide=r["bioguide"], wp=e.code, total=None)
    except Exception as e:
        return dict(bioguide=r["bioguide"], wp=0, total=None)
rows = json.load(open(sys.argv[1]))
with ThreadPoolExecutor(6) as ex: res = list(ex.map(one, rows))
json.dump(res, open(sys.argv[2], "w"))
import collections; print(collections.Counter((r["wp"], r["total"] is not None) for r in res))
