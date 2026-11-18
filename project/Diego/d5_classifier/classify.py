"""D5: what do floor mentions do? A TF-IDF and logistic-regression classifier trained on the hand-labelled
mentions, checked against them, then applied to every floor mention.

Run from project/:  python Diego/d5_classifier/classify.py

Training labels: Diego's code for each of the 100 mentions in ../d2_labelling/labels_final.csv (written by
agreement.py when the sheets come back). Until then it runs on Claude's 50 codes in claude_codes.csv, and
every output is stamped PLACEHOLDER: those numbers are for testing the pipeline and go nowhere.

Choices (each footnoted in README.md):
  text       the mention's context, with the named member's surname replaced by NAMED, so the model learns
             what is said about the person and not who the person is
  features   TF-IDF on words and word pairs, lower case, sublinear term frequency, words in 2+ mentions
  model      logistic regression, classes weighted by inverse frequency, C = 1, not tuned
  check      leave-one-out cross-validation: each labelled mention is predicted by a model that never saw
             it. Reported against a majority-class baseline, with accuracy, macro F1 and the confusion matrix
  apply      refit on all labelled mentions, predict all floor mentions between a Republican and a Democrat
             or within a party, report the share of each code for cross-party and same-party mentions

Writes: results.txt, shares.csv, predictions.parquet, figures/d5_codes.png
"""
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.pipeline import make_pipeline

HERE = Path(__file__).parent
D2 = HERE.parent / "d2_labelling"
CODES = list("PADNX")
NAMES = {"P": "procedure", "A": "agreeing", "D": "disagreeing", "N": "neutral", "X": "wrong person"}

members = pd.read_csv("data/processed/members.csv").set_index("bioguide")
mentions = pd.read_parquet("Martin/mentions.parquet")
key = pd.read_csv(D2 / "full_key.csv").set_index("id")

if (D2 / "labels_final.csv").exists():
    lab = pd.read_csv(D2 / "labels_final.csv", keep_default_na=False).set_index("id")
    labels, PLACEHOLDER = lab.label[lab.label != ""], False
else:
    labels, PLACEHOLDER = pd.read_csv(D2 / "claude_codes.csv").set_index("id").code, True
STAMP = "PLACEHOLDER (Claude's 50 codes, not the human labels): " if PLACEHOLDER else ""


def plain(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()


def masked(context, bioguide):
    """The context with the named member's surname replaced by NAMED (case and accents ignored)."""
    return re.sub(r"\b" + re.escape(plain(members["last"][bioguide])) + r"\b", "NAMED", plain(context), flags=re.I)


train = key.loc[labels.index]
X_train = [masked(c, b) for c, b in zip(train.context, train.named)]
y_train = np.asarray(labels.astype(str).str.upper().tolist(), dtype=object)
model = make_pipeline(
    TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2, sublinear_tf=True),
    LogisticRegression(class_weight="balanced", C=1.0, max_iter=5000),
)

out = [f"{STAMP}D5 classifier, {len(y_train)} labelled mentions",
       "labels: " + ", ".join(f"{c} {int((y_train == c).sum())}" for c in CODES)]
pred = cross_val_predict(model, X_train, y_train, cv=LeaveOneOut())
majority = pd.Series(y_train).mode()[0]
present = [c for c in CODES if c in set(y_train) | set(pred)]
out += ["", "Leave-one-out check against the hand labels",
        f"  accuracy {accuracy_score(y_train, pred):.0%}  (always guessing '{majority}': {np.mean(y_train == majority):.0%})",
        f"  macro F1 {f1_score(y_train, pred, average='macro', labels=present, zero_division=0):.2f}",
        "  per code F1: " + ", ".join(f"{c} {f:.2f}" for c, f in zip(present, f1_score(y_train, pred, average=None, labels=present, zero_division=0))),
        "  confusion (rows: hand label, columns: classifier)",
        pd.DataFrame(confusion_matrix(y_train, pred, labels=present), index=present, columns=present).to_string()]
cross_train = train.cross.values
for name, mask in (("cross-party", cross_train), ("same-party", ~cross_train)):
    if mask.sum():
        out.append(f"  accuracy on {name} mentions: {accuracy_score(y_train[mask], pred[mask]):.0%} (n = {mask.sum()})")

model.fit(X_train, y_train)
vec, clf = model.named_steps["tfidfvectorizer"], model.named_steps["logisticregression"]
terms = np.array(vec.get_feature_names_out())
out += ["", "Terms that weigh most for each code"]
for k, c in enumerate(clf.classes_):
    w = clf.coef_[k] if len(clf.classes_) > 2 else (clf.coef_[0] if k == 1 else -clf.coef_[0])
    out.append(f"  {c}: " + ", ".join(terms[np.argsort(w)[::-1][:10]]))

# ---------------------------------------------------------------- apply to every floor mention
M = mentions[(mentions.source == "floor") & mentions.speaker.isin(members.index) & mentions.named.isin(members.index)].copy()
M["speaker_party"], M["named_party"] = members.party[M.speaker].values, members.party[M.named].values
M = M[M.speaker_party.isin(["R", "D"]) & M.named_party.isin(["R", "D"])]
M["cross"] = M.speaker_party != M.named_party
M["code"] = model.predict([masked(c, b) for c, b in zip(M.context, M.named)])
M[["speaker", "named", "date", "doc_id", "cross", "is_yield", "code"]].to_parquet(HERE / "predictions.parquet")

kind = lambda s: np.where(s, "cross-party", "same-party")
pred_share = pd.crosstab(kind(M.cross), M.code, normalize="index").reindex(columns=CODES, fill_value=0)
hand_share = pd.crosstab(kind(train.cross.values), y_train, normalize="index").reindex(columns=CODES, fill_value=0)
shares = pd.concat({"classifier, all mentions": pred_share, "hand labels, sample": hand_share}).round(3)
shares.index.names, shares.columns.name = ["source", "mentions"], None
shares.to_csv(HERE / "shares.csv")
out += ["", f"Applied to {len(M):,} floor mentions ({int(M.cross.sum()):,} cross-party, {int((~M.cross).sum()):,} same-party)",
        "Share of each code:", shares.to_string(),
        "", "The classifier's shares carry its errors: read them with the confusion matrix above."]
(HERE / "results.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))

# ---------------------------------------------------------------- figure
(HERE / "figures").mkdir(exist_ok=True)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
x = np.arange(len(CODES))
for ax, group in zip(axes, ["cross-party", "same-party"]):
    ax.bar(x - 0.2, pred_share.loc[group] if group in pred_share.index else 0, 0.4, label=f"classifier, all {group} mentions", color="#4C72B0")
    ax.bar(x + 0.2, hand_share.loc[group] if group in hand_share.index else 0, 0.4, label="hand labels, sample", color="#BBBBBB")
    ax.set_xticks(x, [NAMES[c] for c in CODES], rotation=20)
    ax.set_title(f"{group} mentions (n = {int((M.cross == (group == 'cross-party')).sum()):,})", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("share of mentions")
axes[0].legend(frameon=False, fontsize=8)
fig.suptitle(f"{STAMP}What floor mentions do", fontsize=11)
fig.tight_layout()
fig.savefig(HERE / "figures" / "d5_codes.png", dpi=200)
