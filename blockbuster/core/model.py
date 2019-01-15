from datetime import datetime

from blockbuster.core import DATE_FORMAT


class Task:
    def __init__(
        self,
        description,
        done=False,
        priority=None,
        completed_at=None,
        created_at=None,
        projects=None,
        contexts=None,
        tags=None,
    ):
        self.description = description
        self.done = done
        self.priority = priority
        self.completed_at = completed_at
        self.created_at = created_at or datetime.now().date()
        self.projects = projects or []
        self.contexts = contexts or []
        self.tags = tags or {}

    def __repr__(self):
        result = "blockbuster.core.model.Task("
        result += f'description="{self.description}", '
        result += f"done={self.done}, "
        result += f'priority="{self.priority}", '
        result += f"completed_at={repr(self.completed_at)}, "
        result += f"created_at={repr(self.created_at)}, "
        result += f"projects={self.projects}, "
        result += f"contexts={self.contexts}, "
        result += f"tags={self.tags})"
        return result

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
