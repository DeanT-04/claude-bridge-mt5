"""Autonomous YouTube discovery: keyless search (yt-dlp) + transcripts."""

import time
from collections.abc import Callable

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

from propquant.research.inbox import Inbox, Item, sources_config


def search(query: str, n: int) -> list[dict]:
    opts = {"quiet": True, "extract_flat": True, "skip_download": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(opts) as y:
        res = y.extract_info(f"ytsearch{n}:{query}", download=False) or {}
    return [e for e in res.get("entries", []) if e and e.get("id")]


def keep(entry: dict, cfg: dict) -> bool:
    """Quality prior: long enough to contain rules, short enough to not be a stream, watched."""
    dur, views = entry.get("duration") or 0, entry.get("view_count") or 0
    return cfg["min_seconds"] <= dur <= cfg["max_seconds"] and views >= cfg["min_views"]


def transcript(video_id: str) -> str:
    parts = YouTubeTranscriptApi().fetch(video_id, languages=["en", "en-US", "en-GB"])
    return " ".join(p.text for p in parts)


def collect(inbox: Inbox, limit: int | None = None, log: Callable = print) -> int:
    cfg = sources_config()["youtube"]
    cap = min(limit or cfg["daily_cap"], cfg["daily_cap"])
    added = 0
    for q in cfg["queries"]:
        try:
            found = search(q, cfg["per_query"])
        except Exception as ex:  # network / extractor hiccup: log and move on
            log(f"  search failed ({type(ex).__name__}): {q}")
            continue
        for e in found:
            if added >= cap:
                return added
            item_id = f"youtube:{e['id']}"
            if inbox.has(item_id) or not keep(e, cfg):
                continue
            try:
                text = transcript(e["id"])
            except Exception as ex:  # no captions, age-gated, blocked: skip, never fake
                log(f"  skip {e['id']}: {type(ex).__name__}")
                continue
            item = Item(
                id=item_id, kind="video", source="youtube",
                url=f"https://www.youtube.com/watch?v={e['id']}", title=e.get("title", ""),
                author=e.get("channel") or "", query=q,
                meta={"duration": e.get("duration"), "views": e.get("view_count")},
            )  # fmt: skip
            if inbox.add(item, text):
                added += 1
                log(f"  + {item.author}: {item.title[:70]}")
            time.sleep(cfg["pause_seconds"])
    return added
