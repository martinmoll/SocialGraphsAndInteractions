"""Exploratory, 12 Nov 2026: how much of cross-party cosponsorship sits on symbolic bills? One run."""
import sys, numpy as np, pandas as pd, networkx as nx
P=sys.argv[1]; rng=np.random.default_rng(5)
m=pd.read_csv(f"{P}/members.csv"); b=pd.read_parquet(f"{P}/bills.parquet"); c=pd.read_parquet(f"{P}/cosponsors.parquet")
pty=m.set_index("bioguide").party
b=b[b.type.isin(["hr","hjres"])].copy()
RX=r"commemorat|\bcoins?\b|\bmedal|post office|\bdesignat|\bnam(e|ing)\b|\brenam|\bmemorial\b|\bstamp\b|recogni|honor|\bday\b|\bweek\b|\bmonth\b|anniversary"
b["sym"]=b.title.str.lower().str.contains(RX,regex=True)
b["sp"]=b.sponsor.map(pty)
print("bills %d, symbolic by title rule: %.1f%% (R-sponsored %.1f%%, D-sponsored %.1f%%)"%(len(b),b.sym.mean()*100,b[b.sp=="R"].sym.mean()*100,b[b.sp=="D"].sym.mean()*100))
print("sample symbolic titles:",list(b[b.sym].title.sample(8,random_state=1)))
cc=c[~c.withdrawn].merge(b[["bill_id","sp","sym"]],on="bill_id"); cc["cp"]=cc.cosponsor.map(pty); cc=cc[cc.sp.isin(["R","D"])&cc.cp.isin(["R","D"])]
cc["cross"]=cc.sp!=cc.cp; cc["q"]=pd.PeriodIndex(cc.date,freq="Q").astype(str)
print("\nshare of signatures on symbolic bills: same-party %.1f%%, cross-party %.1f%%"%(cc[~cc.cross].sym.mean()*100,cc[cc.cross].sym.mean()*100))
r=cc[cc.cp=="R"]
t=pd.DataFrame({"R->D signatures":r[r.cross].groupby("q").size(),"of which symbolic":r[r.cross].groupby("q").sym.mean().round(3),
 "cross share all":r.groupby("q").cross.mean().round(3),"cross share symbolic":r[r.sym].groupby("q").cross.mean().round(3),"cross share substantive":r[~r.sym].groupby("q").cross.mean().round(3)})
print(t)
print("\nwhole Congress, both parties: cross-party share on symbolic %.3f (n=%d) vs substantive %.3f (n=%d)"%(cc[cc.sym].cross.mean(),cc.sym.sum(),cc[~cc.sym].cross.mean(),(~cc.sym).sum()))
def layer(x):
    G=nx.Graph()
    for (u,v),k in x.groupby(["cosponsor","bill_id"]).size().reset_index().merge(b[["bill_id","sponsor"]],on="bill_id").groupby(["cosponsor","sponsor"]).size().items():
        if u!=v: G.add_edge(u,v,weight=G.get_edge_data(u,v,{"weight":0})["weight"]+k)
    return G
def partyQ(G):
    nodes=[n for n in G if pty.get(n) in ("R","D")]; G=G.subgraph(nodes)
    part=[{n for n in G if pty[n]=="R"},{n for n in G if pty[n]=="D"}]
    q=nx.community.modularity(G,part,weight="weight")
    lab=np.array([pty[n] for n in G]); ns=list(G); null=[]
    for _ in range(100):
        p=rng.permutation(lab); null.append(nx.community.modularity(G,[{n for n,l in zip(ns,p) if l=="R"},{n for n,l in zip(ns,p) if l=="D"}],weight="weight"))
    return G.number_of_nodes(),G.number_of_edges(),q,np.mean(null),np.std(null)
for nm,x in [("symbolic layer",cc[cc.sym]),("substantive layer",cc[~cc.sym])]:
    print(nm,"nodes %d edges %d | modularity of party split %.3f | label-shuffle null %.3f ± %.3f"%partyQ(layer(x)))
