"""Scout rerun, 12 Nov 2026: stricter floor names matcher (House section only, surname must be last token), precision sample, popularity-preserving null."""
import sys, re, numpy as np, pandas as pd
from scipy.stats import spearmanr
P=sys.argv[1]; rng=np.random.default_rng(3)
sp=pd.read_parquet(f"{P}/speeches.parquet"); m=pd.read_csv(f"{P}/members.csv"); b=pd.read_parquet(f"{P}/bills.parquet"); c=pd.read_parquet(f"{P}/cosponsors.parquet")
m=m[m.party.isin(["R","D"])]; pty=m.set_index("bioguide").party; last=m.set_index("bioguide")["last"]
cnt=m["last"].value_counts(); u=m[m["last"].map(cnt)==1]; byname=dict(zip(u["last"],u.bioguide))
RX=re.compile(r"\b(?:Mr\.|Ms\.|Mrs\.|Representatives?|Rep\.|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member)\s+((?:[A-Z][A-Za-z'’\-]+\s){0,2}[A-Z][A-Za-z'’\-]+)")
sp=sp[(sp.n_words>=50)&sp.bioguide.isin(pty.index)&(sp.section=="H")]
rows=[]
for src,t in zip(sp.bioguide,sp.text):
    for mm in RX.finditer(t):
        k=mm.group(1).split()[-1]; k=k.title() if k.isupper() else k
        if k in byname and byname[k]!=src: rows.append((src,byname[k],t[max(0,mm.start()-70):mm.end()+50].replace("\n"," ")))
M=pd.DataFrame(rows,columns=["s","t","ctx"]); print("mentions",len(M),"pairs",M[["s","t"]].drop_duplicates().shape[0],"speakers",M.s.nunique())
print("most named:",[(last[t],k) for t,k in M.t.value_counts().head(10).items()])
print("--- 25 random matches to read")
for r in M.sample(25,random_state=4).itertuples(): print(f"[{last[r.s]} -> {last[r.t]}] …{r.ctx}…")
cc=c[~c.withdrawn].merge(b[["bill_id","sponsor","type"]],on="bill_id"); cc=cc[cc.type.isin(["hr","hjres"])&cc.sponsor.isin(pty.index)&cc.cosponsor.isin(pty.index)]
tie={frozenset(x) for x in cc.groupby(["cosponsor","sponsor"]).size().index if x[0]!=x[1]}
def overlap(s,t): 
    pr={(a,b) for a,b in zip(s,t) if a!=b}; return np.mean([frozenset(p) in tie for p in pr])
obs=overlap(M.s.values,M.t.values); null=[]
for _ in range(300):
    t2=M.t.values.copy()
    for p in ("R","D"):
        idx=np.where(pty[M.t].values==p)[0]; t2[idx]=rng.permutation(t2[idx])
    null.append(overlap(M.s.values,t2))
print("\nnamed pairs with a cosponsorship tie: %.3f | null keeping each speaker's count, each target's popularity and party: %.3f ± %.3f"%(obs,np.mean(null),np.std(null)))
M["cross"]=pty[M.s].values!=pty[M.t].values
nm=M.groupby("s").cross.agg(["mean","size"]); cc["cross"]=cc.sponsor.map(pty)!=cc.cosponsor.map(pty); dd=cc.groupby("cosponsor").cross.agg(["mean","size"])
j=nm[nm["size"]>=10][["mean"]].rename(columns={"mean":"names"}).join(dd[dd["size"]>=10]["mean"].rename("deeds"),how="inner").join(pty.rename("party"))
for p in "RD":
    x=j[j.party==p]; r,pv=spearmanr(x.names,x.deeds); nl=[spearmanr(rng.permutation(x.names.values),x.deeds)[0] for _ in range(2000)]
    print("%s n=%d Spearman names vs deeds %.3f p=%.3g | shuffle band (%.2f, %.2f)"%(p,len(x),r,pv,*np.quantile(nl,[.025,.975])))
