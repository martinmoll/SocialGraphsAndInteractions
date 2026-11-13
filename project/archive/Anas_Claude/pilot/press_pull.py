"""Scout, 12 Nov 2026: ~40 press releases each from eight House Republicans' own sites; who do they name?"""
import sys, re, time, html, json, urllib.request, urllib.parse, collections
import pandas as pd
P,out=sys.argv[1],sys.argv[2]
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=20).read().decode("utf-8","ignore")
    except Exception as e: return ""
m=pd.read_csv(f"{P}/members.csv"); m=m[m.party.isin(["R","D"])]; d=pd.read_csv(f"{P}/districts.csv")
m=m.merge(d[["state","district","lean"]],on=["state","district"],how="left")
cnt=m["last"].value_counts(); u=m[m["last"].map(cnt)==1]; byname=dict(zip(u["last"],zip(u.bioguide,u.party)))
A="{b}/news/documentquery.aspx?DocumentTypeID=27&Page={p}"; B="{b}/press-releases?page={p}"; C="{b}/media/press-releases?page={p}"
sites={"Lawler":("swing",A,1),"Bacon":("swing",A,1),"Fitzpatrick":("swing",B,1),"Ciscomani":("swing",C,0),"Roy":("safe",C,0),"Hageman":("safe",C,0),"Biggs":("safe",C,0),"Arrington":("safe",C,0)}
LINK=re.compile(r'href="([^"#]*(?:documentsingle\.aspx\?DocumentID=\d+|/media/press-releases/[^"/?]+|/20\d\d/\d{1,2}/[^"]+))"',re.I)
DATE=re.compile(r"(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, (20\d\d)")
NAME=re.compile(r"\b(?:Rep\.|Reps\.|Representatives?|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member|Whip|Leader)\s+((?:[A-Z][\w.'’\-]+\s){0,3}[A-Z][\w'’\-]+)")
TAG=re.compile(r"([A-Z][\w'’\-]+)\s*\(([RDI])[-–‑][A-Z][A-Za-z.]{1,5}(?:[-–‑ ]?\d{1,2})?\)")
def body(h):
    k=h.find("<h1"); h=h[k:] if k>0 else h
    h=re.sub(r"(?is)<(script|style|nav|footer|form|aside).*?</\1>"," ",h); k=h.lower().find("<footer"); h=h[:k] if k>0 else h
    return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",h)))
rows=[]
for who,(kind,tpl,p0) in sites.items():
    base=f"https://{who.lower()}.house.gov"; links=[]
    for p in range(p0,p0+6):
        t=get(tpl.format(b=base,p=p)); time.sleep(0.5)
        for l in LINK.findall(t):
            l=urllib.parse.urljoin(tpl.format(b=base,p=p).split("?")[0],html.unescape(l))
            if l not in links: links.append(l)
        if len(links)>=40: break
    n=0
    for l in links[:40]:
        tx=body(get(l)); time.sleep(0.4)
        if len(tx.split())<80: continue
        y=DATE.search(tx); n+=1
        named={}
        for nm in NAME.findall(tx):
            for tok in reversed(nm.split()):
                tok=tok.rstrip("’'s") if tok.endswith(("’s","'s")) else tok
                if tok in byname and tok!=who: named[tok]=byname[tok][1]; break
        tags=[(a,b) for a,b in TAG.findall(tx) if a!=who]
        bi=[mm.start()/max(len(tx),1) for mm in re.finditer(r"bipartisan",tx,re.I)]
        rows.append(dict(member=who,kind=kind,url=l,year=y.group(1) if y else None,words=len(tx.split()),named=named,tags=tags,bip=len(bi),bip_only_tail=bool(bi) and min(bi)>0.85,head=tx[:200]))
    print(who,"links found",len(links),"releases parsed",n,flush=True)
json.dump(rows,open(out,"w"),indent=1)
df=pd.DataFrame(rows); df=df[df.year.isin(["2025","2026"])|df.year.isna()]
df["nR"]=df.named.map(lambda x:sum(v=="R" for v in x.values())); df["nD"]=df.named.map(lambda x:sum(v=="D" for v in x.values()))
df["tagD"]=df.tags.map(lambda x:sum(b=="D" for a,b in x)); df["tagR"]=df.tags.map(lambda x:sum(b=="R" for a,b in x))
g=df.groupby(["kind","member"]).agg(releases=("words","size"),median_words=("words","median"),names_any=("named",lambda s:(s.map(len)>0).mean()),names_R=("nR",lambda s:(s>0).mean()),names_D=("nD",lambda s:(s>0).mean()),
   tag_any=("tags",lambda s:(s.map(len)>0).mean()),tag_D=("tagD",lambda s:(s>0).mean()),says_bipartisan=("bip",lambda s:(s>0).mean()),bip_tail_only=("bip_only_tail","mean"),year_missing=("year",lambda s:s.isna().mean()))
pd.set_option("display.width",250); print(g.round(2))
print("\nDemocrats named, by member:"); 
for who in sites:
    x=df[df.member==who]; print(" ",who,dict(collections.Counter(k for n in x.named for k,v in n.items() if v=="D").most_common(8)))
