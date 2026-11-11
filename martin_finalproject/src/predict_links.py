"""Idea 1 signal test: do 'missing links' found in 2019 get co-cited later?
Usage: python src/predict_links.py FIELD [SPLIT_YEAR]

Reads the data embedded in explorer_FIELD.html (largest component only; raw files are not needed).
Everything used to *predict* comes from papers <= SPLIT_YEAR and citations among them.
The *outcome* is co-citation: a paper > SPLIT_YEAR in the sample cites both papers of a pair.
"""
import collections
import json
import pathlib
import sys

import networkx as nx
import numpy as np
from networkx.algorithms.community import louvain_communities
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import roc_auc_score

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIELD = sys.argv[1]
SPLIT = int(sys.argv[2]) if len(sys.argv) > 2 else 2019
MIN_DIST = 3          # CHOICE: same "far" rule as the missing-link list in pipeline.py
N_POP_BINS = 10       # popularity strata for the matched comparison
TOP_K = [50, 100, 500]
FIELD_STOP = {"energy_systems": {"energy", "system", "systems"}, "ocean_science": {"ocean", "oceans", "oceanic"}}
STOP = list(ENGLISH_STOP_WORDS | FIELD_STOP.get(FIELD, set()) | {
    "paper", "study", "results", "based", "using", "proposed", "used", "analysis", "model", "method", "approach",
    "different", "new", "elsevier", "rights", "reserved", "ltd", "abstract", "research", "present", "presented",
    "article", "work", "review", "overview", "survey", "comprehensive"})  # same list as pipeline.py


def load():
    h = (ROOT / f"explorer_{FIELD}.html").read_text(encoding="utf-8")
    d, _ = json.JSONDecoder().raw_decode(h[h.index('{"metrics"'):])
    return d["nodes"], d["cit"]


def run(N, cit, abstracts_only, drop_reviews=False):
    # drop_reviews: robustness check, since reviews are co-cited en masse and share vocabulary
    pre = [i for i, n in enumerate(N) if n["y"] <= SPLIT and (n["ab"] or not abstracts_only)
           and not (drop_reviews and n["rv"])]
    pos = {i: k for k, i in enumerate(pre)}
    # ---- predictor side: 2019 world only ----
    G = nx.Graph()
    G.add_nodes_from(range(len(pre)))
    G.add_edges_from((pos[a], pos[b]) for a, b in cit if a in pos and b in pos)
    comm = {m: ci for ci, c in enumerate(louvain_communities(G, seed=0)) for m in c}
    dist = dict(nx.all_pairs_shortest_path_length(G, cutoff=MIN_DIST - 1))  # pairs absent here are >= MIN_DIST
    indeg = collections.Counter(pos[b] for a, b in cit if a in pos and b in pos)  # in-sample citations by SPLIT
    docs = [N[i]["t"] + ". " + N[i]["ab"] for i in pre]
    X = TfidfVectorizer(stop_words=STOP, min_df=3, max_df=0.5, sublinear_tf=True,
                        token_pattern=r"[a-zA-Z][a-zA-Z\-]{2,}").fit_transform(docs)
    S = (X @ X.T).toarray()
    # ---- outcome side: citing papers after SPLIT ----
    post = sorted({a for a, b in cit if N[a]["y"] > SPLIT and b in pos})
    prow = {a: r for r, a in enumerate(post)}
    rows, cols = zip(*[(prow[a], pos[b]) for a, b in cit if a in prow and b in pos])
    R = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(post), len(pre)))
    CC = (R.T @ R).toarray()  # CC[i, j] = number of later papers citing both i and j
    # ---- candidate pairs: different community, >= MIN_DIST apart in 2019 ----
    iu, ju = np.triu_indices(len(pre), 1)
    cm = np.array([comm[k] for k in range(len(pre))])
    near = np.zeros((len(pre), len(pre)), bool)
    for a, dd in dist.items():
        near[a, list(dd)] = True
    keep = (cm[iu] != cm[ju]) & ~near[iu, ju]
    iu, ju = iu[keep], ju[keep]
    sim, y = S[iu, ju], (CC[iu, ju] > 0).astype(int)
    pop = np.log1p([indeg[k] for k in range(len(pre))])
    popsum = pop[iu] + pop[ju]  # log of the product of (1 + in-degree)
    bins = np.digitize(popsum, np.quantile(popsum, np.linspace(0, 1, N_POP_BINS + 1)[1:-1]))
    rate_by_bin = np.array([y[bins == b].mean() for b in range(N_POP_BINS)])
    out = {"papers": len(pre), "review_flagged": sum(N[i]["rv"] for i in pre), "later_citing_papers": len(post), "candidate_pairs": int(len(y)),
           "base_rate": float(y.mean()), "auc_similarity": float(roc_auc_score(y, sim)),
           "auc_popularity_only": float(roc_auc_score(y, popsum))}
    # AUC of similarity inside each popularity stratum (does text add anything beyond popularity?)
    aucs = [(roc_auc_score(y[bins == b], sim[bins == b]), (bins == b).sum()) for b in range(N_POP_BINS)
            if 0 < y[bins == b].sum() < (bins == b).sum()]
    out["auc_similarity_within_popularity_strata"] = float(np.average([a for a, _ in aucs], weights=[w for _, w in aucs]))
    order = np.argsort(-sim)
    for k in TOP_K:
        top = order[:k]
        out[f"top{k}"] = {"hit_rate": float(y[top].mean()),
                          "expected_from_popularity": float(rate_by_bin[bins[top]].mean()),  # matched null
                          "lift_vs_base": float(y[top].mean() / y.mean()),
                          "lift_vs_popularity_matched": float(y[top].mean() / rate_by_bin[bins[top]].mean())}
    # permutation null on the top-100: shuffle similarity within popularity strata
    rng = np.random.default_rng(0)
    hits = []
    for _ in range(1000):
        s2 = sim.copy()
        for b in range(N_POP_BINS):
            m = np.where(bins == b)[0]
            s2[m] = rng.permutation(s2[m])
        hits.append(y[np.argsort(-s2)[:100]].mean())
    out["top100_permutation_null_mean_sd"] = [float(np.mean(hits)), float(np.std(hits))]
    out["top100_permutation_p"] = float((np.sum(np.array(hits) >= out["top100"]["hit_rate"]) + 1) / 1001)
    out["examples_top10"] = [{"a": N[pre[iu[o]]]["t"], "b": N[pre[ju[o]]]["t"], "sim": round(float(sim[o]), 3),
                              "later_cocitations": int(CC[iu[o], ju[o]])} for o in order[:10]]
    return out


def main():
    N, cit = load()
    res = {"field": FIELD, "split_year": SPLIT, "min_dist": MIN_DIST,
           "abstracts_only": run(N, cit, True), "all_papers_title_fallback": run(N, cit, False),
           "abstracts_only_no_reviews": run(N, cit, True, drop_reviews=True)}
    (ROOT / "data" / "processed" / FIELD / "predict_links.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
