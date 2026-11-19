"""Independent check of a count: list release links in listing order on pages around the boundary, open item
number `count` (last counted) and `count+1` (first not counted), and read each date from the release page itself."""
import sys, re, html, urllib.parse, importlib.util
spec = importlib.util.spec_from_file_location("p2", sys.argv[1]); p2 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ["x", "/dev/null", "/dev/null", "NONE"]
try: spec.loader.exec_module(p2)
except Exception: pass
listing, count = argv[2], int(argv[3])
h0 = p2.get(listing); kind, url = p2.pager(listing, h0)
path = urllib.parse.urlparse(listing).path.rstrip("/")


def links(h):
    out = []
    for a in re.findall(r'href="([^"#]+)"', p2.main_part(h)):
        full = urllib.parse.urljoin(listing, html.unescape(a)); pp = urllib.parse.urlparse(full).path
        ok = (pp.startswith(path + "/") and not re.search(r"/page/\d+/?$", pp) and "page" not in urllib.parse.urlparse(full).query.lower()) \
            or "documentsingle.aspx" in full.lower() or re.search(r"/20\d\d/\d{1,2}/[^/]+", pp)
        if ok and full not in out: out.append(full)
    return out


per = len(links(h0))
pg = (count - 1) // per
L = links(p2.get(url(pg)) if pg else h0) + links(p2.get(url(pg + 1)))
i = (count - 1) - pg * per
for j, tag in ((i, "last counted"), (i + 1, "first not counted")):
    ds = p2.dates(p2.get(L[j]))
    print(f"{tag:18s} item {pg * per + j + 1}: {min(ds) if ds else None}  {L[j][-70:]}")
print("links per listing page:", per, "| cutoff", p2.CUT)
