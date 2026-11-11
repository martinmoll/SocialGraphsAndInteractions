"""The silence matrix: which fields write about the same things but do not cite each other?
Usage: python src/silence.py FIELD        (e.g. energy_transition; reads the newest raw file for FIELD)

Groups are OpenAlex fields (5) and subfields with >= MIN_GROUP papers. For each pair of groups:
  flow  R = observed citation edges between the groups / edges expected from the groups' degrees alone
  text  S = cosine between the groups' mean TF-IDF vectors (title + abstract)
Silence = how far below the R-vs-S trend a pair sits. Outputs go to data/processed/FIELD/silence.json.
"""
import collections
import glob
import itertools
import json
import pathlib
import sys

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIELD = sys.argv[1]
OUT = ROOT / "data" / "processed" / FIELD
OUT.mkdir(parents=True, exist_ok=True)
MIN_GROUP = 30        # CHOICE: a subfield needs >= 30 papers before its centroid and flows mean anything
N_BOOT = 200          # bootstrap resamples of papers, for intervals on R and S
SPLIT = 2019          # temporal check: flows from papers <= SPLIT vs > SPLIT
MIN_EXPECTED = 20     # CHOICE: rank a pair only if >= 20 edges are expected; below that, 0 observed edges is chance
STOP = list(ENGLISH_STOP_WORDS | {"energy", "transition", "transitions"} | {
    "paper", "study", "results", "based", "using", "proposed", "used", "analysis", "model", "method", "approach",
    "different", "new", "elsevier", "rights", "reserved", "ltd", "abstract", "research", "present", "presented",
    "article", "work", "review", "overview", "survey", "comprehensive"})  # same list as pipeline.py


def abstract_of(w):
    inv = w.get("abstract_inverted_index") or {}
    return " ".join(word for _, word in sorted((p, word) for word, ps in inv.items() for p in ps))


def flows(edges, grp, groups):
    """Observed undirected edges between groups, and the configuration-model expectation K_a K_b / 2m."""
    O = collections.Counter()
    K = collections.Counter()
    for a, b in edges:
        ga, gb = grp.get(a), grp.get(b)
        if ga is None or gb is None:
            continue
        K[ga] += 1
        K[gb] += 1
        if ga != gb:
            O[frozenset((ga, gb))] += 1
    m2 = sum(K.values())
    return {(a, b): (O[frozenset((a, b))], K[a] * K[b] / m2 if m2 else 0) for a, b in itertools.combinations(groups, 2)}


def analyse(level, W, nodes, edges, X, vocab, year):
    key = (lambda w: ((w.get("primary_topic") or {}).get(level) or {}).get("display_name"))
    parent = {}
    for x in nodes:
        pt = W[x].get("primary_topic") or {}
        parent[(pt.get("subfield") or {}).get("display_name")] = (pt.get("field") or {}).get("display_name")
    cnt = collections.Counter(key(W[x]) for x in nodes)
    groups = sorted(g for g, c in cnt.items() if g and c >= MIN_GROUP)
    grp = {x: key(W[x]) for x in nodes if key(W[x]) in groups}
    row = {x: i for i, x in enumerate(nodes)}
    members = {g: np.array([row[x] for x in nodes if grp.get(x) == g]) for g in groups}

    def centroids(mem):
        C = {g: np.asarray(X[idx].mean(0)).ravel() for g, idx in mem.items()}
        return {g: c / (np.linalg.norm(c) or 1) for g, c in C.items()}

    def stats(mem_nodes, mem):
        F = flows(edges, mem_nodes, groups)
        C = centroids(mem)
        return {p: (o, e, o / e if e else np.nan, float(C[p[0]] @ C[p[1]])) for p, (o, e) in F.items()}

    base = stats(grp, members)
    # bootstrap: resample papers within each group (a resampled paper keeps its own edges)
    rng = np.random.default_rng(0)
    boot = collections.defaultdict(list)
    for _ in range(N_BOOT):
        mem = {g: rng.choice(idx, len(idx)) for g, idx in members.items()}
        keep = {nodes[i] for idx in mem.values() for i in idx}
        bs = stats({x: g for x, g in grp.items() if x in keep}, mem)
        for p, v in bs.items():
            boot[p].append(v[2:])

    pairs = [p for p in base if base[p][1] >= MIN_EXPECTED]
    logR = np.array([np.log(base[p][2] + 0.01) for p in pairs])
    S = np.array([base[p][3] for p in pairs])
    slope, icept = np.polyfit(S, logR, 1)
    resid = logR - (slope * S + icept)
    r = float(np.corrcoef(S, logR)[0, 1])
    # permutation test for the S-vs-flow relation
    perm = [abs(np.corrcoef(rng.permutation(S), logR)[0, 1]) for _ in range(2000)]

    # temporal: does text similarity predict flow AFTER SPLIT, given flow up to SPLIT? (regression to the mean control)
    pre = flows([(a, b) for a, b in edges if year[a] <= SPLIT], grp, groups)
    post = flows([(a, b) for a, b in edges if year[a] > SPLIT], grp, groups)
    lpre = np.array([np.log(pre[p][0] / pre[p][1] + 0.01) if pre[p][1] else np.nan for p in pairs])
    lpost = np.array([np.log(post[p][0] / post[p][1] + 0.01) if post[p][1] else np.nan for p in pairs])
    ok = ~np.isnan(lpre) & ~np.isnan(lpost)
    A = np.column_stack([np.ones(ok.sum()), lpre[ok], S[ok]])
    beta = np.linalg.lstsq(A, lpost[ok], rcond=None)[0]
    perm_b = []
    for _ in range(2000):
        A2 = A.copy()
        A2[:, 2] = rng.permutation(A2[:, 2])
        perm_b.append(np.linalg.lstsq(A2, lpost[ok], rcond=None)[0][2])

    out = []
    for k, p in enumerate(pairs):
        b = np.array(boot[p], float)
        C = centroids(members)
        shared = vocab[np.argsort(-(C[p[0]] * C[p[1]]))[:8]].tolist()   # words that drive the text similarity
        out.append({"a": p[0], "b": p[1], "cross_field": parent.get(p[0], p[0]) != parent.get(p[1], p[1]),
                    "observed": base[p][0], "expected": round(base[p][1], 1), "R": round(base[p][2], 3),
                    "R_ci": [round(float(np.nanquantile(b[:, 0], q)), 3) for q in (.025, .975)],
                    "S": round(base[p][3], 3), "S_ci": [round(float(np.quantile(b[:, 1], q)), 3) for q in (.025, .975)],
                    "silence": round(float(-resid[k]), 3), "shared_words": shared,
                    "R_pre": round(float(np.exp(lpre[k]) - .01), 3) if not np.isnan(lpre[k]) else None,
                    "R_post": round(float(np.exp(lpost[k]) - .01), 3) if not np.isnan(lpost[k]) else None})
    out.sort(key=lambda d: -d["silence"])
    return {"groups": {g: int(cnt[g]) for g in groups}, "n_pairs": len(pairs), "n_pairs_too_small": len(base) - len(pairs),
            "corr_S_logR": r, "corr_perm_p": float((np.sum(np.array(perm) >= abs(r)) + 1) / 2001),
            "fit_logR_on_S": [float(slope), float(icept)],
            "temporal": {"pairs_used": int(ok.sum()), "beta_const_pre_S": [float(x) for x in beta],
                         "S_coef_perm_p": float((np.sum(np.abs(perm_b) >= abs(beta[2])) + 1) / 2001)},
            "pairs": out}


def main():
    raw = json.load(open(sorted(glob.glob(str(ROOT / f"data/raw/openalex_{FIELD}_*.json")))[-1], encoding="utf-8"))
    W = {w["id"].rsplit("/", 1)[-1]: w for w in raw["works"]}
    year = {i: w["publication_year"] for i, w in W.items()}
    G = nx.DiGraph()
    G.add_nodes_from(W)
    G.add_edges_from((i, r.rsplit("/", 1)[-1]) for i, w in W.items() for r in w["referenced_works"]
                     if r.rsplit("/", 1)[-1] in W and r.rsplit("/", 1)[-1] != i)
    lcc = max(nx.weakly_connected_components(G), key=len)   # CHOICE: largest weakly connected component, as in pipeline.py
    nodes = sorted(lcc)
    edges = [(a, b) for a, b in G.edges if a in lcc]
    docs = [(W[x]["title"] or "") + ". " + abstract_of(W[x]) for x in nodes]
    tf = TfidfVectorizer(stop_words=STOP, min_df=5, max_df=0.5, sublinear_tf=True, token_pattern=r"[a-zA-Z][a-zA-Z\-]{2,}")
    X = tf.fit_transform(docs)
    vocab = np.array(tf.get_feature_names_out())
    has_abs = [bool(W[x].get("abstract_inverted_index")) for x in nodes]
    res = {"field": FIELD, "collected": raw["date"], "lcc_nodes": len(nodes), "lcc_edges": len(edges),
           "lcc_with_abstract": int(sum(has_abs)), "min_group": MIN_GROUP, "split_year": SPLIT,
           "field_level": analyse("field", W, nodes, edges, X, vocab, year),
           "subfield_level": analyse("subfield", W, nodes, edges, X, vocab, year)}
    # robustness: abstracts only (title-only papers have very sparse text vectors)
    ab_nodes = [x for x, h in zip(nodes, has_abs) if h]
    Xa = TfidfVectorizer(stop_words=STOP, min_df=5, max_df=0.5, sublinear_tf=True,
                         token_pattern=r"[a-zA-Z][a-zA-Z\-]{2,}").fit(
        [(W[x]["title"] or "") + ". " + abstract_of(W[x]) for x in ab_nodes])
    Xab = Xa.transform([(W[x]["title"] or "") + ". " + abstract_of(W[x]) for x in ab_nodes])
    res["subfield_level_abstracts_only"] = analyse("subfield", W, ab_nodes, [(a, b) for a, b in edges if a in set(ab_nodes) and b in set(ab_nodes)],
                                                   Xab, np.array(Xa.get_feature_names_out()), year)
    (OUT / "silence.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    for lvl in ("field_level", "subfield_level", "subfield_level_abstracts_only"):
        L = res[lvl]
        print(f"\n=== {lvl}: {len(L['groups'])} groups, {L['n_pairs']} pairs | corr(S, log R) = {L['corr_S_logR']:+.2f} "
              f"(perm p {L['corr_perm_p']:.3f}) | temporal beta(S) = {L['temporal']['beta_const_pre_S'][2]:+.2f} "
              f"(perm p {L['temporal']['S_coef_perm_p']:.3f}, {L['temporal']['pairs_used']} pairs)")
        show = L["pairs"] if lvl == "field_level" else L["pairs"][:8] + [{"a": "...", "b": ""}] + L["pairs"][-4:]
        for p in show:
            if p["a"] == "...":
                print("   ...")
                continue
            print(f"  silence {p['silence']:+.2f} | R {p['R']:.2f} {p['R_ci']} obs {p['observed']:4d} exp {p['expected']:6.1f} | "
                  f"S {p['S']:.2f} {p['S_ci']} | pre {p['R_pre']} post {p['R_post']} | {'X ' if p['cross_field'] else '  '}"
                  f"{p['a'][:32]} <-> {p['b'][:32]} | {' '.join(p['shared_words'][:5])}")


if __name__ == "__main__":
    main()
