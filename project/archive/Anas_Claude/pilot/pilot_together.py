"""Exploratory pilot, 12 Nov 2026: is Republican 'distancing' explained by a member's own exposure
(district lean) or by whom they work with (cosponsorship ties)? One run, definitions chosen here."""
import sys, numpy as np, pandas as pd, networkx as nx
from scipy.stats import spearmanr
P=sys.argv[1]; CUT="2025-12-01"; rng=np.random.default_rng(7)
sp=pd.read_parquet(f"{P}/speeches.parquet"); m=pd.read_csv(f"{P}/members.csv"); d=pd.read_csv(f"{P}/districts.csv")
b=pd.read_parquet(f"{P}/bills.parquet"); c=pd.read_parquet(f"{P}/cosponsors.parquet")
pty=m.set_index("bioguide").party
m=m.merge(d[["state","district","lean"]],on=["state","district"],how="left")
sp=sp[sp.n_words>=50].copy(); sp["trump"]=sp.text.str.lower().str.count(r"\btrump\b")
sp["h"]=np.where(sp.day<CUT,"e","l")
a=sp.groupby(["bioguide","h"])[["trump","n_words"]].sum().unstack()
T=pd.DataFrame({"e":a.trump.e/a.n_words.e*1e4,"l":a.trump.l/a.n_words.l*1e4,"we":a.n_words.e,"wl":a.n_words.l})
T=T[(T.we>=1500)&(T.wl>=1500)]
cc=c[~c.withdrawn].merge(b[["bill_id","sponsor","type"]],on="bill_id"); cc=cc[cc.type.isin(["hr","hjres"])]
cc["sp"]=cc.sponsor.map(pty); cc["cp"]=cc.cosponsor.map(pty); cc["h"]=np.where(cc.date<CUT,"e","l")
cc["x"]=cc.sp=="D"
w=cc[cc.cp=="R"].groupby(["cosponsor","h"]).x.agg(["mean","size"]).unstack()
W=pd.DataFrame({"ce":w["mean"].e,"cl":w["mean"].l,"k_e":w["size"].e,"k_l":w["size"].l}); W=W[(W.k_e>=10)&(W.k_l>=10)]
M=m[m.party=="R"].set_index("bioguide")[["nominate_dim1","lean","state","last"]]
df=M.join(T).join(W)
def resid(y,X):
    X=np.column_stack([np.ones(len(y))]+X); beta=np.linalg.lstsq(X,y,rcond=None)[0]; return y-X@beta
def r2(y,X):
    e=resid(y,X); return 1-e.var()/y.var()
# R-R network, undirected, weight = bills signed in either direction
rr=cc[(cc.sp=="R")&(cc.cp=="R")]
ew=rr.groupby(["cosponsor","sponsor"]).size()
G=nx.Graph()
for (u,v),k in ew.items():
    if u!=v: G.add_edge(u,v,weight=G.get_edge_data(u,v,{"weight":0})["weight"]+k)
print("R-R network:",G.number_of_nodes(),"nodes",G.number_of_edges(),"edges")
def netcorr(x, nodes, A):
    nb=(A@x)/A.sum(1); return np.corrcoef(x,nb)[0,1]
def test(col, label, base):
    s=df.dropna(subset=[col,base,"nominate_dim1","lean"]); s=s[s.index.isin(G.nodes)]
    nodes=list(s.index); A=nx.to_numpy_array(G,nodelist=nodes,weight="weight")
    keep=A.sum(1)>0; s=s[keep]; A=A[keep][:,keep]
    y=s[col].values.astype(float); z=lambda v:(v-v.mean())/v.std()
    b0=s[base].values; nom=s.nominate_dim1.values; lean=s.lean.values.astype(float)
    print(f"\n== {label}  n={len(s)}")
    print("  R2 baseline level only: %.3f | +lean: %.3f | +nominate: %.3f | +both: %.3f"%(r2(y,[b0]),r2(y,[b0,lean]),r2(y,[b0,nom]),r2(y,[b0,nom,lean])))
    print("  Spearman of change (late-early) with lean: %.2f (p=%.3f); with nominate: %.2f (p=%.3f)"%(*spearmanr(y-b0,lean),*spearmanr(y-b0,nom)))
    for nm,x in [("change adj. for start level",resid(y,[b0])),("adj. for start level + nominate + lean",resid(y,[b0,nom,lean]))]:
        obs=netcorr(x,nodes,A); null=np.array([netcorr(rng.permutation(x),nodes,A) for _ in range(2000)])
        print("  neighbour correlation [%s]: obs %.3f | shuffle null mean %.3f, 95%% band (%.3f, %.3f) | p=%.4f"%(nm,obs,null.mean(),*np.quantile(null,[.025,.975]),(np.abs(null-null.mean())>=abs(obs-null.mean())).mean()))
    # blocs
    H=G.subgraph(s.index)
    for seed in (1,2,3):
        com=nx.community.louvain_communities(H,weight="weight",seed=seed)
        lab=pd.Series({n:i for i,cset in enumerate(com) for n in cset}).reindex(s.index)
        x=resid(y,[b0,nom,lean])
        def eta(v,l):
            g=pd.Series(v).groupby(l.values); return (g.size()*(g.mean()-v.mean())**2).sum()/((v-v.mean())**2).sum()
        o=eta(x,lab); nl=np.array([eta(rng.permutation(x),lab) for _ in range(2000)])
        print("  Louvain seed %d: %d blocs, share of adjusted change explained by bloc %.3f | null mean %.3f, 97.5%% %.3f | p=%.4f"%(seed,len(com),o,nl.mean(),np.quantile(nl,.975),(nl>=o).mean()))
    return s
s1=test("l","WORDS: Trump mentions per 10k words, late period","e")
s2=test("cl","DEEDS: cross-party share of cosponsorships, late period","ce")
