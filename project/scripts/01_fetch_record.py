"""Download the Congressional Record (House + Extensions of Remarks) for the 119th Congress.

    python scripts/01_fetch_record.py [MODS_CACHE_DIR]

Two public govinfo.gov addresses, no API key needed:
  metadata  https://www.govinfo.gov/metadata/pkg/CREC-YYYY-MM-DD/mods.xml   (list of items per day, ~3 MB each)
  text      https://www.govinfo.gov/content/pkg/CREC-YYYY-MM-DD/html/<item>.htm

The metadata files are large (about 530 MB in total), so they go to MODS_CACHE_DIR
(default: a folder in the system temp dir), not into the project. What the project keeps:
  data/raw/record_index.csv        one row per item: day, item id, section (H = House, E = Extensions)
  data/raw/record_html/<day>/*.htm the text of every item

Re-running skips files that already exist, so an interrupted run can be resumed.
"""
import collections
import csv
import datetime
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
HTML = os.path.join(RAW, "record_html")
MODS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(tempfile.gettempdir(), "crec_mods")
FIRST, LAST = datetime.date(2025, 1, 3), datetime.date(2026, 11, 10)   # 119th Congress up to the download date
UA = {"User-Agent": "course-project/0.1 (student research, DTU 02805)"}
WORKERS = 5          # keep it gentle


def fetch(url, tries=3):
    for _ in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return None


def get_mods(day):
    path = os.path.join(MODS, f"{day}.xml")
    if os.path.exists(path):
        return "have"
    b = fetch(f"https://www.govinfo.gov/metadata/pkg/CREC-{day}/mods.xml")
    if b is None or b"<mods" not in b[:2000]:
        return "no issue"            # weekends, recess: the site answers with an HTML page
    with open(path, "wb") as f:
        f.write(b)
    return "new"


def get_html(job):
    day, item = job
    path = os.path.join(HTML, day, item + ".htm")
    if os.path.exists(path):
        return "have"
    b = fetch(f"https://www.govinfo.gov/content/pkg/CREC-{day}/html/{item}.htm")
    if b is None:
        return "failed"
    with open(path, "wb") as f:
        f.write(b)
    return "new"


if __name__ == "__main__":
    os.makedirs(MODS, exist_ok=True)
    days = [FIRST + datetime.timedelta(n) for n in range((LAST - FIRST).days + 1)]
    with ThreadPoolExecutor(WORKERS) as ex:
        print("metadata:", dict(collections.Counter(ex.map(get_mods, days))))

    index = []
    for name in sorted(os.listdir(MODS)):
        day = name[:-4]
        text = open(os.path.join(MODS, name), encoding="utf8", errors="replace").read()
        items = sorted(set(re.findall(r'html/(CREC-%s-pt\d+-Pg[HE][^"<]*?)\.htm' % day, text)))
        index += [(day, it, "H" if "-PgH" in it else "E") for it in items]
        if items:
            os.makedirs(os.path.join(HTML, day), exist_ok=True)
    with open(os.path.join(RAW, "record_index.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day", "item", "section"])
        w.writerows(index)
    print("index:", len(index), "items on", len({d for d, _, _ in index}), "days")

    with ThreadPoolExecutor(WORKERS) as ex:
        print("text:", dict(collections.Counter(ex.map(get_html, [(d, it) for d, it, _ in index]))))
