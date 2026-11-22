"""A3.3: the press version of the matcher (rule_set = "shared + press layer"), since the 21 Nov switch.

Run from Anas/ after match_shared.py:
    python a3/press_layer.py --press press_releases --repo <project/ of the group repo>

Since 21 Nov (A3_MATCHER_SWITCH.md) this is Martin's matcher, code unchanged, run with two press settings, plus a
thin layer for what the matcher does not do. The 20 Nov version (own list, untitled and alias rules on the 75c67ae
matcher) is in the repo history; its hits are kept on Anas's machine as press_hits_layer_75c67ae.parquet.

Press settings of Martin's Matcher (input, not code):
  untitled=True        "First Last" without a title (his change G; off for the floor)       layer_rule "untitled full name"
  nicknames=<file>     his nicknames.csv plus aliases.csv: the first names members use for
                       themselves in their own releases ("Don" Davis, "Val" Hoyle)           layer_rule "alias first name"
  (his list rule, on for both sources, is marked here too)                                   layer_rule "list"
Thin layer on top:
  party-state tag      a dropped shared surname settled by the tag after it: "Rep. Smith (R-NJ)"
  own surname          a dropped shared surname that is the releasing member's own: a self-mention, not lost
  state legislator     a title right after "Assembly" (Martin's matcher already skips "State Rep.")
  title guard          an untitled full name right after "Sen.", "Gov.", "Mayor", ...: flagged, not counted
  list across tags     a list after a plural title that carries party-state tags: "Reps. Sessions (R-TX), Meuser
                       (R-PA) and Bacon (R-NE)". Martin's list rule stops at the first tag; this one steps over
                       the tag and resolves each further name with his own Matcher.resolve, the tag settling a
                       shared surname. Names have no periods, so "Malliotakis. Meng" is not one name (the 20 Nov
                       rule's error)
  middle initial       a titled name with a middle initial, "Congressman Riley M. Moore": Martin's matcher stops at
                       the initial and reads the first name as the surname (Josh Riley; MATCHER_CHECKLIST item 15,
                       found by the A3.4 recall check). Resolved here as first name + surname; replaces his hit
  quoted nickname      a nickname in quotes before the surname: Jesús G. “Chuy” García, Henry C. “Hank” Johnson
                       (the quote stops Martin's untitled rule; about 750 mentions, mostly García, Johnson, Scott, Carter)
A hit the plain shared matcher (match_shared.py) also finds, at the same place for the same member, keeps
layer_rule empty and rule_set "shared", so the shared result can always be shown on its own (decision 3).

Writes press_hits_layer.parquet (in common.HITS): same columns as press_hits_shared.parquet plus `layer_rule`.
"""
import argparse
import os
import re
import sys
import time
import unicodedata
from collections import defaultdict

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ALIASES, HITS, OUT, load_inputs, repeated_spans, status_of, write_matcher_aliases
from prepare import SPLIT

TAG = re.compile(r"\s*\(\s*([RDI])\s*[-–]\s*([A-Z]{2})(?:[-–\s]*\d{1,2}|[-–\s]*AL)?\s*\)")
GUARD_BEFORE = re.compile(r"(?:\bSen\.|\bSenators?|\bGov\.|\bGovernor|\bState|\bAssembly(?:man|woman|member)?|\bMayor|"
                          r"\bPresident|\bSecretary|\bJudge|\bJustice|\bCommissioner|\bCouncil(?:man|woman|member)?)"
                          r"\s+(?:\S+\s+){0,1}$")
ASSEMBLY_BEFORE_TITLE = re.compile(r"\bAssembly\s*$")
PLURAL_TITLE = re.compile(r"\b(Reps\.|Representatives|Congressmen|Congresswomen)\s+")
LIST_WORD = r"[A-ZÀ-Þ][A-Za-zÀ-ÿ'’\-]+"
LIST_ITEM = re.compile(r"((?:" + LIST_WORD + r"\s|[A-Z]\.\s){0,3}" + LIST_WORD + r")")
LIST_SEP = re.compile(r"\s*,\s*and\s+|\s+and\s+|\s*,\s*|\s*&\s*")
QUOTED = re.compile(r"[“\"]([A-ZÀ-Þ][A-Za-zÀ-ÿ\.]*)[”\"]\s+((?:" + LIST_WORD + r"\s){0,2}" + LIST_WORD + r")")


def quoted_nicknames(members, alias_file):
    """(nickname key, surname key) -> bioguide, where exactly one member has that pair: Jesús G. “Chuy” García."""
    m = members.set_index("bioguide")
    al = pd.read_csv(alias_file)
    pairs = defaultdict(set)
    for b, nick in zip(al.bioguide, al.nickname):
        if b in m.index:
            pairs[(key(str(nick)), key(m.at[b, "last"]))].add(b)
    return {k: v.pop() for k, v in pairs.items() if len(v) == 1}


def quoted_hits(text, qn):
    out = []
    for qm in QUOTED.finditer(text):
        nick, words = key(qm.group(1)), qm.group(2).split()
        for n in (3, 2, 1):
            if len(words) >= n and (b := qn.get((nick, key(" ".join(words[:n]))))):
                out.append((qm.start(), qm.start(2) + len(" ".join(words[:n])), "", b, "quoted nickname"))
                break
    return out


def middle_initial_rx(M):
    """Title, first name(s), one capital initial, surname: "Congressman Riley M. Moore". Built from Martin's own TITLE
    and WORD (module M = his matcher), so only the initial is new."""
    name = r"(?:" + M.WORD + r"\s){0,2}" + M.WORD
    return re.compile(r"\b" + M.TITLE + r"\s+(" + name + r")\s[A-Z]\.\s+(" + name + r")")


def middle_initial_hits(text, mt, rx):
    """(start, end, title, named, how) for titled names with a middle initial. Martin's NAME stops at the initial, so
    "Riley M. Moore" is read as "Riley" (Josh Riley) and "Alma S. Adams" as "Alma" (no one): MATCHER_CHECKLIST item 15.
    The first name(s) and the surname are resolved together with his Matcher.resolve; trailing capitalised words
    ("Moore Announces") are dropped from the end until a member is found."""
    out, nobody = [], set()
    for mm in rx.finditer(text):
        first, last = mm.group(2).split(), mm.group(3).split()
        for k in range(len(last), 0, -1):
            r = mt.resolve(mm.group(1), first + last[:k], text, mm.start(), mm.end())
            if r:
                end = mm.start(3) + len(" ".join(last[:k]))
                out.append((mm.start(), end, mm.group(1), r[0], "middle initial: " + r[1]))
                break
        else:                                   # "Mr. James R. Willis": no member, so the hit on "James" is wrong too
            nobody.add(mm.start())
    return out, nobody


def tagged_list(text, mt, resolver, speaker):
    """(start, end, title, named, how) for names in plural-title lists that carry party-state tags."""
    out = []
    for pm in PLURAL_TITLE.finditer(text):
        pos, tagged = pm.end(), False
        while (im := LIST_ITEM.match(text, pos)):
            tg = TAG.match(text, im.end())
            tagged = tagged or bool(tg)
            r = mt.resolve(pm.group(1), im.group(1).split(), text, im.start(1), im.end(1))
            if r and r[0] is None and r[1] == "shared surname, dropped" and tg:
                rn, rh = resolver.resolve(im.group(1).split(), (tg.group(1), tg.group(2)), None)
                r = (rn, "list: " + rh) if rn else r
            elif r:
                r = (r[0], "list: " + r[1])
            if r and tagged:
                out.append((im.start(1), im.end(1), pm.group(1), *r))
            end = tg.end() if tg else im.end()
            sm = LIST_SEP.match(text, end)
            if not sm:
                break
            pos = sm.end()
    return out


def key(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


class Resolver:
    """Settles a surname the matcher dropped as shared, by party-state tag or as the releasing member's own."""
    def __init__(self, members):
        m = members.set_index("bioguide")
        self.state, self.party = m["state"].to_dict(), m["party"].to_dict()
        self.by_last = defaultdict(list)
        for b, last in m["last"].items():
            self.by_last[key(last)].append(b)

    def resolve(self, words, tag, speaker):
        k = [key(w.rstrip(".")) for w in words]
        for n in (3, 2, 1):
            cands = self.by_last.get(" ".join(k[-n:])) if len(k) >= n else None
            if not cands:
                continue
            if tag:
                t = [c for c in cands if self.party[c] == tag[0] and self.state[c] == tag[1]]
                if len(t) == 1:
                    return t[0], "party-state tag"
            if speaker in cands:
                return speaker, "own surname"
            return None, None
        return None, None


def tag_after(text, end):
    m = TAG.match(text, end)
    return (m.group(1), m.group(2)) if m else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    t0 = time.time()
    d, members, Matcher, LEADER_TITLES, bm = load_inputs(a.press, a.repo)
    flags = pd.read_parquet(os.path.join(OUT, "release_flags.parquet")).set_index("url")
    rep = pd.read_csv(os.path.join(OUT, "repeated_sentences.csv"))
    repeated = rep.groupby("bioguide").sentence.apply(set).to_dict()
    S = pd.read_parquet(os.path.join(HITS, "press_hits_shared.parquet"))
    shared_keys = set(zip(S.doc_id, S.start, S.named.fillna("")))
    alias_file = write_matcher_aliases(a.repo)
    mt = Matcher(members, nicknames=alias_file)
    R = Resolver(members)
    QN = quoted_nicknames(members, alias_file)
    import matcher as M                          # Martin's module, on the path after load_inputs
    MI, MI_QUICK = middle_initial_rx(M), re.compile(r"\s[A-Z]\.\s")

    rows, n_mi_dropped = [], 0
    for r in d.itertuples():
        t = r.text
        hits = [(h.start, h.end, h.title, h.named, h.how, None) for h in mt.find(t, untitled=True)]
        mi, nobody = middle_initial_hits(t, mt, MI) if MI_QUICK.search(t) else ([], set())
        if mi or nobody:                         # replaces Martin's hit at the same title, which read the first name
            starts = {s for s, *_ in mi} | nobody
            dropped = [h for h in hits if h[0] in nobody and h[3]]
            hits = [h for h in hits if h[0] not in starts]
            n_mi_dropped += len(dropped)
            taken = [(h[0], h[1]) for h in hits]
            hits += [(s, e, ti, nm, hw, "middle initial") for s, e, ti, nm, hw in mi
                     if all(e <= a0 or s >= b0 for a0, b0 in taken)]
        if PLURAL_TITLE.search(t) and TAG.search(t):
            taken = [(h[0], h[1]) for h in hits]
            hits += [(s, e, ti, nm, hw, "list across tags") for s, e, ti, nm, hw in tagged_list(t, mt, R, r.bioguide)
                     if all(e <= a0 or s >= b0 for a0, b0 in taken)]
        if "”" in t or '"' in t:
            taken = [(h[0], h[1]) for h in hits]
            hits += [(s, e, ti, nm, hw, "quoted nickname") for s, e, ti, nm, hw in quoted_hits(t, QN)
                     if all(e <= a0 or s >= b0 for a0, b0 in taken)]
        if not hits:
            continue
        bounds = [0] + [m.end() for m in bm.SENT_END.finditer(t)]
        spans = repeated_spans(t, repeated.get(r.bioguide, set()), SPLIT)
        mine = repeated.get(r.bioguide, set())
        tpl = bool(flags.at[r.url, "template"])
        for start, end, title, named, how, rule in hits:
            status = None
            in_rep = any(s <= start < e and txt in mine for s, e, txt in spans)
            if title and ASSEMBLY_BEFORE_TITLE.search(t[max(0, start - 12):start]):
                rule, status = "state legislator", "state legislator"
            elif how == "full name, no title" and GUARD_BEFORE.search(t[max(0, start - 40):start]):
                rule, status = "title guard", "title guard"
            elif how.endswith("shared surname, dropped"):
                words = t[start:end].split()
                words = words[2:] if title == "Ranking Member" else words if how.startswith("list: ") else words[1:]
                rn, rh = R.resolve(words, tag_after(t, end), r.bioguide)
                if rn:
                    named, how, rule = rn, rh, rule or rh
            if rule is None and (r.url, start, named or "") not in shared_keys:
                rule = ("untitled full name" if how == "full name, no title" else
                        "list" if how.startswith("list: ") else "alias first name")
            if status is None:
                status = status_of(named, r.bioguide, tpl, in_rep)
            rows.append(dict(speaker=r.bioguide, named=named, source="press", date=r.date, doc_id=r.url,
                             context=bm.context(t, bounds, start, end), is_yield=False, how=how,
                             title_word=title, is_leader_title=title in LEADER_TITLES,
                             rule_set="shared" if rule is None else "shared + press layer", start=start,
                             end=end, status=status, template=tpl, in_boilerplate=in_rep, item_type=r.item_type,
                             listed=r.listed, layer_rule=rule))
    out = pd.DataFrame(rows)
    out.to_parquet(os.path.join(HITS, "press_hits_layer.parquet"), index=False)

    print(f"hits {len(out):,} ({time.time() - t0:.0f} s); aliases file {os.path.basename(ALIASES)} -> "
          f"{sum(1 for _ in open(os.path.join(OUT, 'matcher_aliases.csv'))) - 1} extra first names")
    print("layer rule x status:\n", out[out.layer_rule.notna()].groupby(["layer_rule", "status"]).size().unstack(fill_value=0))
    sc = S[S.status == "counted"].drop_duplicates(["doc_id", "named"])
    lc = out[out.status == "counted"].drop_duplicates(["doc_id", "named"])
    party = members.set_index("bioguide").party

    def xp(o):
        sp, nm = party.reindex(o.speaker).values, party.reindex(o.named).values
        ok = pd.Series(sp).isin(["R", "D"]).values & pd.Series(nm).isin(["R", "D"]).values
        return (sp[ok] != nm[ok]).mean()
    print(f"counted, once per release: shared {len(sc):,} ({xp(sc):.1%} cross-party) -> with layer {len(lc):,} "
          f"({xp(lc):.1%}); releases naming a colleague {sc.doc_id.nunique():,} -> {lc.doc_id.nunique():,}")
    print("still unresolved:", int((out.status == "unresolved").sum()))
    print("middle initial: hits of Martin's matcher dropped because the full name is no member:", n_mi_dropped)
