import datetime as dt
from hashlib import sha256
from pathlib import Path
from typing import Dict, List, Optional

import attr
import blockbuster.core.parser as parser
from blockbuster.core import DATE_FORMAT


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
    tasks: List[str]
    file: str
    prior_hash: str
    new_hash: str
    occurred_at: dt.datetime = dt.datetime.now()

    def to_dict(self):
        return attr.asdict(self)


def _read_tasks(file):
    """Create Tasks instances from a todo.txt file

    Parameters
    ----------
    file
        A Path instance

    Returns
    -------
    list
        of Task instances
    """
    with file.open("r") as reader:
        tasks_raw = reader.readlines()

    return [Task.from_todotxt(todotxt) for todotxt in tasks_raw]


def _add_tasks(additions, file):
    """Add tasks to a todo.txt file

    Parameters
    ----------
    additions
        A list or tuple of strings in todo.txt format
    file
        A Path instance

    Returns
    -------
    TasksAdded
        An instance of blockbuster.core.model.Event
    """
    with file.open("r+") as read_writer:
        prior_hash = sha256(read_writer.read().encode(encoding="UTF-8")).hexdigest()
        for task in additions:
            read_writer.write(f"{task}\n")
        read_writer.seek(0)
        new_hash = sha256(read_writer.read().encode(encoding="UTF-8")).hexdigest()

    return Event(
        event_type="blockbuster.core.tasks_added",
        tasks=additions,
        file=file,
        prior_hash=prior_hash,
        new_hash=new_hash,
    )


def _delete_tasks(deletions, file):
    """Delete lines from a todo.txt file

    Parameters
    ----------
    deletions
        A list or tuple of index numbers indicating which tasks to delete by
        their position in the file
    file
        A Path instance

    Returns
    -------
    TasksDeleted
        An instance of blockbuster.core.model.Event
    """
    with file.open("r+") as read_writer:
        prior_hash = sha256(read_writer.read().encode(encoding="UTF-8")).hexdigest()
        read_writer.seek(0)
        tasks = read_writer.readlines()
        keep_ids = [i for i in range(len(tasks)) if i not in deletions]
        read_writer.seek(0)
        for task in [tasks[i] for i in keep_ids]:
            read_writer.write(task)
        read_writer.truncate()
        read_writer.seek(0)
        new_hash = sha256(read_writer.read().encode(encoding="UTF-8")).hexdigest()
    return Event(
        event_type="blockbuster.core.tasks_deleted",
        tasks=[tasks[i] for i in deletions],
        file=file,
        prior_hash=prior_hash,
        new_hash=new_hash,
    )


def _update_tasks(updates, file):
    """Update lines in a todo.txt file

    Parameters
    ----------
    updates
        A dictionary mapping the index number of the task within the file to
        a string of its updated content
    file
        A Path instance

    Returns
    -------
    TasksUpdated
        An instance of blockbuster.core.model.Event
    """
    with file.open("r+") as read_writer:
        prior_hash = sha256(read_writer.read().encode(encoding="UTF-8")).hexdigest()
        read_writer.seek(0)
        tasks = read_writer.readlines()
        new_tasks = [
            updates[item[0]] if item[0] in updates else tasks[item[0]]
            for item in enumerate(tasks)
        ]
        print(new_tasks)
        read_writer.seek(0)
        for task in new_tasks:
            read_writer.write(f"{task.strip()}\n")
        read_writer.truncate()
        read_writer.seek(0)
        new_hash = sha256(read_writer.read().encode(encoding="UTF-8")).hexdigest()
    return Event(
        event_type="blockbuster.core.tasks_updated",
        tasks=list(updates.values()),
        file=file,
        prior_hash=prior_hash,
        new_hash=new_hash,
    )


@attr.s(auto_attribs=True, slots=True)
class TaskList:
    """A class to represent a todo.txt file and its contents

    Attributes
    ----------
    file : pathlib.Path
        the todo.txt file
    tasks :  list or tuple
        of Task instances representing the file contents
    """

    file: Path
    tasks: List[Task]
