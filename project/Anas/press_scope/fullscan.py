"""Check: walk every listing page of one member and count distinct release links dated >= cutoff."""
import sys, re, html, time, importlib.util, json
spec = importlib.util.spec_from_file_location("p2", sys.argv[1]); p2 = importlib.util.module_from_spec(spec)
sys.argv_saved = sys.argv; sys.argv = ["x", sys.argv[2], "/dev/null", "NONE"]; spec.loader.exec_module(p2); sys.argv = sys.argv_saved
listing = sys.argv[3]
h0 = p2.get(listing); kind, url = p2.pager(listing, h0)
total, n = 0, 0
while True:
    h = h0 if n == 0 else p2.get(url(n)); time.sleep(0.4)
    ds = p2.dates(h)
    k = sum(x >= p2.CUT for x in ds); total += k
    if not ds or min(ds) < p2.CUT: break
    n += 1
print(listing, "pages", n + 1, "dates>=cut", total)
