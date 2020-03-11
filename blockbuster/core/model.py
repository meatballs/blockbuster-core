"""Classes to represent tasks and the events which cause them to change state.

These classes have no dependencies on any other component of the blockbuster
namespace.
"""
import datetime as dt
import re
from typing import Dict, List, Optional

import attr
from blockbuster.core import DATE_FORMAT


def _done(todotxt):
    """
    Returns
    -------
    tuple
        boolean indicating whether the task is complete
        the todo.txt string stripped of any completed portion
    """
    done = todotxt.startswith("x")
    if done:
        todotxt = todotxt[1:].strip()
    return done, todotxt


def _priority(todotxt):
    """
    Returns
    -------
    tuple
        Any priority character
        The todo.txt string stripped of any priority character
    """
    regex = re.compile(r"\s*\((\S)\)")
    match = regex.search(todotxt)
    priority = None
    if match:
        priority = match.group(0).strip().lstrip("(").rstrip(")")
        todotxt = regex.sub("", todotxt).strip()
    return priority, todotxt


def _dates(todotxt):
    regex = re.compile(r"(?<!\S)(\s*\d{4}-\d{2}-\d{2})")
    match = regex.search(todotxt)
    dates = {"completed_at": None, "created_at": None}
    if match:
        matches = [item for item in regex.finditer(todotxt)]
        if len(matches) == 2:
            dates["completed_at"] = dt.datetime.strptime(
                matches[0].group().strip(), "%Y-%m-%d"
            ).date()
            dates["created_at"] = dt.datetime.strptime(
                matches[1].group().strip(), "%Y-%m-%d"
            ).date()
        else:
            dates["created_at"] = dt.datetime.strptime(
                matches[0].group().strip(), "%Y-%m-%d"
            ).date()
        todotxt = regex.sub("", todotxt).strip()

    return dates, todotxt


def _projects(todotxt):
    regex = re.compile(r"\s+(\+\w+)")
    match = regex.search(todotxt)
    projects = []
    if match:
        projects = [
            item.group().strip().lstrip("+") for item in regex.finditer(todotxt)
        ]
        todotxt = regex.sub("", todotxt).strip()

    return projects, todotxt


def _contexts(todotxt):
    regex = re.compile(r"\s+(\@\w+)")
    match = regex.search(todotxt)
    contexts = []
    if match:
        contexts = [
            item.group().strip().lstrip("@") for item in regex.finditer(todotxt)
        ]
        todotxt = regex.sub("", todotxt).strip()

    return contexts, todotxt


def _tags(todotxt):
    regex = re.compile(r"\s+(\w+\:\S+)")
    match = regex.search(todotxt)
    tags = {}
    if match:
        items = (item.group().strip() for item in regex.finditer(todotxt))
        tags = {item.split(":")[0]: item.split(":")[1] for item in items}
        todotxt = regex.sub("", todotxt).strip()

    if tags:
        tags = {
            key: (
                dt.datetime.strptime(value, "%Y-%m-%d").date()
                if re.match(r"\d{4}-\d{2}-\d{2}$", value)
                else value
            )
            for key, value in tags.items()
        }

    return tags, todotxt


@attr.s(auto_attribs=True, slots=True)
class Task:
    """ A class to represent a task

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
    completed_at: Optional[dt.datetime.date] = None
    created_at: dt.datetime.date = dt.datetime.now().date()
    projects: List[str] = attr.Factory(list)
    contexts: List[str] = attr.Factory(list)
    tags: Dict = attr.Factory(dict)

    @classmethod
    def from_todotxt(cls, todotxt):
        """Create a Task instance from a string in todo.txt format"""
        todotxt = todotxt.strip()

        task = {
            "description": None,
            "done": False,
            "priority": None,
            "completed_at": None,
            "created_at": None,
            "projects": None,
            "contexts": None,
            "tags": None,
        }

        task["done"], todotxt = _done(todotxt)
        task["priority"], todotxt = _priority(todotxt)
        task["tags"], todotxt = _tags(todotxt)
        task["projects"], todotxt = _projects(todotxt)
        task["contexts"], todotxt = _contexts(todotxt)
        dates, todotxt = _dates(todotxt)
        task["completed_at"] = dates["completed_at"]
        task["created_at"] = dates["created_at"]
        task["description"] = todotxt.strip()

        return cls(**task)

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

        for key, value in self.tags.items():
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
