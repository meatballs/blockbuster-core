from typing import Iterable
from pathlib import Path

def read_tasks(file: Path): ...
def add_tasks(additions: Iterable[str], file: Path): ...
def delete_tasks(deletions: Iterable[str], file: Path): ...
def update_tasks(updates: Iterable[str], file: Path): ...
