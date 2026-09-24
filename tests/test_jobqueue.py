import pytest

from registry import db
from research import jobqueue


@pytest.fixture
def con(tmp_path):
    return db.connect(tmp_path / "r.sqlite")


def test_enqueue_dedupes_and_respects_redo(con):
    assert jobqueue.enqueue(["donchian", "orb"], ["EURUSD"], ["H1"], con=con) == 2
    assert jobqueue.enqueue(["donchian"], ["EURUSD"], ["H1"], con=con) == 0
    job = jobqueue._claim(con)
    con.execute("UPDATE jobs SET status='done' WHERE id=?", (job["id"],))
    assert jobqueue.enqueue([job["family"]], ["EURUSD"], ["H1"], con=con) == 0
    assert jobqueue.enqueue([job["family"]], ["EURUSD"], ["H1"], redo=True, con=con) == 1


def test_claim_is_fifo_and_exhausts(con):
    jobqueue.enqueue(["donchian", "orb"], ["EURUSD"], ["H1"], con=con)
    a, b = jobqueue._claim(con), jobqueue._claim(con)
    assert (a["family"], b["family"]) == ("donchian", "orb") and a["status"] == "running"
    assert jobqueue._claim(con) is None
    assert jobqueue.status(con)["jobs"] == {"running": 2}


def test_unknown_family_rejected(con):
    with pytest.raises(ValueError):
        jobqueue.enqueue(["nope"], ["EURUSD"], ["H1"], con=con)
