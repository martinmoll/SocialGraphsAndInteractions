"""Pilot, 18 Nov 2026: 20 recent releases each from 8 Democrats and 8 Republicans (4 exposed, 4 safe per party).
A colleague counts only if the surname is a unique House surname in members.csv; an (R-ST)/(D-ST) tag counts only
when its party agrees with the roster (drops senators). Self-mentions removed by the member's own roster surname."""
import sys, re, json, html, time, urllib.parse, pandas as pd, importlib.util
spec = importlib.util.spec_from_file_location("p2", sys.argv[1]); p2 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ["x", "/dev/null", "/dev/null", "NONE"]
try: spec.loader.exec_module(p2)
except Exception: pass
sys.argv = argv
P = argv[2]
m = pd.read_csv(f"{P}/members.csv"); m = m[m.party.isin(["R", "D"])]
cnt = m["last"].value_counts(); u = m[m["last"].map(cnt) == 1]; byname = dict(zip(u["last"], u.party))
NAME = re.compile(r"\b(?:Rep\.|Reps\.|Representatives?|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member|Whip|Leader|Speaker)\s+((?:[A-Z][\w.'’\-]+\s){0,3}[A-Z][\w'’\-]+)")
TAG = re.compile(r"([A-Z][\w'’\-]+)\s*\(([RDI])[-–‑][A-Z][A-Za-z.]{1,5}(?:[-–‑ ]?\d{1,2})?\)")
LEAD = {"Johnson", "Scalise", "Emmer", "Jeffries", "Clark", "Aguilar"}  # party leaders: named by role, not partnership
sites = {"golden": ("D", "exposed", "Golden"), "kaptur": ("D", "exposed", "Kaptur"), "dondavis": ("D", "exposed", "Davis"),
         "vasquez": ("D", "exposed", "Vasquez"), "pelosi": ("D", "safe", "Pelosi"), "cohen": ("D", "safe", "Cohen"),
         "schakowsky": ("D", "safe", "Schakowsky"), "ocasio-cortez": ("D", "safe", "Ocasio-Cortez"),
         "lawler": ("R", "exposed", "Lawler"), "bacon": ("R", "exposed", "Bacon"), "fitzpatrick": ("R", "exposed", "Fitzpatrick"),
         "ciscomani": ("R", "exposed", "Ciscomani"), "roy": ("R", "safe", "Roy"), "hageman": ("R", "safe", "Hageman"),
         "biggs": ("R", "safe", "Biggs"), "arrington": ("R", "safe", "Arrington")}
listing = {r["final"].split("//")[1].split(".")[0]: r.get("listing") for r in json.load(open(argv[3]))}


def body(h):
    k = h.find("<h1"); h = h[k:] if k > 0 else h
    h = re.sub(r"(?is)<(script|style|nav|footer|form|aside)\b.*?</\1>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


rows = []
for s, (party, kind, self_last) in sites.items():
    L = listing.get(s)
    if not L: print(s, "no listing"); continue
    links = []
    for p in range(3):
        h = p2.get(L if p == 0 else p2.pager(L, p2.get(L))[1](p)); time.sleep(0.4)
        path = urllib.parse.urlparse(L).path.rstrip("/")
        for a in re.findall(r'href="([^"#]+)"', h):
            a = html.unescape(a); full = urllib.parse.urljoin(L, a)
            if (path and urllib.parse.urlparse(full).path.startswith(path + "/") and "page" not in a.lower()) or "documentsingle.aspx" in a.lower() or re.search(r"^/20\d\d/\d{1,2}/[^/]+", urllib.parse.urlparse(full).path):
                if full not in links: links.append(full)
        if len(links) >= 20: break
    for l in links[:20]:
        tx = body(p2.get(l)); time.sleep(0.4)
        if len(tx.split()) < 60: continue
        named = {}
        for nm in NAME.findall(tx):
            for tok in reversed(nm.split()):
                tok = re.sub(r"[’']s$", "", tok)
                if tok in byname: named[tok] = byname[tok]; break
        for a, b in TAG.findall(tx):
            if byname.get(a) == b: named[a] = b
        named.pop(self_last, None)
        nonlead = {k: v for k, v in named.items() if k not in LEAD}
        other = "D" if party == "R" else "R"
        rows.append(dict(member=s, party=party, kind=kind, url=l, n_other=sum(v == other for v in nonlead.values()),
                         n_own=sum(v == party for v in nonlead.values()), other=[k for k, v in nonlead.items() if v == other],
                         bip=bool(re.search("bipartisan", tx, re.I))))
    print(s, len(links), "links", flush=True)
df = pd.DataFrame(rows)
g = df.groupby(["party", "kind", "member"]).agg(releases=("url", "size"), names_other_party=("n_other", lambda x: (x > 0).mean()),
        names_own_party=("n_own", lambda x: (x > 0).mean()), says_bipartisan=("bip", "mean"))
pd.set_option("display.width", 200); print(g.round(2))
print(df.groupby(["party", "kind"]).agg(releases=("url", "size"), names_other_party=("n_other", lambda x: (x > 0).mean())).round(2))
for s in sites: print(s, sorted({r for x in df[df.member == s].other for r in x}))
df.to_json("names_both.json", orient="records", indent=1)
