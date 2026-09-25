from propquant.research import papers, sites, youtube
from propquant.research.inbox import Inbox, Item


def test_inbox_dedupes_and_tracks_status(tmp_path) -> None:
    ib = Inbox(tmp_path)
    it = Item(id="youtube:abc", kind="video", source="youtube", url="u", title="ORB")
    assert ib.add(it, "hello world")
    assert not ib.add(it, "again")  # duplicates are ignored
    assert ib.text("youtube:abc") == "hello world"
    ib.set_status("youtube:abc", "read")
    assert ib.listing("new") == [] and len(ib.listing("read")) == 1
    ib.close()


def test_site_relevance_uses_slug() -> None:
    kw = ["strateg", "backtest"]
    assert sites.relevant("https://x.com/opening-range-strategy/", kw)
    assert not sites.relevant("https://x.com/strategy-category/best-etfs/", kw)


def test_youtube_quality_prior() -> None:
    cfg = {"min_seconds": 240, "max_seconds": 4200, "min_views": 2000}
    assert youtube.keep({"duration": 600, "view_count": 5000}, cfg)
    assert not youtube.keep({"duration": 60, "view_count": 5000}, cfg)  # a short
    assert not youtube.keep({"duration": 600, "view_count": 10}, cfg)


def test_openalex_abstract_rebuild() -> None:
    inv = {"Intraday": [0], "momentum": [1], "exists": [2]}
    assert papers._abstract(inv) == "Intraday momentum exists"


def test_inbox_survives_bad_pdf_characters(tmp_path) -> None:
    bad = chr(0xDC99)  # lone surrogate, as produced by some PDF text extraction
    ib = Inbox(tmp_path)
    it = Item(id="arxiv:1", kind="paper", source="arxiv", url="u", title="t" + bad)
    assert ib.add(it, "abc" + bad + "def")
    assert ib.text("arxiv:1") == "abc?def"
    ib.close()
