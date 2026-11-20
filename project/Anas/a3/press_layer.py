"""A3.3: the press layer on top of Martin's shared matcher (rule_set = "shared + press layer").

Run from Anas/ after match_shared.py:
    python a3/press_layer.py --press press_releases --repo <project/ of the group repo> --leg press_scope/leg.json

Martin's matcher is not changed. Its hits (press_hits_shared.parquet, in common.HITS) are taken as they are, and this layer
(a) resolves some of the hits it had to drop and (b) adds names it cannot see. Every changed or added hit says
which rule did it (`layer_rule`), so the shared result can always be shown on its own (decision 3).

Rules, following MATCHER_CHECKLIST.md:
  alias first name   item 9   a dropped shared surname resolved by a first-name alias: the official nickname
                              (legislators-current.json) or the first name the member uses for themselves in their
                              own releases ("Congressman Don Davis": members.csv has Donald)
  party-state tag    item 4   a dropped shared surname resolved by the tag right after it: "Rep. Smith (R-NJ)"
  own surname        -        a dropped shared surname that is the releasing member's own: a self-mention, not lost
  list               item 1   names after a plural title: "Reps. Lawler, Golden, and Fitzpatrick"
  untitled full name item 2   a member's "First Last" with no title: "my colleague Chip Roy"
  state legislator   item 10  guard: a title preceded by "State" or "Assembly" is not a House member
Guards on the two new extractors (list, untitled): not after "Sen.", "Senator", "Gov.", "Governor", "State",
"Assembly", "Mayor", "President", "Secretary", "Judge"; not inside a longer capitalised name ("Jimmy Earl Carter").

Writes out/aliases.csv and press_hits_layer.parquet (in common.HITS: press_raw/a3_out/ on Anas's machine, else out/) (the shared hits, updated, plus the new ones; same columns
as press_hits_shared.parquet plus `layer_rule`).
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, load_inputs, HITS
from prepare import SPLIT

ALIAS_MIN_USES, ALIAS_MIN_SHARE = 5, 0.5
TAG = re.compile(r"\s*\(\s*([RDI])\s*[-–]\s*([A-Z]{2})(?:[-–\s]*\d{1,2}|[-–\s]*AL)?\s*\)")
PLURAL = re.compile(r"\b(Reps\.|Representatives|Congressmen|Congresswomen)\s+")
NAME = r"[A-ZÀ-Þ][A-Za-zÀ-ÿ'’\-]+"
ITEM = re.compile(r"((?:" + NAME + r"\.?\s){0,3}" + NAME + r")")
SEP = re.compile(r"^(?:\s*,\s*|\s+and\s+|\s*,\s*and\s+|\s*&\s*)$")
GUARD_BEFORE = re.compile(r"(?:\bSen\.|\bSenators?|\bGov\.|\bGovernor|\bState|\bAssembly(?:man|woman|member)?|\bMayor|"
                          r"\bPresident|\bSecretary|\bJudge|\bJustice|\bCommissioner|\bCouncil(?:man|woman|member)?)"
                          r"\s+(?:\S+\s+){0,1}$")
# capital "State" only: lowercase "state" is far more often the verb ("Reports further state Rep. Omar", found in the
# 20 Nov precision reading); in all 43 guard hits it was the only lowercase one
STATE_BEFORE_TITLE = re.compile(r"\b(?:State|Assembly)\s*$")


def key(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def build_aliases(members, leg, shared, texts):
    """First names per member: members.csv, the official nickname, and the member's own usage."""
    m = members.set_index("bioguide")
    alias = {b: {(key(f), "members.csv")} for b, f in m["first"].items()}
    for l in leg:
        b = l["id"].get("bioguide")
        if b in alias and l["name"].get("nickname"):
            alias[b].add((key(l["name"]["nickname"]), "official nickname"))
        if b in alias:
            for q in re.findall(r"[\"“]([^\"”]+)[\"”]", l["name"].get("official_full", "")):
                alias[b].add((key(q), "official nickname"))
    # self-naming: words right before the member's own surname in hits on their own releases
    own = pd.concat([shared[shared.speaker == shared.named], shared[shared.status == "unresolved"]])
    seen = defaultdict(Counter)
    lastkey = m["last"].map(key)
    for r in own.itertuples():
        words = texts[r.doc_id][r.start:r.end].split()[1:]          # drop the title
        k = [key(w) for w in words]
        lk = lastkey[r.speaker].split()
        if len(k) > len(lk) and k[-len(lk):] == lk:
            seen[r.speaker][k[-len(lk) - 1]] += 1
    for b, c in seen.items():
        tot = sum(c.values())
        f, n = c.most_common(1)[0]
        if n >= ALIAS_MIN_USES and n / tot >= ALIAS_MIN_SHARE and len(f) > 1 and not f.endswith("."):
            alias[b].add((f, "own releases"))
    return alias


class Resolver:
    def __init__(self, members, alias):
        m = members.set_index("bioguide")
        self.state, self.party = m["state"].to_dict(), m["party"].to_dict()
        self.first = {b: {f for f, _ in a} for b, a in alias.items()}
        self.by_last = defaultdict(list)
        for b, last in m["last"].items():
            self.by_last[key(last)].append(b)

    def resolve(self, words, tag=None, speaker=None):
        """words = the name as written (without title). Returns (bioguide or None, how, n surname words)."""
        k = [key(w.rstrip(".")) for w in words]
        for n in (3, 2, 1):
            if len(k) < n or not self.by_last.get(" ".join(k[-n:])):
                continue
            cands = self.by_last[" ".join(k[-n:])]
            before = k[:-n]
            if len(cands) == 1:
                return cands[0], "unique surname", n
            first = [c for c in cands if self.first[c] & set(before)]
            if len(first) == 1:
                return first[0], "alias first name", n
            if tag:
                t = [c for c in cands if self.party[c] == tag[0] and self.state[c] == tag[1]]
                if len(t) == 1:
                    return t[0], "party-state tag", n
            if speaker in cands and not first:
                return speaker, "own surname", n
            return None, "shared surname, dropped", n
        return None, "no member", 0


def tag_after(text, end):
    m = TAG.match(text, end)
    return (m.group(1), m.group(2)) if m else None


_FOLD = {}


def fold(t):
    """Lower case without accents, keeping every position: one character in, one character out
    ("García’s" -> "garcia s"), so a match in the folded text is a match at the same place in the original."""
    for c in set(t):
        if c not in _FOLD:
            k = key(c)
            _FOLD[c] = k if len(k) == 1 else " "
    return "".join(_FOLD[c] for c in t)


def repeated_spans(text, mine):
    """Spans of the member's repeated sentences, split exactly as prepare.py splits them."""
    out, pos = [], 0
    if not mine:
        return out
    for m in list(SPLIT.finditer(text)) + [None]:
        end = m.start() if m else len(text)
        if text[pos:end].strip() in mine:
            out.append((pos, end))
        pos = m.end() if m else end
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--leg", required=True)
    a = ap.parse_args()
    d, members, Matcher, LEADER_TITLES, bm = load_inputs(a.press, a.repo)
    texts = dict(zip(d.url, d.text))
    meta = d.set_index("url")[["bioguide", "date", "item_type", "listed"]]
    flags = pd.read_parquet(os.path.join(OUT, "release_flags.parquet")).set_index("url")
    S = pd.read_parquet(os.path.join(HITS, "press_hits_shared.parquet"))
    alias = build_aliases(members, json.load(open(a.leg)), S, texts)
    pd.DataFrame([(b, f, src) for b, s in alias.items() for f, src in sorted(s)],
                 columns=["bioguide", "first", "source"]).to_csv(os.path.join(OUT, "aliases.csv"), index=False)
    R = Resolver(members, alias)

    # 1. the shared hits: state-legislator guard, then re-resolve the dropped shared surnames
    L = S.copy()
    L["layer_rule"] = None
    for i, r in L.iterrows():
        t = texts[r.doc_id]
        if STATE_BEFORE_TITLE.search(t[max(0, r.start - 12):r.start]):
            L.at[i, "status"], L.at[i, "layer_rule"] = "state legislator", "state legislator"
            continue
        if r.status != "unresolved" or r.how != "shared surname, dropped":
            continue
        words = t[r.start:r.end].split()[1:] if r.title_word not in ("Ranking Member",) else t[r.start:r.end].split()[2:]
        named, how, _ = R.resolve(words, tag_after(t, r.end), r.speaker)
        if named:
            L.at[i, "named"], L.at[i, "how"], L.at[i, "layer_rule"] = named, how, how
            L.at[i, "status"] = "self" if named == r.speaker else (
                "template" if r.template else "in_boilerplate" if r.in_boilerplate else "counted")

    # 2. new hits: lists after plural titles, and untitled full names
    taken = defaultdict(list)
    for r in L.itertuples():
        taken[r.doc_id].append((r.start, r.end))

    def free(doc, s, e):
        return all(e <= a0 or s >= b0 for a0, b0 in taken[doc])

    full = {}                                                  # "first last" key -> bioguides
    m = members.set_index("bioguide")
    for b, fs in R.first.items():
        for f in fs:
            full.setdefault(f + " " + key(m.at[b, "last"]), set()).add(b)
    pats = sorted({w for k_ in full for w in [k_]}, key=len, reverse=True)
    FULL = re.compile(r"(?<![\w'’])(" + "|".join(re.escape(p).replace(r"\ ", r"\s+") for p in pats) + r")(?![\w'’])")

    rep = pd.read_csv(os.path.join(OUT, "repeated_sentences.csv"))
    repeated = rep.groupby("bioguide").sentence.apply(set).to_dict()
    new = []
    for url, t in texts.items():
        sp = meta.at[url, "bioguide"]
        tpl = bool(flags.at[url, "template"])
        found = []
        for pm in PLURAL.finditer(t):                          # rule: list
            pos = pm.end()
            first_item = True
            while True:
                im = ITEM.match(t, pos)
                if not im:
                    break
                tg = tag_after(t, im.end())
                end = TAG.match(t, im.end()).end() if tg else im.end()
                named, how, n = R.resolve(im.group(1).split(), tg, sp)
                if named:                                       # the first item after "Representatives" is often
                    found.append((im.start(), im.end(), pm.group(1), named,   # Martin's hit already: overlap
                                  "list after plural title", "list"))          # with it is skipped below
                first_item = False
                sm = re.match(r"\s*,\s*and\s+|\s+and\s+|\s*,\s*|\s*&\s*", t[end:])
                if not sm:
                    break
                pos = end + sm.end()
        low = fold(t)
        if True:
            for fm in FULL.finditer(low):                       # rule: untitled full name
                s, e = fm.start(), fm.end()
                bs = full.get(re.sub(r"\s+", " ", fm.group(1)))
                if not bs or len(bs) != 1:
                    continue
                if not t[s:s + 1].isupper():
                    continue
                if GUARD_BEFORE.search(t[max(0, s - 40):s]) or re.search(NAME + r"\s+$", t[max(0, s - 30):s]) \
                        or re.match(r"\s+" + NAME, t[e:]) and not re.match(r"\s+\(", t[e:]):
                    continue
                found.append((s, e, None, next(iter(bs)), "untitled full name", "untitled full name"))
        if not found:
            continue
        bounds = [0] + [mm.end() for mm in bm.SENT_END.finditer(t)]
        spans = repeated_spans(t, repeated.get(sp, set()))
        for s, e, title, named, how, rule in found:
            if not free(url, s, e):
                continue
            taken[url].append((s, e))
            in_rep = any(a0 <= s < b0 for a0, b0 in spans)
            status = "self" if named == sp else "template" if tpl else "in_boilerplate" if in_rep else "counted"
            new.append(dict(speaker=sp, named=named, source="press", date=meta.at[url, "date"], doc_id=url,
                            context=bm.context(t, bounds, s, e), is_yield=False, how=how, title_word=title,
                            is_leader_title=False, rule_set="shared + press layer", start=s, end=e, status=status,
                            template=tpl, in_boilerplate=in_rep, item_type=meta.at[url, "item_type"],
                            listed=meta.at[url, "listed"], layer_rule=rule))
    N = pd.DataFrame(new)
    L.loc[L.layer_rule.notna(), "rule_set"] = "shared + press layer"
    out = pd.concat([L, N], ignore_index=True)
    out.to_parquet(os.path.join(HITS, "press_hits_layer.parquet"), index=False)

    al = pd.read_csv(os.path.join(OUT, "aliases.csv"))
    extra = al[al.source != "members.csv"]
    print(f"aliases beyond members.csv: {len(extra)} ({extra.source.value_counts().to_dict()})")
    print("layer rule (all statuses):", out.layer_rule.value_counts().to_dict())
    print("layer rule x status:\n", out[out.layer_rule.notna()].groupby(["layer_rule", "status"]).size().unstack(fill_value=0))
    sc = S[S.status == "counted"].drop_duplicates(["doc_id", "named"])
    lc = out[out.status == "counted"].drop_duplicates(["doc_id", "named"])
    print(f"counted, once per release: shared {len(sc):,} -> with layer {len(lc):,} (+{len(lc) - len(sc):,}, "
          f"{(len(lc) - len(sc)) / len(sc):+.1%}); releases naming a colleague {sc.doc_id.nunique():,} -> {lc.doc_id.nunique():,}")
    print("still unresolved:", int((out.status == "unresolved").sum()))
