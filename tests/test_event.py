from pathlib import Path

from blockbuster.core.model import Event

TEST_EVENT_KWARGS = {
    "event_type": "test event",
    "file": Path("directory_name", "file_name"),
    "prior_hash": "prior hash",
    "new_hash": "new hash",
    "tasks": ["task one", "task two"],
}


def test_events():
    event = Event(**TEST_EVENT_KWARGS)
    keys = list(TEST_EVENT_KWARGS.keys()) + ["occurred_at"]
    assert list(event.to_dict().keys()) == keys
