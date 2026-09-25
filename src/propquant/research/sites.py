"""Strategy-site articles: Oxford Strat (sitemap, robots-checked) and Quantified Strategies
(public Internet Archive captures, because the live site answers bots with a verification page
that we do not try to get past)."""

import re
import time
import urllib.robotparser
from collections.abc import Callable

import httpx
import trafilatura

from propquant.research.inbox import Inbox, Item, sources_config

UA = "Mozilla/5.0 (compatible; propquant-research/0.1; personal non-commercial research)"
LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


def relevant(url: str, keywords: list[str]) -> bool:
    slug = url.lower().rstrip("/").rsplit("/", 1)[-1]
    return any(k in slug for k in keywords)


def extract(html: str) -> tuple[str, str]:
    """(title, main text) of an article page."""
    text = trafilatura.extract(html, include_tables=True, favor_recall=True) or ""
    meta = trafilatura.extract_metadata(html)
    return (meta.title if meta and meta.title else ""), text


def _robots(client: httpx.Client, base: str) -> urllib.robotparser.RobotFileParser | None:
    """Parsed robots.txt, or None if it can't be read (then we don't crawl at all)."""
    for attempt in range(4):
        try:
            r = client.get(base + "/robots.txt", headers={"User-Agent": UA}, timeout=60,
                           follow_redirects=True)  # fmt: skip
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            return rp
        except httpx.HTTPError:
            time.sleep(5 * (attempt + 1))
    return None


def _get(client: httpx.Client, url: str, **kw) -> httpx.Response | None:
    for attempt in range(3):
        try:
            return client.get(url, follow_redirects=True, **kw)
        except httpx.HTTPError:
            time.sleep(5 * (attempt + 1))
    return None


def oxfordstrat(inbox: Inbox, client: httpx.Client, log: Callable, limit: int) -> int:
    cfg = sources_config()["sites"]
    rp = _robots(client, "https://oxfordstrat.com")
    sm = _get(client, cfg["oxfordstrat"]["sitemap"], headers={"User-Agent": UA}, timeout=60)
    if rp is None or sm is None:
        log("  oxfordstrat: robots.txt or sitemap unreachable, skipped (not crawling blind)")
        return 0
    xml = sm.text
    urls = [u for u in LOC.findall(xml) if relevant(u, cfg["keywords"])]
    added = 0
    for u in urls:
        if added >= limit:
            break
        item_id = f"oxfordstrat:{u.rstrip('/').rsplit('/', 1)[-1]}"
        if inbox.has(item_id) or not rp.can_fetch(UA, u):
            continue
        r = _get(client, u, headers={"User-Agent": UA}, timeout=60)
        if r is None:
            continue
        title, text = extract(r.text)
        if r.status_code == 200 and len(text) > 500:
            if inbox.add(Item(id=item_id, kind="article", source="oxfordstrat", url=u,
                              title=title), text):  # fmt: skip
                added += 1
                log(f"  + Oxford Strat: {title[:70]}")
        time.sleep(cfg["pause_seconds"])
    return added


def quantifiedstrategies(inbox: Inbox, client: httpx.Client, log: Callable, limit: int) -> int:
    cfg = sources_config()["sites"]
    qs = cfg["quantifiedstrategies"]
    resp = _get(
        client,
        "https://web.archive.org/cdx/search/cdx",
        params={"url": f"{qs['domain']}/*", "output": "json", "fl": "timestamp,original",
                "filter": ["statuscode:200", "mimetype:text/html"], "collapse": "urlkey",
                "limit": "20000"},
        timeout=120,
    )  # fmt: skip
    if resp is None or resp.status_code != 200:
        log("  quantifiedstrategies: archive index unreachable, skipped")
        return 0
    cdx = resp.json()[1:]
    latest: dict[str, str] = {}
    for ts, url in cdx:
        u = re.sub(r"^https?://(www\.)?", "https://www.", url.split("?")[0]).replace(":80", "")
        if relevant(u, cfg["keywords"]) and ts > latest.get(u, ""):
            latest[u] = ts
    added = 0
    for u, ts in sorted(latest.items()):
        if added >= min(limit, qs["max_articles"]):
            break
        item_id = f"quantifiedstrategies:{u.rstrip('/').rsplit('/', 1)[-1]}"
        if inbox.has(item_id):
            continue
        try:
            r = client.get(f"https://web.archive.org/web/{ts}id_/{u}", timeout=90,
                           follow_redirects=True)  # fmt: skip
        except httpx.HTTPError:
            time.sleep(10)
            continue
        title, text = extract(r.text)
        if r.status_code == 200 and len(text) > 500:
            item = Item(id=item_id, kind="article", source="quantifiedstrategies", url=u,
                        title=title, meta={"archive_capture": ts})  # fmt: skip
            if inbox.add(item, text):
                added += 1
                log(f"  + Quantified Strategies: {title[:70]}")
        time.sleep(cfg["pause_seconds"] + 2)  # archive.org rate limits aggressively
    return added


def collect(inbox: Inbox, log: Callable = print, limit: int = 100) -> int:
    with httpx.Client() as client:
        return oxfordstrat(inbox, client, log, limit) + quantifiedstrategies(
            inbox, client, log, limit
        )
