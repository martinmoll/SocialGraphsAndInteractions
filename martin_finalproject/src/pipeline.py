"""Prototype pipeline: graph -> communities -> bridges -> text topics -> NMI -> null -> explorer.
Usage: python src/pipeline.py FIELD [N_NULL]     (default 100 null runs)
Every CHOICE comment is a modelling decision that must be defensible; see NOTES.md.
"""
import collections
import csv
import glob
import itertools
import json
import pathlib
import random
import re
import sys

import networkx as nx
import numpy as np
from networkx.algorithms.community import louvain_communities, modularity
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer, TfidfVectorizer
from sklearn.metrics import normalized_mutual_info_score as nmi
from sklearn.preprocessing import normalize

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIELD = sys.argv[1]
OUT = ROOT / "data" / "processed" / FIELD
OUT.mkdir(parents=True, exist_ok=True)
N_NULL = int(sys.argv[2]) if len(sys.argv) > 2 else 100

# ---- CHOICES (all in one place) ----
COUPLING_MIN_SHARED = 5   # coupling edge = two papers share >= 5 references
MIN_DEGREE = 5            # a paper needs >= 5 citation links before its participation coeff. means anything
BRIDGE_TOP = 0.10         # bridge = top 10% participation among eligible papers
HUB_TOP = 0.05            # "hub" flag = top 5% degree
K_TOPICS = 12             # number of LDA topics / k-means clusters
SWAPS_PER_EDGE = 10       # rewiring attempts per edge in each null run
REVIEW_RE = re.compile(r"\b(review|survey|overview|state[- ]of[- ]the[- ]art|perspectives?|roadmap)\b", re.I)
FIELD_STOP = {"energy_systems": {"energy", "system", "systems"}, "ocean_science": {"ocean", "oceans", "oceanic"}}
DOMAIN_STOP = FIELD_STOP.get(FIELD, set()) | {"paper", "study", "results", "based", "using", "proposed",
               "used", "analysis", "model", "method", "approach", "different", "new", "elsevier", "rights",
               "reserved", "ltd", "abstract", "research", "present", "presented", "article", "work",
               "review", "overview", "survey", "comprehensive"}   # document-type words, not topics


def abstract_of(w):
    inv = w.get("abstract_inverted_index") or {}
    pos = sorted((p, word) for word, ps in inv.items() for p in ps)
    return " ".join(word for _, word in pos)


def participation(U, comm):
    """Guimera-Amaral participation coefficient: 1 - sum_c (k_ic / k_i)^2."""
    P = {}
    for n in U:
        k = U.degree(n)
        cnt = collections.Counter(comm[m] for m in U[n])
        P[n] = 1 - sum((c / k) ** 2 for c in cnt.values()) if k else 0.0
    return P


def rewire(edges, year, rng):
    """Degree-preserving target swap that keeps every edge pointing new -> old (same year allowed)."""
    edges = list(edges)
    eset = set(edges)
    for _ in range(SWAPS_PER_EDGE * len(edges)):
        i, j = rng.randrange(len(edges)), rng.randrange(len(edges))
        (a, b), (c, d) = edges[i], edges[j]
        if a == c or b == d or a == d or c == b:
            continue
        if year[a] < year[d] or year[c] < year[b]:
            continue
        if {(a, d), (c, b), (d, a), (b, c)} & eset:
            continue
        eset -= {(a, b), (c, d)}
        eset |= {(a, d), (c, b)}
        edges[i], edges[j] = (a, d), (c, b)
    return edges


def bridges_from(P, eligible):
    ranked = sorted(eligible, key=lambda n: (-P[n], n))
    return set(ranked[: max(1, int(BRIDGE_TOP * len(ranked)))])


def main():
    raw = json.load(open(sorted(glob.glob(str(ROOT / f"data/raw/openalex_{FIELD}_*.json")))[-1], encoding="utf-8"))
    W = {w["id"].rsplit("/", 1)[-1]: w for w in raw["works"]}
    short = lambda u: u.rsplit("/", 1)[-1]
    year = {i: w["publication_year"] for i, w in W.items()}
    M = {"field": FIELD, "query": raw["query"], "collected": raw["date"], "total_matching": raw["total_matching"], "n_works": len(W)}

    # ---- 1. graphs ----
    G = nx.DiGraph()
    G.add_nodes_from(W)
    G.add_edges_from((i, short(r)) for i, w in W.items() for r in w["referenced_works"]
                     if short(r) in W and short(r) != i)
    M["n_citation_edges"] = G.number_of_edges()
    M["edges_pointing_to_newer"] = sum(year[a] < year[b] for a, b in G.edges)
    lcc = max(nx.weakly_connected_components(G), key=len)
    G = G.subgraph(sorted(lcc)).copy()   # CHOICE: analyse the largest weakly connected component only
    U = nx.Graph(G.edges)
    U.add_nodes_from(G)
    nodes = sorted(G)
    M["lcc_nodes"], M["lcc_edges_directed"], M["lcc_edges_undirected"] = len(nodes), G.number_of_edges(), U.number_of_edges()

    inv = collections.defaultdict(list)
    for i, w in W.items():
        for r in set(w["referenced_works"]):
            inv[r].append(i)
    shared = collections.Counter()
    for l in inv.values():
        shared.update(itertools.combinations(sorted(l), 2))
    coupling = [(a, b, c) for (a, b), c in shared.items() if c >= COUPLING_MIN_SHARED]
    n = len(W)
    M["coupling_edges"] = len(coupling)
    M["coupling_density"] = len(coupling) / (n * (n - 1) / 2)
    M["coupling_lcc"] = max(map(len, nx.connected_components(nx.Graph([(a, b) for a, b, _ in coupling]))))

    # ---- 2. communities (Louvain; leidenalg is not installed) ----
    parts = [louvain_communities(U, seed=s) for s in range(10)]
    labels = [{m: ci for ci, c in enumerate(p) for m in c} for p in parts]
    mods = [modularity(U, p) for p in parts]
    pair_nmi = [nmi([a[x] for x in nodes], [b[x] for x in nodes]) for a, b in itertools.combinations(labels, 2)]
    part = sorted(parts[0], key=len, reverse=True)   # CHOICE: seed 0 is the reference partition
    comm = {m: ci for ci, c in enumerate(part) for m in c}
    M["modularity"] = mods[0]
    M["modularity_10seeds_mean_sd"] = [float(np.mean(mods)), float(np.std(mods))]
    M["stability_pairwise_nmi_mean_min"] = [float(np.mean(pair_nmi)), float(np.min(pair_nmi))]
    M["community_sizes"] = [len(c) for c in part]

    # ---- 3. bridges ----
    P = participation(U, comm)
    btw = nx.betweenness_centrality(U, k=500, seed=0)   # CHOICE: sampled (500 sources), not exact
    deg = dict(U.degree())
    eligible = [x for x in nodes if deg[x] >= MIN_DEGREE]
    bridges = bridges_from(P, eligible)
    hub_cut = np.quantile([deg[x] for x in nodes], 1 - HUB_TOP)
    is_review = {x: bool(REVIEW_RE.search(W[x]["title"] or "")) for x in nodes}
    is_hub = {x: deg[x] >= hub_cut for x in nodes}
    M["n_eligible"], M["n_bridges"] = len(eligible), len(bridges)
    M["bridge_P_cutoff"] = min(P[b] for b in bridges)
    M["bridges_review_share"] = float(np.mean([is_review[b] for b in bridges]))
    M["eligible_review_share"] = float(np.mean([is_review[b] for b in eligible]))
    M["bridges_hub_share"] = float(np.mean([is_hub[b] for b in bridges]))
    M["eligible_hub_share"] = float(np.mean([is_hub[b] for b in eligible]))

    # ---- 4. text ----
    abstracts = {x: abstract_of(W[x]) for x in nodes}
    docs = [((W[x]["title"] or "") + ". " + abstracts[x]) for x in nodes]   # CHOICE: title + abstract (title only if no abstract)
    M["lcc_with_abstract"] = sum(bool(abstracts[x]) for x in nodes)
    M["all_with_abstract"] = sum(bool(w.get("abstract_inverted_index")) for w in W.values())
    stop = list(ENGLISH_STOP_WORDS | DOMAIN_STOP)
    cv = CountVectorizer(stop_words=stop, min_df=5, max_df=0.5, token_pattern=r"[a-zA-Z][a-zA-Z\-]{2,}")
    C = cv.fit_transform(docs)
    vocab = np.array(cv.get_feature_names_out())
    lda = LatentDirichletAllocation(n_components=K_TOPICS, random_state=0, max_iter=30)
    theta = lda.fit_transform(C)
    topic = theta.argmax(1)   # CHOICE: one topic per paper = its largest LDA share
    topic_words = [list(vocab[np.argsort(-row)[:8]]) for row in lda.components_]
    tf = TfidfVectorizer(vocabulary=cv.vocabulary_, stop_words=stop, token_pattern=r"[a-zA-Z][a-zA-Z\-]{2,}", sublinear_tf=True)
    X = tf.fit_transform(docs)
    # second method. ponytail: LSA + k-means stands in for sentence embeddings (sentence-transformers not installed)
    Z = normalize(TruncatedSVD(100, random_state=0).fit_transform(X))
    km = KMeans(K_TOPICS, n_init=10, random_state=0).fit_predict(Z)
    # community names: top TF-IDF terms of each community's summed text
    comm_arr = np.array([comm[x] for x in nodes])
    comm_terms = [list(vocab[np.argsort(-np.asarray(X[comm_arr == c].sum(0)).ravel())[:5]]) for c in range(len(part))]

    with open(OUT / "topic_samples.md", "w", encoding="utf-8") as f:
        f.write("# LDA topics: top words + 10 highest-share papers each (read these to NAME the topic by hand)\n")
        for t in range(K_TOPICS):
            f.write(f"\n## Topic {t}: {', '.join(topic_words[t])}  (n={int((topic == t).sum())})\n")
            for i in np.argsort(-theta[:, t])[:10]:
                f.write(f"- **{W[nodes[i]]['title']}** ({year[nodes[i]]}) {abstracts[nodes[i]][:400]}\n")

    # ---- 5. join: NMI between groupings ----
    oa_topic = [(W[x].get("primary_topic") or {}).get("display_name", "none") for x in nodes]
    oa_sub = [((W[x].get("primary_topic") or {}).get("subfield") or {}).get("display_name", "none") for x in nodes]
    has_abs = np.array([bool(abstracts[x]) for x in nodes])
    groupings = {"citation communities": comm_arr, "LDA topics": topic, "LSA k-means": km,
                 "OpenAlex topic": np.array(oa_topic), "OpenAlex subfield": np.array(oa_sub)}
    M["nmi"] = {f"{a} vs {b}": float(nmi(groupings[a], groupings[b])) for a, b in itertools.combinations(groupings, 2)}
    M["nmi_abstract_only"] = {f"{a} vs {b}": float(nmi(groupings[a][has_abs], groupings[b][has_abs]))
                              for a, b in itertools.combinations(list(groupings)[:3], 2)}
    # baseline: NMI is biased upward for many small groups -> shuffle one side
    rng_np = np.random.default_rng(0)
    M["nmi_shuffled_baseline_comm_vs_lda"] = float(np.mean([nmi(comm_arr, rng_np.permutation(topic)) for _ in range(20)]))

    # ---- 6. null: time-respecting degree-preserving rewiring ----
    idx = {x: i for i, x in enumerate(nodes)}
    el_idx = np.array([idx[x] for x in eligible])

    def topic_share(bset, drop_reviews=False):
        # drop_reviews: robustness check, since review papers bridge by citing widely
        keep = [idx[b] for b in bset if not (drop_reviews and is_review[b])]
        return np.bincount(topic[keep], minlength=K_TOPICS) / len(keep)

    obs_share = topic_share(bridges)
    obs_share_nr = topic_share(bridges, True)
    base_share = np.bincount(topic[el_idx], minlength=K_TOPICS) / len(el_idx)
    hiP = lambda PP: sum(PP[x] >= 0.6 for x in eligible)
    null = collections.defaultdict(list)
    for r in range(N_NULL):
        e = rewire(G.edges, year, random.Random(r))
        Un = nx.Graph(e)
        Un.add_nodes_from(nodes)
        pn = louvain_communities(Un, seed=r)
        cn = {m: ci for ci, c in enumerate(pn) for m in c}
        Pn = participation(Un, cn)
        null["modularity"].append(modularity(Un, pn))
        null["n_comm"].append(len(pn))
        null["mean_P"].append(np.mean([Pn[x] for x in eligible]))
        null["hiP"].append(hiP(Pn))
        bn = bridges_from(Pn, [x for x in nodes if Un.degree(x) >= MIN_DEGREE])
        null["share"].append(topic_share(bn))
        null["share_nr"].append(topic_share(bn, True))
        if r % 10 == 9:
            print(f"null {r + 1}/{N_NULL}", flush=True)
    sh, sh_nr = np.array(null["share"]), np.array(null["share_nr"])
    z = lambda obs, xs: float((obs - np.mean(xs)) / (np.std(xs) or 1))
    M["null"] = {
        "runs": N_NULL,
        "modularity_mean_sd": [float(np.mean(null["modularity"])), float(np.std(null["modularity"]))],
        "modularity_z": z(M["modularity"], null["modularity"]),
        "n_communities_real_vs_null_mean": [len(part), float(np.mean(null["n_comm"]))],
        "mean_P_real_vs_null": [float(np.mean([P[x] for x in eligible])), float(np.mean(null["mean_P"]))],
        "papers_P>=0.6_real_vs_null_mean_sd": [hiP(P), float(np.mean(null["hiP"])), float(np.std(null["hiP"]))],
        "papers_P>=0.6_z": z(hiP(P), null["hiP"]),
    }
    topics_out = [{"id": t, "words": topic_words[t], "n": int((topic == t).sum()),
                   "bridge_share": float(obs_share[t]), "base_share": float(base_share[t]),
                   "null_mean": float(sh[:, t].mean()), "null_sd": float(sh[:, t].std()),
                   "z": z(obs_share[t], sh[:, t]), "z_no_reviews": z(obs_share_nr[t], sh_nr[:, t])} for t in range(K_TOPICS)]
    M["topics"] = topics_out

    # ---- missing links: close in text, far in citations (papers with abstracts only) ----
    ai = np.where(has_abs)[0]
    S = (X[ai] @ X[ai].T).toarray()
    np.fill_diagonal(S, 0)
    iu = np.triu_indices(len(ai), 1)
    missing = []
    for o in np.argsort(-S[iu])[:3000]:
        a, b = nodes[ai[iu[0][o]]], nodes[ai[iu[1][o]]]
        if U.has_edge(a, b) or comm[a] == comm[b]:
            continue
        d = nx.shortest_path_length(U, a, b)
        if d >= 3:   # CHOICE: "far" = different community and >= 3 citation steps apart
            missing.append({"a": a, "b": b, "sim": float(S[iu][o]), "dist": d})
        if len(missing) == 20:
            break
    M["n_missing_links_listed"] = len(missing)

    # ---- layout (visual only): intra-community edges pull harder so communities separate on screen ----
    for a, b in U.edges:
        U[a][b]["w"] = 2.0 if comm[a] == comm[b] else 0.3
    pos = nx.spring_layout(U, weight="w", seed=1, iterations=80)
    xy = np.array([pos[x] for x in nodes])
    xy -= np.median(xy, 0)
    r = np.linalg.norm(xy, axis=1, keepdims=True) + 1e-9
    xy = xy / r * (r / np.quantile(r, 0.97)) ** 0.55   # visual only: spread the dense core, pull in outliers
    pos = dict(zip(nodes, xy))

    # ---- outputs ----
    with open(OUT / "nodes.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["id", "title", "year", "doi", "cited_by", "degree", "community", "participation", "betweenness",
                     "bridge", "review_flag", "hub_flag", "lda_topic", "kmeans", "openalex_topic", "has_abstract"])
        for i, x in enumerate(nodes):
            wr.writerow([x, W[x]["title"], year[x], W[x]["doi"], W[x]["cited_by_count"], deg[x], comm[x], round(P[x], 4),
                         round(btw[x], 6), int(x in bridges), int(is_review[x]), int(is_hub[x]), topic[i], km[i],
                         oa_topic[i], int(has_abs[i])])
    with open(OUT / "edges_citation.csv", "w", newline="") as f:
        csv.writer(f).writerows([["citing", "cited"], *G.edges])
    with open(OUT / "edges_coupling.csv", "w", newline="") as f:
        csv.writer(f).writerows([["a", "b", "shared_refs"], *coupling])
    json.dump(M, open(OUT / "metrics.json", "w"), indent=1)

    data = {
        "metrics": M, "topics": topics_out, "missing": missing,
        "communities": [{"id": c, "n": len(part[c]), "terms": comm_terms[c]} for c in range(len(part))],
        "nodes": [{"id": x, "t": W[x]["title"], "y": year[x], "doi": W[x]["doi"], "cb": W[x]["cited_by_count"],
                   "c": comm[x], "P": round(P[x], 3), "b": round(btw[x], 5), "k": deg[x], "tp": int(topic[i]),
                   "oa": oa_topic[i], "br": int(x in bridges), "rv": int(is_review[x]), "hub": int(is_hub[x]),
                   "x": round(float(pos[x][0]), 4), "yy": round(float(pos[x][1]), 4), "ab": abstracts[x]}
                  for i, x in enumerate(nodes)],
        "cit": [[idx[a], idx[b]] for a, b in G.edges],
        "cou": [[idx[a], idx[b]] for a, b, _ in coupling if a in idx and b in idx],
    }
    html = (ROOT / "src" / "explorer_template.html").read_text(encoding="utf-8")
    (ROOT / f"explorer_{FIELD}.html").write_text(
        html.replace("FIELDNAME", FIELD.replace("_", " ")).replace("/*DATA*/", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
    print(json.dumps({k: v for k, v in M.items() if k != "topics"}, indent=1))
    for t in sorted(topics_out, key=lambda t: -t["z"]):
        print(f"z={t['z']:+.1f} (no reviews {t['z_no_reviews']:+.1f}) bridge {t['bridge_share']:.3f} null {t['null_mean']:.3f} base {t['base_share']:.3f}  T{t['id']} {' '.join(t['words'][:6])}")


if __name__ == "__main__":
    main()
