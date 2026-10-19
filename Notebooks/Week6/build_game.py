"""Builds the data behind the "Mutant or not?" game at the top of posts/week6/index.html.

Run from this folder: python build_game.py (standard library only). It reads the frozen
week-1/5/6 data, recomputes the one answer the post's viz-data does not carry (is mutant(s)
among a page's 10 highest TF-IDF words, the notebook's in_fp), and writes the result into the
post's <script id="game-data"> block. viz-data is left untouched, so the notebook's
staleness check on it still holds.
"""
import json, math, re, urllib.parse, zipfile
from collections import Counter
from pathlib import Path

DATA1, DATA5, DATA6 = Path("../../Data/Week1"), Path("../../Data/Week5"), Path("../../Data/Week6")
POST = Path("../../posts/week6/index.html")

with zipfile.ZipFile(DATA5 / "marvel_pages.zip") as z:
    pages = {urllib.parse.unquote(n.split("/")[-1][:-4]): z.read(n).decode("utf-8")
             for n in z.namelist() if n.endswith(".txt") and "README" not in n}
KEYS = sorted(pages); N = len(KEYS)

# same tokenizer and TF-IDF definition as SGI-6.11.ipynb
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")
MUT = {"mutant", "mutants", "mutant's", "mutants'", "mutant’s", "mutants’"}
toks = {k: WORD.findall(pages[k].lower()) for k in KEYS}
assert sum(map(len, toks.values())) == 727261
DF = Counter(t for k in KEYS for t in set(toks[k]))


def fingerprint(k):
    c, n = Counter(toks[k]), len(toks[k])
    w = {t: v / n * math.log(N / DF[t]) for t, v in c.items()}
    return {t for t, _ in sorted(w.items(), key=lambda x: -x[1])[:10]}


in_fp = [bool(MUT & fingerprint(k)) for k in KEYS]
assert sum(in_fp) == 7, sum(in_fp)                               # the notebook's fingerprint_pages

# the dossier: the article's lead, publishing history dropped, the word itself marked ⟦…⟧ for the page to black out
SENT = re.compile(r"(?<!Dr\.)(?<!Mr\.)(?<!Ms\.)(?<!St\.)(?<![A-Z]\.)(?<=[.!?])\s+(?=[A-Z\"“])")
PUB = re.compile(r"first appear|created by|creators?\b|debut|#\d|\bissue\b|cover[- ]dated?|\bwriter\b|\bartist\b|"
                 r"portray|voiced|\bfilms?\b|television|video games?|\bMCU\b|publication", re.I)
CLAUSE = re.compile(r"(?:appearing|featured) in (?:American )?(?:comic )?books published by Marvel Comics", re.I)
REDACT = re.compile(r"\b(?:homo (?:sapiens )?superior|mutants?['’]?s?|mutant['’]s|mutations?)\b", re.I)


def dossier(text, limit=300):
    lead = []
    for line in text.split("\n"):
        line = line.strip()
        if not line: continue
        if len(line) < 60 and not line.endswith("."): break                 # first section heading ends the lead
        lead.append(line)
    sents = [CLAUSE.sub("in Marvel Comics", s) for p in lead for s in SENT.split(p)]
    keep = [s for s in sents if not PUB.search(s) and len(s) > 40]
    out = ""
    for s in keep:
        if out and len(out) + len(s) > limit: break
        out = (out + " " + s).strip()
    if len(out) > limit + 100: out = out[:limit].rsplit(" ", 1)[0] + " …"
    return REDACT.sub(lambda m: f"⟦{m.group(0)}⟧", out) or "The file is empty. Trust your gut."


Path(DATA6 / "mutant_category.tsv")
assert KEYS == [l.split("\t")[0] for l in (DATA6 / "mutant_category.tsv").read_text(encoding="utf-8").splitlines()[2:]]
game = {"fp": [i for i, f in enumerate(in_fp) if f], "dossier": [dossier(pages[k]) for k in KEYS]}

html = POST.read_text(encoding="utf-8")
block = '<script type="application/json" id="game-data">' + json.dumps(game, ensure_ascii=False) + "</script>"
pat = re.compile(r'<script type="application/json" id="game-data">.*?</script>', re.S)
assert pat.search(html), "post has no game-data block"
POST.write_text(pat.sub(lambda _: block, html), encoding="utf-8")
print(f"fingerprint pages: {[KEYS[i] for i in game['fp']]}; wrote {len(block):,} bytes of game data")
