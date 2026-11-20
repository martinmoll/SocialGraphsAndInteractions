"""A1: collect the full text and date of House members' press releases since 3 Jan 2025.

Run from project/ (one process; sites are fetched in parallel, each site one request at a time):

    python Anas/collector/collect.py --scope Anas/press_scope/scope_by_member.csv \
        --raw ../press_raw --out Anas/collector/parts --members B001323,L000599   # or --members all

Writes, per member, `parts/<bioguide>.parquet` (one row per release) and `parts/<bioguide>.log.csv` (every
fetch that failed, with its reason). `combine.py` joins the parts into `press_releases.parquet`.

Columns (the five agreed in WORK_AND_DEADLINES.md section 3, then provenance):
    bioguide, url, date, title, text,
    listing_url, layout, date_source, listing_dates, n_words, text_sha1, item_type, fetched_at

Rules (see README.md):
- Follows each site's robots.txt. One request at a time per site, DELAY seconds apart.
- A failed fetch is logged and retried once later; it never becomes an empty row.
- Raw pages are kept, gzipped, in --raw (outside the repo), so text can be re-extracted without refetching.
- Only the article body is kept as text: navigation, sidebars, "recent releases" boxes, sliders, share buttons
  and footers are removed, because they name other members and would create false mentions later.
- No name matching here. That is Martin's matcher (M1), in A3.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import html as htmlmod
import json
import os
import re
import sys
import threading
import time
import urllib.robotparser
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
DELAY = 0.5
MAX_BLOCKED = 4          # consecutive 403/429/503 or challenge pages before a host is left alone
SINCE = dt.date(2025, 1, 3)
TODAY = dt.date.today()
MON = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
DATE_TXT = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20\d\d)\b")
DATE_NUM = re.compile(r"\b(\d{1,2})/(\d{1,2})/(20\d\d)\b")
DATE_ISO = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)")

# Article containers, most specific first. Found by inspecting each site family (README, "Layouts").
BODY_SELECTORS = [
    ".evo-press-release__body", ".field--name-body", ".evo-page-content article",
    ".bodycopy", ".newsbody", ".main-newscopy",
    ".post-body", ".et_pb_post_content", ".entry-content", ".post-content", ".single-content",
    "#press", ".press-release", ".bodycontent", "article .content", "article", "#main_column", "main",
]
# Blocks inside a container that are not the release itself.
DROP = re.compile(r"related|recent|slider|share|social|sidebar|breadcrumb|pager|pagination|subscribe|newsletter|"
                  r"tags?\b|categor|nav|menu|footer|header|comment|print|signup|sign-up|widget|carousel", re.I)
# Wrappers that look like DROP but hold release text (audit of all kept releases, 20 Nov): emails pasted into the
# site (newsletterContent, subscriber-only, header-bar), Word (MsoCommentText), CKEditor embeds (cke_widget).
KEEP = re.compile(r"newsletter_?content|subscriber|header-bar|MsoComment|cke_widget", re.I)
ALWAYS_DROP = re.compile(r"related|recent|slider|carousel|share|social", re.I)


# ----------------------------------------------------------------------------------------------- fetching
class Site:
    """One host: robots.txt, a delay between requests, a failure log. Used by one thread at a time."""

    def __init__(self, base, raw):
        self.base, self.raw, self.last, self.fails = base, raw, 0.0, []
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.rp = urllib.robotparser.RobotFileParser()
        try:
            r = self.s.get(base + "/robots.txt", timeout=20)
            self.rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except requests.RequestException:
            self.rp.parse([])
        self.blocked = 0

    def get(self, url, tries=2, fresh=False):
        """Return (status, text). Release pages are read from the cache if present; listing pages (fresh=True)
        are always fetched again, so a later run sees new releases. Never returns an error page as text."""
        key = hashlib.sha1(url.encode()).hexdigest()
        path = os.path.join(self.raw, urlparse(url).netloc, key[:2], key + ".html.gz")
        if self.blocked >= MAX_BLOCKED:
            self.fails.append((url, "host gave up after repeated 403/429/503", 0))
            return None, None
        if os.path.exists(path) and not fresh:
            with gzip.open(path, "rt", encoding="utf-8") as f:
                return 200, f.read()
        if not self.rp.can_fetch(UA, url):
            self.fails.append((url, "robots.txt disallows", 0))
            return None, None
        for attempt in range(tries):
            wait = self.last + DELAY - time.time()
            if wait > 0:
                time.sleep(wait)
            try:
                r = self.s.get(url, timeout=30)
                self.last = time.time()
            except requests.RequestException as e:
                self.last = time.time()
                err = type(e).__name__
                time.sleep(3 * (attempt + 1))
                continue
            ttl = re.search(r"<title[^>]*>(.*?)</title>", r.text[:5000], re.I | re.S)
            # a block page announces itself in its title; "captcha" in a page body is usually a contact form
            challenge = bool(ttl and re.search(r"Attention Required|Just a moment|Access Denied|Request Rejected",
                                               ttl.group(1), re.I))
            if r.status_code == 200 and r.text and not challenge:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with gzip.open(path, "wt", encoding="utf-8") as f:
                    f.write(r.text)
                self.blocked = 0
                return 200, r.text
            err = "challenge page" if challenge else f"HTTP {r.status_code}"
            if challenge or r.status_code in (403, 429, 503):
                self.blocked += 1
                time.sleep(30 * (attempt + 1))
            elif r.status_code == 404:
                break
        self.fails.append((url, err, tries))
        return None, None


# ----------------------------------------------------------------------------------------------- parsing
def text_dates(t):
    out = []
    for m, d, y in DATE_TXT.findall(t):
        try:
            out.append(dt.date(int(y), MON[m[:3].lower()], int(d)))
        except ValueError:
            pass
    if not out:
        for a, b, y in DATE_NUM.findall(t):
            try:
                out.append(dt.date(int(y), int(a), int(b)))
            except ValueError:
                pass
    return [x for x in out if dt.date(2000, 1, 1) <= x <= TODAY]


def listing_dates(soup):
    """Dates shown on a listing page; dates far from the page's median (quoted in titles) are dropped."""
    for t in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        t.decompose()
    out = text_dates(soup.get_text(" "))
    if not out:
        out = [dt.date(*map(int, m)) for m in DATE_ISO.findall(str(soup)) if 2000 < int(m[0]) <= TODAY.year]
    if len(out) >= 3:
        med = sorted(out)[len(out) // 2]
        out = [x for x in out if abs((x - med).days) <= 400]
    return out


UUID_TAIL = re.compile(r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/?$", re.I)
NOT_RELEASE = re.compile(r"/(page|table|feed|rss)(/|$)")


def release_links(listing_url, soup):
    """Links on a listing page that point to single releases on the same site."""
    host, path = urlparse(listing_url).netloc, urlparse(listing_url).path.rstrip("/")
    seg = path.split("/")[-1] if path else ""        # WordPress: /category/press-releases/ lists /press-releases/<slug>/
    # links inside the listed posts of a WordPress category page (posts live at the site root, /<slug>/):
    # <article> (Brownley) or <div class="post"> (Clarke)
    in_post = {id(a) for art in soup.select("article, div.post") for a in art.find_all("a", href=True)} \
        if "/category/" in path else set()
    out, seen = [], set()
    for a in soup.find_all("a", href=True):
        full = urljoin(listing_url, htmlmod.unescape(a["href"])).split("#")[0]
        p = urlparse(full)
        if p.netloc != host:
            continue
        low = full.lower()
        ok = ("documentsingle.aspx" in low and "documentid=" in low) \
            or (p.path.rstrip("/") == path and re.search(r"(^|&)id=[\w-]{6,}", p.query, re.I)) \
            or (path and p.path.startswith(path + "/") and not p.query
                and not NOT_RELEASE.search(p.path) and p.path.rstrip("/") != path) \
            or (re.match(r"^/20\d\d/\d{1,2}/(\d{1,2}/)?[^/]+/?$", UUID_TAIL.sub("", p.path)) and not p.query) \
            or ("/category/" in path and seg and re.search(rf"/{re.escape(seg)}/[^/]+/?$", p.path)
                and "/category/" not in p.path and not p.query)
        # evo Drupal sites list /media/press-releases but link /media-center/press-releases/<slug> (Radewagen,
        # DeGette, Keating, Foster), /media/press-releases/<slug> (Crow) or /press-releases/<slug> (Scalise)
        # (also singular: Amo lists /press-releases but links /press-release/<slug>)
        if not ok and "press-release" in seg.lower() and not p.query and not NOT_RELEASE.search(p.path):
            ok = bool(re.search(r"/press[-_]releases?/[^/]+/?$", p.path, re.I))
        # (tested and rejected: any path inside a listed post picks up issue and newsletter pages, Jayapal,
        # Jeffries; Goodlander's one press release filed at /media/in-the-news/<slug>/ stays a known miss)
        if not ok and id(a) in in_post and not p.query and not NOT_RELEASE.search(p.path) \
                and re.fullmatch(r"/[^/]+/?", p.path) and not re.search(r"/(category|tag|author)/", p.path):
            ok = True
        # the same page linked as /News/ and /news/ (Cuellar), or as /2025/1/<slug> and /2025/1/<slug>/<uuid>
        key = UUID_TAIL.sub("", full.lower().rstrip("/")).rstrip("/")
        if ok and key not in seen:
            seen.add(key)
            out.append(full)
    return out


def link_dates(listing_url, soup, wanted):
    """The date shown next to each release link on a listing page: the nearest enclosing block (up to 5 levels)
    that holds exactly one distinct date. Blocks with several dates (a whole list) are ambiguous and skipped."""
    out = {}
    page = Counter(listing_dates(BeautifulSoup(str(soup), "lxml")))
    for a in soup.find_all("a", href=True):
        full = urljoin(listing_url, htmlmod.unescape(a["href"])).split("#")[0]
        if full not in wanted or full in out:
            continue
        for par in list(a.parents)[:5]:
            ds = set(text_dates(par.get_text(" ")))
            if len(ds) == 1:
                out[full] = ds.pop()
                break
            if len(ds) > 1:
                # an item whose title quotes a date ("September 11, 2001"): the one the page uses as an item date
                cand = [x for x in ds if page[x]]
                if len(cand) == 1:
                    out[full] = cand[0]
                break
    # guard (checked on 80 members: 722 of 733 agree with the release's own date within a day): a date must be one
    # the page shows as an item date, and may not be handed to more links than the page shows it (a sidebar date
    # attached to many items, McClain; "September 11, 2001" quoted in a title)
    used = Counter(out.values())
    return {l: d for l, d in out.items() if page[d] and used[d] <= page[d]}


def pager(listing, kind, offset):
    """URL of logical listing page n (0 = first) for each layout found by the scope scan."""
    sep = "&" if "?" in listing else "?"
    if kind == "wp":
        base = listing.rstrip("/")
        return lambda n: listing if n == 0 else f"{base}/page/{n + 1}/"
    if kind == "asp":
        return lambda n: f"{listing}{sep}Page={n + 1}"
    if kind == "drupal":
        return lambda n: f"{listing}{sep}page={n}"
    if kind == "drupal1":
        return lambda n: listing if n == 0 else f"{listing}{sep}page={n + offset}"
    if kind and kind.startswith("param:"):
        p = kind.split(":", 1)[1]
        return lambda n: f"{listing}{sep}{p}={n + 1}"
    return None


def parse_release(url, h):
    """Title, date (and where it came from), body text and item type of one release page."""
    soup = BeautifulSoup(h, "lxml")
    meta = {}
    for m in soup.find_all("meta"):
        k = (m.get("property") or m.get("name") or m.get("itemprop") or "").lower()
        if k and m.get("content"):
            meta.setdefault(k, m["content"].strip())
    title = meta.get("og:title") or ""
    site_name = meta.get("og:site_name") or ""
    generic = (not title or title == site_name or re.search(r"press releases?\s*(\||$)", title, re.I)
               or re.fullmatch(r"(U\.?S\.? )?(Congress(wo)?man|Rep(resentative)?\.?)\s+[\w.\s'-]{2,40}", title.strip(), re.I))
    GENERIC = re.compile(r"(press releases?|news|media center|(U\.?S\.? )?(Congress(wo)?man|Rep(resentative)?\.?)"
                         r"\s+[\w.\s'-]{2,40})", re.I)
    if generic:
        # the <title> tag (minus the site name after a dash or bar), then headings, skipping generic ones
        cands = []
        if soup.title and soup.title.get_text(strip=True):
            cands.append(re.split(r"\s+[–—|-]\s+(?=[^–—|-]*$)", soup.title.get_text(" ", strip=True))[0])
        cands += [x.get_text(" ", strip=True) for x in soup.find_all(["h1", "h2"])]
        cands = [x for x in cands if x and not GENERIC.fullmatch(x.strip())]
        title = cands[0] if cands else title
    title = re.sub(r"\s*[|–—]\s*(U\.?S\.? )?(Congress|Representative|Rep\.).*$", "", title).strip()

    # date: page metadata first, then <time>, then a date in the first part of the body
    date, src = None, None
    for k in ("article:published_time", "date", "dcterms.date", "datepublished", "dc.date"):
        if k in meta:
            m = DATE_ISO.search(meta[k])
            if m:
                date, src = dt.date(*map(int, m.groups())), "meta:" + k
                break

    for t in soup(["script", "style", "noscript", "form", "iframe", "svg", "button"]):
        t.decompose()
    for t in soup(["nav", "footer", "header", "aside"]):
        # some themes wrap the whole page in <header> (Kiggans): keep a block that holds the main content
        if not t.decomposed and not t.find(["main", "article"]) and len(t.get_text(" ", strip=True).split()) < 300:
            t.decompose()
    body = None
    for sel in BODY_SELECTORS:
        cands = [c for c in soup.select(sel) if len(c.get_text(" ", strip=True).split()) >= 25]
        if cands:
            body, used = max(cands, key=lambda c: len(c.get_text(" ", strip=True))), sel
            break
    if body is None:
        return dict(title=title, date=date, date_source=src, text=None, selector=None)
    drop = []
    body_words = len(body.get_text(" ", strip=True).split())
    for el in body.find_all(True):
        ident = " ".join(el.get("class", []) or []) + " " + (el.get("id") or "")
        n = len(el.get_text(" ", strip=True).split())
        # a block holding most of the body is the release itself, whatever its class says (Boebert's
        # "header-bar", Hoyer's "x_newsletterContent"); text pasted from Word or an email keeps its wrappers
        # ...but a slider or "related posts" block is never the release, however large (McBath, Neal, Whitesides:
        # posts with no text of their own, where only the slider of other posts is left)
        if ident.strip() and DROP.search(ident) and not KEEP.search(ident) and n < 400 \
                and (n < 0.5 * body_words or ALWAYS_DROP.search(ident)):
            drop.append(el)
    for el in drop:                                   # outermost first; children of a dropped block go with it
        if not any(p in drop for p in el.parents):
            el.decompose()
    if date is None:
        # a <time> outside the article is the template's, not the release's (Latta: 13 Nov 2017 on every page)
        tm, tsrc = (body.find("time"), "time") if body.find("time") is not None else (soup.find("time"), "page time")
        if tm is not None:
            m = DATE_ISO.search(tm.get("datetime") or "") or None
            if m:
                date, src = dt.date(*map(int, m.groups())), tsrc
            else:
                d = text_dates(tm.get_text(" "))
                if d:
                    date, src = d[0], tsrc
    if date is None:                                  # a visible date label, e.g. <span class="date"> (Steube)
        for el in body.select('[class*="date"], [class*="Date"]')[:3] + soup.select('[class*="date"]')[:3]:
            d = text_dates(el.get_text(" "))
            if d:
                date, src = d[0], "date element"
                break
    paras = [p.get_text(" ", strip=True) for p in body.find_all(["p", "li", "h2", "h3", "h4", "blockquote"])
             if not p.find_parent(["li", "blockquote"]) or p.name in ("li", "blockquote")]
    full = body.get_text("\n", strip=True)
    joined = "\n".join(x for x in paras if x)
    # paragraphs miss text kept in plain <div>s on some sites (Correa): then take the whole container
    text = joined if len(joined) >= 0.6 * len(full) else full
    text = re.sub(r"[ \t ]+", " ", text).strip()
    if date is None:
        m = re.search(r"/(20\d\d)/(\d{1,2})/(\d{1,2})/", urlparse(url).path)
        if m:
            try:
                date, src = dt.date(*map(int, m.groups())), "url"
            except ValueError:
                pass
    if date is None:
        d = text_dates(text[:400])
        if d:
            date, src = d[0], "body text"
    if title and text.startswith(title):
        text = text[len(title):].lstrip()
    return dict(title=title, date=date, date_source=src, text=text, selector=used)


def fetch_release(site, b, l, listing, kind):
    """Fetch and parse one release. None = fetch failed (logged); "no body" = page without an article."""
    st, h = site.get(l)
    if h is None:
        return None
    r = parse_release(l, h)
    if not r["text"]:
        site.fails.append((l, "no article body found", 0))
        return "no body"
    return dict(bioguide=b, url=l, date=r["date"], title=r["title"], text=r["text"],
                listing_url=listing, layout=kind, date_source=r["date_source"],
                body_selector=r["selector"], n_words=len(r["text"].split()),
                text_sha1=hashlib.sha1(re.sub(r"\W+", " ", r["text"].lower()).encode()).hexdigest(),
                item_type=item_type(l, r["title"]), fetched_at=dt.datetime.now().isoformat(timespec="seconds"))


def rediscover(site, host):
    """Find a press-release listing on the homepage, as the scope scan did (probe1.py)."""
    st, h = site.get(host + "/")
    if h is None:
        return None
    for a in BeautifulSoup(h, "lxml").find_all("a", href=True):
        full = urljoin(host + "/", a["href"])
        if urlparse(full).netloc == urlparse(host).netloc and re.search(r"press[-_ ]?releases?", full, re.I):
            return full
    return None


def item_type(url, title):
    s = (url + " " + (title or "")).lower()
    if re.search(r"\b(on|joins|appears on|interview|msnbc|ms-now|cnn|fox|cbs|abc|nbc|npr)\b.*\b(interview|show|news|now)\b|"
                 r"/(in-the-news|media-appearances?|interviews?)/", s):
        return "media"
    if re.search(r"op-?ed|column|opinion", s):
        return "op-ed"
    if re.search(r"statement", s):
        return "statement"
    if re.search(r"newsletter|e-?news", s):
        return "newsletter"
    if re.search(r"video|photo|in the news|media appearance", s):
        return "media"
    return "press release"


# ----------------------------------------------------------------------------------------------- members
def collect_member(row, raw, out, limit=None):
    b, listing, kind = row["bioguide"], row["listing"], row["kind"]
    host = urlparse(listing).scheme + "://" + urlparse(listing).netloc
    site = Site(host, raw)
    rows, seen_pages = [], []
    url_of = pager(listing, kind, int(row.get("offset", 1) or 1))
    max_pages = int(row["boundary_page"]) + 4 if pd.notna(row.get("boundary_page")) else 200
    links, stop, failed = [], None, []
    n = 0
    while True:
        u = listing if n == 0 or url_of is None else url_of(n)
        st, h = site.get(u, fresh=True)
        if h is None and n == 0:
            # the site changed since the scope scan (Lynch moved to WordPress): find the listing again
            new = rediscover(site, host)
            if new and new != listing:
                site.fails.append((listing, f"listing moved to {new}", 0))
                listing, kind = new, ("wp" if "/category/" in new else kind)
                url_of = pager(listing, kind, 1)
                continue
        if h is None and n > 0 and site.fails and site.fails[-1][1] == "HTTP 404":
            # a WordPress listing answers 404 past its last page (Baumgartner, page 11): the listing has ended
            stop = "listing ended (404 past last page)"
            break
        if h is None:
            stop = "listing fetch failed"
            break
        soup = BeautifulSoup(h, "lxml")
        new = [l for l in release_links(listing, soup) if l not in links]
        ds = listing_dates(BeautifulSoup(h, "lxml"))
        # nothing new, or the site repeats a page. A "repeat" needs a real page of dates: Jeffries' pages show only
        # two fixed sidebar dates, identical on every page, which cut his walk at 10 of 709 releases
        if not new or (len(ds) >= 5 and ds in seen_pages):
            stop = "no new links" if n > 0 else "no links on the first page"
            break
        seen_pages.append(ds)
        links += new
        page_dates = []
        shown = link_dates(listing, soup, set(new))
        for l in new[: (limit - len(rows)) if limit else None]:
            r = fetch_release(site, b, l, listing, kind)
            if r is None:
                failed.append((l, site.fails[-1][1] if site.fails else ""))
            elif r == "no body":
                pass
            else:
                # a release page without a date of its own, or with only a date quoted in its text, takes the date
                # shown next to its link on the listing (Latta: quoted 2023 dates dropped 6 of 20 releases)
                # (also over <time> and date labels: the listing agrees with page metadata for 717 of 718 links)
                if r["date_source"] in (None, "body text", "page time", "time", "date element") and l in shown:
                    r["date"], r["date_source"] = shown[l], "listing"
                if r["date"] is not None:
                    page_dates.append(r["date"])
                if r["date"] is None or r["date"] >= SINCE:
                    rows.append(r)
        if url_of is None:
            stop = "single page (no pager)"
            break
        # a real page of listing dates decides the cut-off on its own; release dates only when the listing has none
        # (Latta: one misdated release on page 2 ended the walk at 14 of about 110)
        if (max(ds) < SINCE) if len(ds) >= 5 else (page_dates and max(page_dates) < SINCE):
            stop = "reached cutoff"
            break
        if limit and len(links) >= limit:
            stop = "test limit"
            break
        if n + 1 >= max_pages:
            stop = "page cap"
            break
        n += 1
    # A 404 means the site itself has no such page: refetching cannot help, so it does not keep the member
    # incomplete. It is logged and counted (missing_at_source). Most are links the site cut short
    # ("...tribute-to-", Harder, Courtney) whose full link was collected; the rest are dead links (Wittman,
    # DocumentID=6798). Connection errors and timeouts still count as failures and are retried by --skip-done.
    got = {r["url"] for r in rows}
    # a redirect loop (Goodlander: TooManyRedirects on 2 releases) is just as permanent on the site's side
    gone = [u for u, why in failed if why in ("HTTP 404", "TooManyRedirects")]
    missing_at_source = 0
    for u in gone:
        cut = any(o != u and o.startswith(u) and o in got for o in links)
        missing_at_source += not cut
        site.fails.append((u, "cut-short link; full link collected" if cut else "dead link on the site (404 or redirect loop)", 0))
    failed_releases = len(failed) - len(gone)
    # a release collected by an earlier run, dated in the window, that the listing no longer shows is kept and
    # flagged listed=False: sites unlist releases whose pages stay online (Obernolte: 2 releases of March-April 2026
    # left his listing on 20 Nov). Undated earlier rows are not carried over (Espaillat's turned out to be 2024)
    for r in rows:
        r["listed"] = True
    prev_parquet = os.path.join(out, f"{b}.parquet")
    if os.path.exists(prev_parquet):
        prev_rows = pd.read_parquet(prev_parquet)
        if len(prev_rows) and "date" in prev_rows:
            keep = prev_rows[~prev_rows.url.isin(got) & prev_rows.date.notna()]
            keep = keep[keep.date.map(lambda d: d >= SINCE)]
            for r in keep.to_dict("records"):
                r["listed"] = False
                rows.append(r)
    df = pd.DataFrame(rows)
    os.makedirs(out, exist_ok=True)
    complete = stop in ("reached cutoff", "no new links", "single page (no pager)",
                        "listing ended (404 past last page)") and failed_releases == 0
    old = os.path.join(out, f"{b}.status.json")
    prev = json.load(open(old)) if os.path.exists(old) else {}
    if prev.get("complete") and not complete and prev.get("releases", 0) >= len(df):
        # never replace a complete earlier result with a worse one (a site that failed today); but a run that
        # found more releases always wins (Goodlander: an earlier "complete" 15 against a new 357)
        site.fails.append((listing, f"run incomplete ({stop}); kept the earlier complete result", 0))
        pd.DataFrame(site.fails, columns=["url", "reason", "tries"]).assign(bioguide=b).to_csv(
            os.path.join(out, f"{b}.retry.log.csv"), index=False)
        return b, len(links), len(df), len(site.fails), 0, stop + " (earlier result kept)", False
    df.to_parquet(os.path.join(out, f"{b}.parquet"), index=False)
    pd.DataFrame(site.fails, columns=["url", "reason", "tries"]).assign(bioguide=b).to_csv(
        os.path.join(out, f"{b}.log.csv"), index=False)
    status = dict(bioguide=b, listing=listing, layout=kind, stop=stop, pages=n + 1, links=len(links),
                  releases=len(df), failed_releases=failed_releases, missing_at_source=missing_at_source,
                  complete=complete,
                  finished_at=dt.datetime.now().isoformat(timespec="seconds"))
    json.dump(status, open(os.path.join(out, f"{b}.status.json"), "w"))
    return b, len(links), len(df), len(site.fails), int(df.date.isna().sum()) if len(df) else 0, stop, complete


def safe_collect(row, raw, out, limit):
    """One member's failure (an unexpected page, a parse error) must not stop the others."""
    try:
        return collect_member(row, raw, out, limit)
    except Exception as e:
        b = row["bioguide"]
        os.makedirs(out, exist_ok=True)
        json.dump(dict(bioguide=b, stop=f"exception: {type(e).__name__}: {e}"[:300], complete=False),
                  open(os.path.join(out, f"{b}.status.json"), "w"))
        return b, 0, 0, 0, 0, f"exception: {type(e).__name__}", False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--members", default="all")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--skip-done", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="releases per member (testing only)")
    a = ap.parse_args()
    sc = pd.read_csv(a.scope)
    sc = sc[sc.status == "ok"]
    d = os.path.dirname(a.scope)                     # the scan's paging results: how deep each listing goes
    pages = {x["bioguide"]: x.get("boundary_page") for f in ("stage2b.json", "guess2.json")
             for x in json.load(open(os.path.join(d, f))) if x.get("status") == "ok"}
    sc["boundary_page"] = sc.bioguide.map(pages)
    extra = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra_listings.csv"))
    # listings the scan missed, or got wrong (Brownley pages with ?paged=N): an extra row replaces the scan's row
    sc = pd.concat([sc, extra.assign(status="ok")], ignore_index=True).drop_duplicates("bioguide", keep="last")
    if a.members != "all":
        sc = sc[sc.bioguide.isin(a.members.split(","))]

    def done(b):                                     # skip only members whose last run was complete
        f = os.path.join(a.out, f"{b}.status.json")
        return os.path.exists(f) and json.load(open(f)).get("complete") is True
    if a.skip_done:
        sc = sc[~sc.bioguide.map(done)]
    todo = sc.to_dict("records")
    print(f"{len(todo)} members", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(a.threads) as ex:
        for b, nl, nr, nf, nd, stop, ok in ex.map(lambda r: safe_collect(r, a.raw, a.out, a.limit), todo):
            print(f"{b}: links {nl}, releases kept {nr}, failures {nf}, no date {nd}, stop: {stop}, "
                  f"complete: {ok}  [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
