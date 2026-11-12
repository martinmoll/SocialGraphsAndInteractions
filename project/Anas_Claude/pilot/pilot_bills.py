"""Exploratory pilot, 12 Nov 2026: what are the bills Republicans sign across the aisle about?
Floor-speech vocabulary scores each bill title as Republican- or Democratic-sounding. One run."""
import sys, re, numpy as np, pandas as pd
from collections import Counter
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as STOP
P=sys.argv[1]; rng=np.random.default_rng(11)
sp=pd.read_parquet(f"{P}/speeches.parquet"); m=pd.read_csv(f"{P}/members.csv")
b=pd.read_parquet(f"{P}/bills.parquet"); c=pd.read_parquet(f"{P}/cosponsors.parquet")
pty=m.set_index("bioguide").party
sp=sp[(sp.n_words>=50)].copy(); sp["party"]=sp.bioguide.map(pty); sp=sp[sp.party.isin(["R","D"])]
tok=lambda t:[w for w in re.findall(r"[a-z]{3,}",t.lower()) if w not in STOP]
cnt={"R":Counter(),"D":Counter()}; users={}
for bg,p,t in zip(sp.bioguide,sp.party,sp.text):
    ws=tok(t); cnt[p].update(ws)
    for w in set(ws): users.setdefault(w,set()).add(bg)
tot={p:sum(cnt[p].values()) for p in cnt}
vocab=[w for w,u in users.items() if len(u)>=20]
part={w:np.log2((cnt["R"][w]/tot["R"]*1e4+0.1)/(cnt["D"][w]/tot["D"]*1e4+0.1)) for w in vocab}
print("vocab",len(vocab),"| most R:",sorted(part,key=part.get)[-12:],"| most D:",sorted(part,key=part.get)[:12])
b=b[b.type.isin(["hr","hjres"])].copy(); b["sp"]=b.sponsor.map(pty)
def score(t):
    v=[part[w] for w in tok(t) if w in part and w not in ("act","bill","amend","provide","purposes","united","states","code","title")]
    return np.mean(v) if len(v)>=2 else np.nan
b["score"]=b.title.map(score)
print("bills",len(b),"scored",b.score.notna().sum(),"| mean title score by sponsor party:",b.groupby("sp").score.mean().round(3).to_dict())
# validity: does the title score tell sponsor party? AUC
x=b.dropna(subset=["score"]); x=x[x.sp.isin(["R","D"])]
from sklearn.metrics import roc_auc_score
print("AUC title score -> sponsor is Republican: %.3f (n=%d)"%(roc_auc_score(x.sp=="R",x.score),len(x)))
cc=c[~c.withdrawn].merge(b[["bill_id","sp","score","policy_area","title"]],on="bill_id"); cc["cp"]=cc.cosponsor.map(pty)
cc["q"]=pd.PeriodIndex(cc.date,freq="Q").astype(str)
D=x[x.sp=="D"].copy()
nR=cc[cc.cp=="R"].groupby("bill_id").size(); nD=cc[cc.cp=="D"].groupby("bill_id").size()
D["nR"]=D.bill_id.map(nR).fillna(0); D["nD"]=D.bill_id.map(nD).fillna(0)
print("\nDemocratic-sponsored bills n=%d; with >=1 R cosponsor: %.1f%%"%(len(D),(D.nR>0).mean()*100))
print("Spearman(title score, number of R cosponsors) among D bills: %.3f p=%.2g"%spearmanr(D.score,D.nR))
D["fifth"]=pd.qcut(D.score,5,labels=["most D-sounding","2","3","4","most R-sounding"])
print(D.groupby("fifth",observed=True).agg(bills=("nR","size"),share_with_R=("nR",lambda v:(v>0).mean()),mean_R_cosp=("nR","mean"),mean_D_cosp=("nD","mean"),mean_score=("score","mean")).round(3))
# time: what R->D ties are about, vs D->D ties in the same quarter
t=cc[(cc.sp=="D")&cc.score.notna()]
med=D.score.median()
g=t.groupby(["q","cp"]).score.agg(["mean","size"]).unstack().round(3); print("\nMean title score of D-sponsored bills signed, by quarter and signer's party (lower = more Democratic-sounding)\n",g)
g2=t.assign(dem=t.score<med).groupby(["q","cp"]).dem.mean().unstack().round(3); print("\nShare of signatures on D bills that sound more Democratic than the median D bill\n",g2[["D","R"]])
# policy areas of R->D ties
t2=cc[(cc.sp=="D")&(cc.cp=="R")].copy(); t2["h"]=np.where(t2.date<"2025-12-01","early","late")
pa=t2.groupby(["policy_area","h"]).size().unstack(fill_value=0); pa=pa/pa.sum()*100; pa["diff"]=pa.late-pa.early
print("\nR->D signatures by policy area, pct of period (n early=%d, late=%d)"%(int((t2.h=="early").sum()),int((t2.h=="late").sum())))
print(pa.sort_values("late",ascending=False).head(10).round(1)); print("biggest movers\n",pa.sort_values("diff").round(1).iloc[[0,1,2,-3,-2,-1]])
top=t2[t2.h=="late"].groupby(["bill_id","title"]).size().sort_values(ascending=False).head(12); print("\nD bills with most Republican signatures, late period\n",top.to_string())
