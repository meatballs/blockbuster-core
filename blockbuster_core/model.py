from datetime import datetime


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

    def __str__(self):
        optional_prefixes = ""
        minimal_text = (
            f"{self.created_at.strftime('%Y-%m-%d')} {self.description}"
        )
        optional_suffixes = ""

        if self.done:
            optional_prefixes += "x "

        if self.priority:
            optional_prefixes += f"({self.priority}) "

        if self.completed_at:
            optional_prefixes += f"{self.completed_at.strftime('%Y-%m-%d')} "

        for project in self.projects:
            optional_suffixes += f" +{project}"

        for context in self.contexts:
            optional_suffixes += f" @{context}"

        for key, value in self.tags.items():
            optional_suffixes += f" {key}:{value}"

        return optional_prefixes + minimal_text + optional_suffixes
