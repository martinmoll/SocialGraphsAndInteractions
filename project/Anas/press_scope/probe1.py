"""Stage 1: for every current House member, fetch the homepage and find the press-release listing URL."""
import json, re, sys, html, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
A = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)


def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25)
        return r.status, r.geturl(), r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, u, ""
    except Exception as e:
        return 0, u, type(e).__name__


def find_listing(base, page):
    cands = []
    for href, text in A.findall(page):
        t = re.sub(r"<[^>]+>|\s+", " ", html.unescape(text)).strip().lower()
        h = html.unescape(href)
        u = urllib.parse.urljoin(base, h)
        if urllib.parse.urlparse(u).netloc != urllib.parse.urlparse(base).netloc:
            continue
        hl = h.lower()
        score = 0
        if t in ("press releases", "press release", "news releases"):
            score += 10
        elif "press release" in t:
            score += 5
        if re.search(r"/press-releases/?$", hl):
            score += 8
        if "documentquery.aspx" in hl and "press" in t:
            score += 8
        if score:
            cands.append((score, u, t))
    cands.sort(key=lambda x: -x[0])
    return cands[0] if cands else None


def one(rec):
    bio, party, url, rss = rec
    st, final, page = get(url)
    out = dict(bioguide=bio, party=party, url=url, status=st, final=final, bytes=len(page))
    if st == 200:
        c = find_listing(final, page)
        if c:
            out.update(listing=c[1], anchor=c[2])
        fam = "drupal" if "drupal" in page.lower() or "/sites/evo-subsites/" in page or "pager__item" in page else (
            "aspnet" if "documentsingle.aspx" in page.lower() or "documentquery.aspx" in page.lower() else "other")
        out["family"] = fam
    time.sleep(0.3)
    return out


reps = json.load(open(sys.argv[1]))
with ThreadPoolExecutor(8) as ex:
    rows = list(ex.map(one, reps))
json.dump(rows, open(sys.argv[2], "w"), indent=1)
import collections
print(collections.Counter(r["status"] for r in rows))
print(collections.Counter(r.get("family") for r in rows))
print("with listing:", sum("listing" in r for r in rows))
