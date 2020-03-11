from pathlib import Path

from blockbuster.core.model import Event

test_event_kwargs = {
    "event_type": "test event",
    "tasks": ["task one", "task two"],
    "file": Path("directory_name", "file_name"),
    "prior_hash": "prior hash",
    "new_hash": "new hash",
}


def test_events():
    event = Event(**test_event_kwargs)
    keys = list(test_event_kwargs.keys()) + ["occurred_at"]
    assert list(event.to_dict().keys()) == keys
