"""For members with no listing link or no usable pager: try common listing paths, keep the first with >=5 dates."""
import json, sys, time, importlib.util
spec = importlib.util.spec_from_file_location("p2", sys.argv[1]); p2 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ["x", argv[2], "/dev/null", "NONE"]; spec.loader.exec_module(p2); sys.argv = argv
PATHS = ["/media/press-releases", "/press-releases", "/news/press-releases", "/media-center/press-releases",
         "/newsroom/press-releases", "/category/press-releases/", "/press", "/news/documentquery.aspx?DocumentTypeID=27",
         "/statements-and-releases/", "/news/", "/news"]
rows = json.load(open(argv[2])); ids = set(argv[4].split(","))
out = []
for r in rows:
    if r["bioguide"] not in ids: continue
    base = r["final"].rstrip("/")
    best = None
    for p in PATHS:
        h = p2.get(base + p); time.sleep(0.3)
        ds = p2.dates(h)
        if len(ds) >= 5 and p2.pager(base + p, h)[1]:
            best = base + p; break
        if len(ds) >= 5 and not best: best = base + p
    r = dict(r); r["listing"] = best; r["guessed"] = True
    out.append(r); print(r["final"], best, flush=True)
json.dump(out, open(argv[3], "w"), indent=1)
