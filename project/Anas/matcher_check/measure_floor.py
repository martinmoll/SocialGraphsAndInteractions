"""How often would each proposed matcher change matter on the floor speeches? Run from project/:  python Anas/matcher_check/measure_floor.py Anas/press_scope/leg.json
Uses Martin's Matcher unchanged and the turn filter of build_mentions.py (section H, >= 50 words, member speaker)."""
import re, sys, json, collections, unicodedata
import pandas as pd
sys.path.insert(0, "Martin")
from matcher import Matcher, key, RX

members = pd.read_csv("data/processed/members.csv")
sp = pd.read_parquet("data/processed/speeches.parquet")
turns = sp[(sp.section == "H") & (sp.n_words >= 50) & sp.bioguide.isin(members.bioguide)]
mt = Matcher(members)
how = collections.Counter(); inherit_turn = inherit_doc = 0; shared_dropped = 0
resolved_by_doc = collections.defaultdict(dict)   # doc -> surname key -> set of bioguides resolved earlier
for t in turns.sort_values(["item"]).itertuples():
    seen_turn = {}
    for h in mt.find(t.text):
        how[h.how] += 1
        words = t.text[h.start:h.end].split()[1:]
        k = key(words[-1]) if words else ""
        if h.named:
            seen_turn.setdefault(k, set()).add(h.named); resolved_by_doc[t.item].setdefault(k, set()).add(h.named)
        elif h.how == "shared surname, dropped":
            shared_dropped += 1
            if len(seen_turn.get(k, ())) == 1: inherit_turn += 1
            elif len(resolved_by_doc[t.item].get(k, ())) == 1: inherit_doc += 1
print("matcher rules on floor turns:", dict(how))
print(f"shared surname dropped: {shared_dropped}; resolvable by an earlier unique resolution in the same turn: {inherit_turn}; "
      f"only in the same debate (doc): {inherit_doc}")

# untitled full names: 'First Last' of a member, with no matcher title in the 25 characters before
TITLES = re.compile(r"(Mr\.|Ms\.|Mrs\.|Speaker|Leader|Whip|Representatives?|Rep\.|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member)\s*$")
full = {}
for r in members.itertuples():
    full[(r.first.split()[0], r.last)] = r.bioguide
pat = re.compile(r"\b(" + "|".join(sorted({re.escape(f"{f} {l}") for f, l in full}, key=len, reverse=True)) + r")\b")
untitled = titled = 0; ex = []
for t in turns.itertuples():
    for m in pat.finditer(t.text):
        if TITLES.search(t.text[max(0, m.start() - 25):m.start()]): titled += 1
        else:
            untitled += 1
            if len(ex) < 6 and m.start() > 40: ex.append(t.text[m.start() - 40:m.end() + 20].replace("\n", " "))
print(f"full-name mentions 'First Last': titled {titled}, untitled {untitled}")
for e in ex: print("   …", e)

# senators who share a surname with a House member
leg = json.load(open(sys.argv[1]))
sen = {(l["name"]["last"], l["terms"][-1]["state"]) for l in leg if l["terms"][-1]["type"] == "sen"}
house_last = set(members["last"].map(key))
clash = sorted(f"{l} ({s})" for l, s in sen if key(l) in house_last)
print(f"senators sharing a surname with a House member: {len(clash)}:", ", ".join(clash))
n_sen_title = sum(len(re.findall(r"\b(?:Senator|Sen\.)\s+[A-Z]", x)) for x in turns.text)
print("'Senator X' / 'Sen. X' in House floor turns:", n_sen_title)

# hyphenated and multi-word surnames: does the matcher find them?
for nm in ["Miller-Meeks", "Ocasio-Cortez", "Gluesenkamp Perez", "Van Duyne", "Scott Franklin"]:
    hits = mt.find(f"I thank Rep. {nm} for her work.")
    print(f"  'Rep. {nm}':", [(members.set_index('bioguide').name.get(h.named), h.how) for h in hits])
print("shared surnames in members.csv:", int((members['last'].map(key).value_counts() > 1).sum()))
