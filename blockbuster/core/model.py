import datetime as dt
from hashlib import sha256
from pathlib import Path
from typing import Dict, List, Optional

import attr
import blockbuster.core.io as io
import blockbuster.core.parser as parser
from blockbuster.core import (
    DATE_FORMAT,
    FILE_READ,
    TASKS_ADDED,
    TASKS_DELETED,
    TASKS_UPDATED,
)


@attr.s(auto_attribs=True, slots=True)
class Task:
    """A class to represent a task

    Attributes
    ----------
    description:
        Text to describe the task
    done:
        True if the task has been completed
    priority:
        By convention, a single upper case character to indicate priority level
    completed_at:
        The date on which the task was completed
    created_at:
        The date on which the task was created
    projects:
        A list of project tags (denoted by a + prefix in the text definition)
    contexts:
        A list of context tags (denoted by a @ prefix in the text definition)
    tags:
        A dict of user defined tag keys and values
    """

    description: str
    done: bool = False
    priority: Optional[str] = None
    completed_at: Optional[dt.date] = None
    created_at: dt.date = dt.datetime.now().date()
    projects: List[str] = attr.Factory(list)
    contexts: List[str] = attr.Factory(list)
    tags: Dict = attr.Factory(dict)

    @classmethod
    def from_todotxt(cls, todotxt):
        """Create a Task instance from a string in todo.txt format"""
        return cls(**parser.parse(todotxt))

    def __str__(self):
        optional_prefixes = ""
        minimal_text = f"{self.created_at.strftime(DATE_FORMAT)} {self.description}"
        optional_suffixes = ""

        if self.done:
            optional_prefixes += "x "

        if self.priority:
            optional_prefixes += f"({self.priority}) "

        if self.completed_at:
            optional_prefixes += f"{self.completed_at.strftime(DATE_FORMAT)} "

        for project in self.projects:
            if project:
                optional_suffixes += f" +{project}"

        for context in self.contexts:
            if context:
                optional_suffixes += f" @{context}"

        for key, value in self.tags.items():  # pylint: disable=no-member
            optional_suffixes += f" {key}:{value}"

        return optional_prefixes + minimal_text + optional_suffixes


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Event:
    event_type: str
    file: str
    prior_hash: str
    new_hash: str
    tasks: List[str] = attr.Factory(list)
    occurred_at: dt.datetime = dt.datetime.now()

    def to_dict(self):
        return attr.asdict(self)


def _tasks_hash(tasks):
    return sha256("\n".join(tasks).encode("UTF-8")).hexdigest()


@attr.s(auto_attribs=True, slots=True)
class TaskList:
    """A class to represent a todo.txt file and its contents

    Attributes
    ----------
    file : pathlib.Path
        the todo.txt file
    tasks :  list or tuple
        of Task instances representing the file contents
    tasks_hash : str
        sha256 hash of the tasks content
    log : List
        of Event instances
    """

    file: Path
    tasks: List[Task] = attr.Factory(list)
    tasks_hash: str = attr.Factory(str)
    log: List[Event] = attr.Factory(list)

    @classmethod
    def from_file(cls, file):
        task = cls(file=file)
        file.touch()
        task.read_file()
        return task

    def read_file(self):
        prior_hash = self.tasks_hash
        with self.file.open("r") as reader:
            tasks_raw = reader.readlines()
        self.tasks = [Task.from_todotxt(todotxt) for todotxt in tasks_raw]
        self.tasks_hash = _tasks_hash([str(task) for task in self.tasks])
        event = Event(
            event_type=FILE_READ,
            file=self.file,
            prior_hash=prior_hash,
            new_hash=self.tasks_hash,
        )
        self.log.append(event)  # pylint: disable=no-member
        return event

    def _change_tasks(self, event_type, changes):
        actions = {
            TASKS_ADDED: io.add_tasks,
            TASKS_DELETED: io.delete_tasks,
            TASKS_UPDATED: io.update_tasks,
        }
        prior_hash = self.tasks_hash
        actions[event_type](changes, self.file)
        event = Event(
            event_type=event_type,
            tasks=changes,
            file=self.file,
            prior_hash=prior_hash,
            new_hash=self.tasks_hash,
        )
        self.log.append(event)  # pylint: disable=no-member
        self.read_file()
        return event

    def add_tasks(self, additions):
        return self._change_tasks(TASKS_ADDED, additions)

    def delete_tasks(self, deletions):
        return self._change_tasks(TASKS_DELETED, deletions)

    def update_tasks(self, updates):
        return self._change_tasks(TASKS_UPDATED, updates)
