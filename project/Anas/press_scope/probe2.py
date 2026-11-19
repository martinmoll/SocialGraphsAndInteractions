"""Stage 2: per listing, count releases dated on or after 3 Jan 2025 by binary search over listing pages.

Count = k * per_page + (dates >= cutoff on boundary page k), where k is the first page whose oldest date
is before the cutoff. Pages are 0-based logical indices mapped to each layout's own parameter.
"""
import json, re, sys, html, time, datetime as dt, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
CUT = dt.date(2025, 1, 3)
MON = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
D1 = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20\d\d)\b")
D2 = re.compile(r"\b(\d{1,2})[/.](\d{1,2})[/.](20\d\d|\d\d)\b")
D3 = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b")


def get(u):
    for _ in range(2):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25)
            return r.read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(2)
    return ""


def main_part(h):
    h = re.sub(r"(?is)<(script|style|nav|footer|header|aside|noscript)\b.*?</\1>", " ", h)
    return h


def dates(h):
    h = main_part(h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    out = []
    for m, d, y in D1.findall(t):
        try: out.append(dt.date(int(y), MON[m[:3].lower()], int(d)))
        except ValueError: pass
    if not out:
        for a, b, y in D2.findall(t):
            y = int(y) + (2000 if len(y) == 2 else 0)
            try: out.append(dt.date(y, int(a), int(b)))
            except ValueError: pass
    if not out:
        for y, m, d in D3.findall(h):
            try: out.append(dt.date(int(y), int(m), int(d)))
            except ValueError: pass
    out = [x for x in out if dt.date(2000, 1, 1) <= x <= dt.date(2026, 12, 31)]
    if len(out) >= 3:  # drop dates quoted in titles ("September 11, 2001"): far from the page's median
        med = sorted(out)[len(out) // 2]
        out = [x for x in out if abs((x - med).days) <= 400]
    return out


def pager(listing, h):
    hl = html.unescape(h)
    if re.search(r"/page/\d+/", hl):
        base = listing.rstrip("/")
        return "wp", lambda n: base + "/" if n == 0 else f"{base}/page/{n + 1}/"
    if re.search(r"[?&]Page=\d+", hl):
        return "asp", lambda n: f"{listing}&Page={n + 1}" if "?" in listing else f"{listing}?Page={n + 1}"
    sep = "&" if "?" in listing else "?"
    if re.search(r"[?&]page=\d+", hl):
        # 0-based on most Drupal sites; 1-based where page=1 is the "Next" link (Fitzpatrick)
        one_based = bool(re.search(r'href="[^"]*[?&]page=1"[^>]*>\s*(?:1|First|«)', hl)) or "page=0" not in hl and bool(re.search(r'[?&]page=2"[^>]*>\s*Next', hl))
        off = 1 if one_based else 0
        return "drupal" + ("1" if off else ""), lambda n: f"{listing}{sep}page={n + off}"
    m = re.search(r"[?&]([A-Za-z_]*page[A-Za-z_]*)=2\b", hl, re.I)  # PageNum_rs=2 and similar
    if m:
        p = m.group(1)
        return "param:" + p, lambda n: f"{listing}{sep}{p}={n + 1}"
    return "none", None


def one(r):
    out = dict(bioguide=r["bioguide"], party=r["party"], listing=r.get("listing"))
    if not r.get("listing"):
        out["status"] = "no listing"; return out
    h0 = get(r["listing"]); time.sleep(0.4)
    d0 = dates(h0)
    kind, url = pager(r["listing"], h0)
    out.update(kind=kind, newest=str(max(d0)) if d0 else None, n_dates_p0=len(d0))
    if not d0:
        out["status"] = "no dates on listing"; return out
    if url is None:
        out.update(status="no pager", count=sum(x >= CUT for x in d0), lower_bound=True); return out
    if min(d0) < CUT:  # the first page already reaches back before the cutoff
        out.update(status="ok", per_page=len(d0), boundary_page=0, count=sum(x >= CUT for x in d0), requests=1,
                   oldest_seen=str(min(d0)))
        return out
    cache = {0: d0}

    def page(n):
        if n not in cache:
            ds = dates(get(url(n))); time.sleep(0.4)
            # a site that ignores out-of-range page numbers serves a page we have seen: treat as past the end
            cache[n] = [] if any(ds == v for k, v in cache.items() if ds) else ds
        return cache[n]

    p1 = page(1)
    if not p1 or p1 == d0:
        out.update(status="pager not followed", count=sum(x >= CUT for x in d0), lower_bound=True); return out
    per = len(p1)
    # exponential then binary search for first page whose oldest date < CUT (or empty page)
    lo, hi = 0, 1
    while True:
        ds = page(hi)
        if not ds or min(ds) < CUT: break
        lo, hi = hi, hi * 2
        if hi > 512: break
    while hi - lo > 1:
        mid = (lo + hi) // 2
        ds = page(mid)
        if ds and min(ds) >= CUT: lo = mid
        else: hi = mid
    ds = page(hi)
    n = hi * per + sum(x >= CUT for x in ds)
    if hi > 512:
        out.update(status="runaway pager", count=None, requests=len(cache)); return out
    out.update(status="ok", per_page=per, boundary_page=hi, count=n, requests=len(cache),
               oldest_seen=str(min(min(v) for v in cache.values() if v)))
    return out


rows = json.load(open(sys.argv[1]))
if len(sys.argv) > 3: rows = [r for r in rows if r["bioguide"] in sys.argv[3].split(",")]
with ThreadPoolExecutor(10) as ex:
    res = list(ex.map(one, rows))
json.dump(res, open(sys.argv[2], "w"), indent=1)
import collections
print(collections.Counter(x["status"] for x in res))
