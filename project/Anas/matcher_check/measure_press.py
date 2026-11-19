"""Martin's matcher on 60 press releases (10 each from 6 members): what does it find, miss or mismatch?
Run from project/:  python measure_press.py <probe2.py> <stage1.json> <out.json>"""
import sys, re, json, html, time, urllib.parse, collections, importlib.util
import pandas as pd
sys.path.insert(0, "Martin")
from matcher import Matcher, key
spec = importlib.util.spec_from_file_location("p2", sys.argv[1]); p2 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ["x", "/dev/null", "/dev/null", "NONE"]
try: spec.loader.exec_module(p2)
except Exception: pass
sys.argv = argv
members = pd.read_csv("data/processed/members.csv"); mt = Matcher(members); B = members.set_index("bioguide")
listing = {r["final"].split("//")[1].split(".")[0]: r.get("listing") for r in json.load(open(argv[2]))}
TAG = re.compile(r"((?:[A-Z][\w.'’\-]+\s){0,3}[A-Z][\w'’\-]+)\s*\(([RDI])[-–‑]([A-Z]{2})(?:[-–‑ ]?\d{1,2})?\)")
SEN = re.compile(r"\b(?:Senators?|Sen\.)\s+((?:[A-Z][\w.'’\-]+\s){0,2}[A-Z][\w'’\-]+)")
full = {}
for r in members.itertuples(): full[f"{r.first.split()[0]} {r.last}"] = r.bioguide
FULL = re.compile(r"\b(" + "|".join(sorted(map(re.escape, full), key=len, reverse=True)) + r")\b")
TITLE_BEFORE = re.compile(r"(Mr\.|Ms\.|Mrs\.|Speaker|Leader|Whip|Representatives?|Rep\.|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member)\s*$")


def body(h):
    k = h.find("<h1"); h = h[k:] if k > 0 else h
    h = re.sub(r"(?is)<(script|style|nav|footer|form|aside)\b.*?</\1>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


out, c = [], collections.Counter()
for s in ["golden", "kaptur", "vasquez", "lawler", "bacon", "fitzpatrick"]:
    L = listing[s]; h = p2.get(L); path = urllib.parse.urlparse(L).path.rstrip("/"); links = []
    for a in re.findall(r'href="([^"#]+)"', h):
        full_u = urllib.parse.urljoin(L, html.unescape(a)); pp = urllib.parse.urlparse(full_u).path
        if (pp.startswith(path + "/") and "page" not in a.lower()) or "documentsingle.aspx" in a.lower() or re.search(r"^/20\d\d/\d{1,2}/[^/]+", pp):
            if full_u not in links: links.append(full_u)
    for l in links[:10]:
        tx = body(p2.get(l)); time.sleep(0.4)
        hits = mt.find(tx)
        tags = TAG.findall(tx); sens = SEN.findall(tx)
        fulls = [(m.group(1), bool(TITLE_BEFORE.search(tx[max(0, m.start() - 25):m.start()]))) for m in FULL.finditer(tx)]
        resolved = {h.named for h in hits if h.named}
        # tags naming a House member whose state disagrees with the tag (a senator or another person)
        tag_state_clash = [(n, p, st) for n, p, st in tags if key(n.split()[-1]) in mt.by_last
                           and all(B.state[b] != st for b in mt.by_last[key(n.split()[-1])])]
        tag_unresolved = [(n, p, st) for n, p, st in tags if key(n.split()[-1]) in mt.by_last
                          and not any(b in resolved for b in mt.by_last[key(n.split()[-1])])
                          and any(B.state[b] == st for b in mt.by_last[key(n.split()[-1])])]
        PL = re.compile(r"\b(?:Reps\.|Representatives|Congressmen|Congresswomen)\s+((?:[A-Z][\w'’\-]+\s?){1,3}(?:,\s*(?:and\s+)?(?:[A-Z][\w'’\-]+\s?){1,3})*(?:,?\s*and\s+(?:[A-Z][\w'’\-]+\s?){1,3}))")
        lists = [m.group(1) for m in PL.finditer(tx)]
        names_in_lists = [w for l in lists for w in re.split(r",\s*(?:and\s+)?|\s+and\s+", l) if w.strip()]
        list_missed = [w.strip() for w in names_in_lists if key(w.strip().split()[-1]) in mt.by_last
                       and not any(b in resolved for b in mt.by_last[key(w.strip().split()[-1])])]
        c["plural-title lists"] += len(lists); c["names in those lists the matcher missed"] += len(list_missed)
        untitled_new = [n for n, t in fulls if not t and full[n] not in resolved]
        c["releases"] += 1; c["matcher hits"] += len(hits); c["resolved"] += sum(h.named is not None for h in hits)
        c["dropped shared"] += sum(h.how == "shared surname, dropped" for h in hits)
        c["dropped capitals"] += sum(h.how.startswith("printed") for h in hits)
        c["tags (Name (P-ST))"] += len(tags); c["tag: state disagrees with every House namesake"] += len(tag_state_clash)
        c["tag: House member the matcher missed"] += len(tag_unresolved)
        c["'Senator X' mentions"] += len(sens)
        c["full name, untitled, not otherwise resolved"] += len(untitled_new)
        out.append(dict(member=s, url=l, hits=[(h.named, h.how) for h in hits], tags=tags, tag_state_clash=tag_state_clash,
                        tag_unresolved=tag_unresolved, list_missed=list_missed, senators=sens, untitled_new=untitled_new))
    print(s, "done", flush=True)
for k, v in c.items(): print(f"{k:50s} {v}")
json.dump(out, open(argv[3], "w"), indent=1)
ex = [(o["member"], x) for o in out for x in o["tag_state_clash"]][:8]; print("state clashes:", ex)
ex = [(o["member"], x) for o in out for x in o["tag_unresolved"]][:8]; print("tags missed:", ex)
print("list missed:", [(o["member"], x) for o in out for x in o["list_missed"]][:12]); ex = [(o["member"], x) for o in out for x in o["untitled_new"]][:10]; print("untitled new:", ex)
