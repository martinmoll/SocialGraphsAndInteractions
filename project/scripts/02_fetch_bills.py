"""Download House bills of the 119th Congress and extract sponsors and cosponsors.

    python scripts/02_fetch_bills.py

Source: govinfo bulk data, one zip per bill type (public domain, no key):
  https://www.govinfo.gov/bulkdata/BILLSTATUS/119/<type>/BILLSTATUS-119-<type>.zip
Types: hr (bills), hjres (joint resolutions), hres (simple resolutions), hconres (concurrent resolutions).

Writes:
  data/processed/bills.parquet       one row per bill: bill_id, type, number, introduced, sponsor, policy_area, title, n_cosponsors
  data/processed/cosponsors.parquet  one row per (bill, cosponsor): bill_id, cosponsor, date, original, withdrawn
Members are identified by their Bioguide ID throughout.
"""
import os
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "billstatus")
OUT = os.path.join(ROOT, "data", "processed")
TYPES = ["hr", "hjres", "hres", "hconres"]


def text(node, path):
    found = node.find(path)
    return found.text if found is not None else None


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    bills, cos = [], []
    for t in TYPES:
        path = os.path.join(RAW, f"BILLSTATUS-119-{t}.zip")
        if not os.path.exists(path):
            url = f"https://www.govinfo.gov/bulkdata/BILLSTATUS/119/{t}/BILLSTATUS-119-{t}.zip"
            req = urllib.request.Request(url, headers={"User-Agent": "course-project/0.1"})
            with open(path, "wb") as f:
                f.write(urllib.request.urlopen(req, timeout=300).read())
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                bill = ET.fromstring(z.read(name)).find("bill")
                bill_id = f"{t}{text(bill, 'number')}"
                sponsor = text(bill, "sponsors/item/bioguideId")
                items = bill.findall("cosponsors/item")
                bills.append(dict(bill_id=bill_id, type=t, number=int(text(bill, "number")),
                                  introduced=text(bill, "introducedDate"), sponsor=sponsor,
                                  policy_area=text(bill, "policyArea/name"), title=text(bill, "title"),
                                  n_cosponsors=len(items)))
                for it in items:
                    cos.append(dict(bill_id=bill_id, cosponsor=text(it, "bioguideId"),
                                    date=text(it, "sponsorshipDate"),
                                    original=text(it, "isOriginalCosponsor") == "True",
                                    withdrawn=text(it, "sponsorshipWithdrawnDate") is not None))
    bills, cos = pd.DataFrame(bills), pd.DataFrame(cos)
    bills.to_parquet(os.path.join(OUT, "bills.parquet"), index=False)
    cos.to_parquet(os.path.join(OUT, "cosponsors.parquet"), index=False)
    print(bills.groupby("type").agg(bills=("bill_id", "size"), no_sponsor=("sponsor", lambda s: s.isna().sum()),
                                    cosponsor_links=("n_cosponsors", "sum"), max_cosponsors=("n_cosponsors", "max")))
    print("cosponsor rows:", len(cos), "| withdrawn:", int(cos.withdrawn.sum()), "| missing id:", int(cos.cosponsor.isna().sum()))
