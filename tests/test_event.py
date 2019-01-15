from pathlib import Path

from blockbuster.core.model import TasksAdded, TasksDeleted, TasksUpdated

test_event_kwargs = {
    "tasks": ["task one", "task two"],
    "file": Path("directory_name", "file_name"),
    "prior_hash": "prior hash",
    "new_hash": "new hash",
}


def test_events():
    for event_class in [TasksAdded, TasksDeleted, TasksUpdated]:
        event = event_class(**test_event_kwargs)
        deserialised = eval(str(event))
        keys = ["event_type", "occurred_at", "tasks", "file", "prior_hash", "new_hash"]
        assert isinstance(deserialised, dict)
        for key in keys:
            assert key in deserialised
            assert key in event.to_dict()
