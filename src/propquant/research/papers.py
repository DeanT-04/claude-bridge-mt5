"""Keyless paper discovery: arXiv API and OpenAlex (open-access PDFs where available)."""

import io
import time
from collections.abc import Callable

import feedparser
import httpx
from pypdf import PdfReader

from propquant.research.inbox import Inbox, Item, sources_config

HEADERS = {"User-Agent": "propquant-research/0.1 (personal, non-commercial research)"}


def pdf_text(client: httpx.Client, url: str, max_pages: int = 40) -> str:
    try:
        r = client.get(url, headers=HEADERS, timeout=60, follow_redirects=True)
        if r.status_code != 200 or b"%PDF" not in r.content[:1024]:
            return ""
        reader = PdfReader(io.BytesIO(r.content))
        return "\n".join((p.extract_text() or "") for p in reader.pages[:max_pages])
    except Exception:
        return ""


def arxiv(inbox: Inbox, client: httpx.Client, log: Callable) -> int:
    cfg = sources_config()["papers"]["arxiv"]
    added = 0
    for q in cfg["queries"]:
        try:
            r = client.get(
                "https://export.arxiv.org/api/query",
                params={"search_query": q, "max_results": cfg["max_results"],
                        "sortBy": "relevance"},
                timeout=60, follow_redirects=True,
            )  # fmt: skip
        except httpx.HTTPError as ex:
            log(f"  arXiv query failed ({type(ex).__name__}): {q}")
            continue
        for e in feedparser.parse(r.text).entries:
            aid = e.id.rsplit("/", 1)[-1]
            item_id = f"arxiv:{aid.split('v')[0]}"
            if inbox.has(item_id):
                continue
            pdf = next((lk.href for lk in e.links if lk.get("type") == "application/pdf"), "")
            body = pdf_text(client, pdf) if pdf else ""
            text = f"{e.title}\n\n{e.summary}\n\n{body}"
            item = Item(
                id=item_id, kind="paper", source="arxiv", url=e.link, title=e.title.strip(),
                author=", ".join(a.name for a in e.get("authors", []))[:300],
                published=e.get("published", ""), query=q,
                meta={"full_text": bool(body)},
            )  # fmt: skip
            if inbox.add(item, text):
                added += 1
                log(f"  + arXiv {item.published[:4]}: {item.title[:70]}")
            time.sleep(3)  # arXiv API etiquette
    return added


def _abstract(inv: dict | None) -> str:
    if not inv:
        return ""
    words = sorted((pos, w) for w, ps in inv.items() for pos in ps)
    return " ".join(w for _, w in words)


def openalex(inbox: Inbox, client: httpx.Client, log: Callable) -> int:
    cfg = sources_config()["papers"]["openalex"]
    added = 0
    for q in cfg["queries"]:
        try:
            r = client.get(
                "https://api.openalex.org/works",
                params={"search": q, "per_page": cfg["per_page"], "filter": "is_oa:true"},
                headers=HEADERS, timeout=60,
            )  # fmt: skip
            results = r.json().get("results", [])
        except (httpx.HTTPError, ValueError) as ex:
            log(f"  OpenAlex query failed ({type(ex).__name__}): {q}")
            continue
        for w in results:
            item_id = f"openalex:{w['id'].rsplit('/', 1)[-1]}"
            if inbox.has(item_id):
                continue
            loc = w.get("best_oa_location") or {}
            body = pdf_text(client, loc["pdf_url"]) if loc.get("pdf_url") else ""
            text = (
                f"{w.get('title', '')}\n\n{_abstract(w.get('abstract_inverted_index'))}\n\n{body}"
            )
            item = Item(
                id=item_id, kind="paper", source="openalex",
                url=w.get("doi") or loc.get("landing_page_url") or w["id"],
                title=(w.get("title") or "").strip(),
                author=", ".join(a["author"]["display_name"]
                                 for a in w.get("authorships", [])[:6]),
                published=str(w.get("publication_year", "")), query=q,
                meta={"cited_by": w.get("cited_by_count"), "full_text": bool(body)},
            )  # fmt: skip
            if inbox.add(item, text):
                added += 1
                log(f"  + OpenAlex {item.published}: {item.title[:70]}")
            time.sleep(1)
    return added


def collect(inbox: Inbox, log: Callable = print) -> int:
    with httpx.Client() as client:
        return arxiv(inbox, client, log) + openalex(inbox, client, log)
