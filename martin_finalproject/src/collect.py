"""Collect works from OpenAlex. Usage: python src/collect.py [FIELD] [N]
Raw pages go to data/raw/ (read-only after saving), with query + date in the filename/meta.
The API key (optional) is read from OPENALEX_API_KEY and never written anywhere.
"""
import datetime
import json
import os
import pathlib
import sys
import time

import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

# --- the one place the field is defined: change this to change the field ---
FIELD = "energy_systems"
FILTERS = {  # one entry per field tried, so every raw file stays reproducible
    "energy_systems": 'title_and_abstract.search:"energy system",publication_year:2015-2024,type:article',
    # CHOICE: OpenAlex subfield 1910 (Oceanography), not a phrase search: "ocean science" matches only 1,145 works
    "ocean_science": "primary_topic.subfield.id:1910,publication_year:2015-2024,type:article",
    # CHOICE: a list = stratified sample, N/len(list) most-cited works per stratum. One stratum per OpenAlex field
    # with > 2,000 matching works (Energy, Engineering, Environmental Sci., Economics, Social Sci.), so no field
    # crowds out the others; the between-field question needs every field well represented.
    "energy_transition": [f'title_and_abstract.search:"energy transition",publication_year:2015-2024,type:article,'
                          f'primary_topic.field.id:{f}' for f in (21, 22, 23, 20, 33)],
}
SORT = "cited_by_count:desc"  # CHOICE: most-cited first -> dense sample, biased to older/review papers
SELECT = ("id,doi,title,publication_year,type,cited_by_count,referenced_works,"
          "primary_topic,topics,abstract_inverted_index")


def fetch(flt, n, key):
    params = {"filter": flt, "sort": SORT, "select": SELECT, "per_page": 100, "page": 1}
    works = []
    while len(works) < n:  # page paging: works keyless, caps at 10,000 results (cursor paging needs a key)
        r = requests.get("https://api.openalex.org/works",
                         params={**params, **({"api_key": key} if key else {})}, timeout=60)
        r.raise_for_status()
        page = r.json()
        works += page["results"]
        params["page"] += 1
        if not page["results"]:
            break
        print(f"{len(works)} works, budget left ${r.headers.get('X-RateLimit-Remaining-USD')}", flush=True)
        time.sleep(0.3)
    return works[:n], page["meta"]["count"]


def main(field, n):
    RAW.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    key = os.environ.get("OPENALEX_API_KEY")
    strata = FILTERS[field] if isinstance(FILTERS[field], list) else [FILTERS[field]]
    works, total = [], []
    for flt in strata:
        w, t = fetch(flt, n // len(strata), key)
        works += w
        total.append(t)
    out = RAW / f"openalex_{field}_{today}_n{len(works)}.json"
    out.write_text(json.dumps({"query": {"filter": strata if len(strata) > 1 else strata[0], "sort": SORT,
                                         "select": SELECT, "per_page": 100},
                               "date": today, "total_matching": total if len(strata) > 1 else total[0],
                               "works": works}), encoding="utf-8")
    print("saved", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else FIELD, int(sys.argv[2]) if len(sys.argv) > 2 else 3000)
