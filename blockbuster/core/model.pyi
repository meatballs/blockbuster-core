import datetime as dt
from pathlib import Path
from typing import Any, Dict, List, Optional

class Task:
    description: str
    done: bool = ...
    priority: Optional[str] = ...
    completed_at: Optional[dt.date] = ...
    created_at: dt.date = ...
    projects: List[str] = ...
    contexts: List[str] = ...
    tags: Dict[str, str] = ...
    @classmethod
    def from_todotxt(cls, todotxt: str): ...
    def __init__(self) -> None: ...
    def __ne__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

class Event:
    event_type: str
    tasks: List[str]
    file: str
    prior_hash: str
    new_hash: str
    occurred_at: dt.datetime = ...
    def to_dict(self) -> Dict: ...
    def __init__(self) -> None: ...
    def __ne__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

class TaskList:
    file: Path
    tasks: List[Task]
    tasks_hash: str
    log: List[Event]
    @classmethod
    def from_file(cls, file: Path): ...
    def read_file(self) -> None: ...
    def add_tasks(self, additions: List[str]) -> Event: ...
    def delete_tasks(self, deletions: List[int]) -> Event: ...
    def update_tasks(self, updates: Dict[int, str]) -> Event: ...
