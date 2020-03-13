import datetime as dt
from typing import Dict, List, Optional

import attr
import blockbuster.core.parser as parser
from blockbuster.core import DATE_FORMAT


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

        for key, value in self.tags.items(): # pylint: disable=no-member
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
