from datetime import datetime

from blockbuster.core.model import Task
from hypothesis import given
from hypothesis.strategies import (
    booleans,
    characters,
    dates,
    dictionaries,
    lists,
    sampled_from,
    text,
)

ALPHABET = characters(blacklist_characters=('"'), blacklist_categories=("Cc", "Cs"))


def minimal_text(created_at, description):
    return f"{created_at.strftime('%Y-%m-%d')} {description}"


@given(
    description=text(min_size=1, alphabet=ALPHABET),
    done=booleans(),
    priority=ALPHABET,
    completed_at=dates(),
    created_at=dates(),
    projects=lists(text(min_size=1)),
    contexts=lists(text(min_size=1)),
    tags=dictionaries(keys=text(min_size=1), values=text(min_size=1)),
)
def test_repr(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    task = Task(
        description=description,
        done=done,
        priority=priority,
        completed_at=completed_at,
        created_at=created_at,
        projects=projects,
        contexts=contexts,
        tags=tags,
    )
    import blockbuster.core
    import datetime

    assert isinstance(eval(repr(task)), Task)


@given(created_at=dates(), description=text(min_size=1, alphabet=ALPHABET))
def test_minimal_string(created_at, description):
    task = Task(created_at=created_at, description=description)
    assert str(task) == minimal_text(created_at, description)


@given(
    done=booleans(),
    priority=sampled_from((None, "A")),
    completed_at=sampled_from((None, datetime(2019, 1, 1).date())),
    created_at=dates(),
    description=text(min_size=1, alphabet=ALPHABET),
)
def test_done_string(done, priority, completed_at, created_at, description):
    task = Task(
        done=done,
        priority=priority,
        completed_at=completed_at,
        created_at=created_at,
        description=description,
    )
    if done:
        assert str(task).startswith("x ")
    assert str(task).endswith(minimal_text(created_at, description))


@given(
    done=booleans(),
    priority=ALPHABET,
    completed_at=sampled_from((None, datetime(2019, 1, 1).date())),
    created_at=dates(),
    description=text(min_size=1, alphabet=ALPHABET),
)
def test_priority_string(done, priority, completed_at, created_at, description):
    task = Task(
        done=done,
        priority=priority,
        completed_at=completed_at,
        created_at=created_at,
        description=description,
    )
    if priority:
        assert f"({priority})" in str(task)
    assert str(task).endswith(minimal_text(created_at, description))


@given(
    done=booleans(),
    priority=sampled_from((None, "A")),
    completed_at=dates(),
    created_at=dates(),
    description=text(min_size=1, alphabet=ALPHABET),
)
def test_completed_at_string(done, priority, completed_at, created_at, description):
    task = Task(
        done=done,
        priority=priority,
        completed_at=completed_at,
        created_at=created_at,
        description=description,
    )
    if completed_at:
        assert f"{completed_at.strftime('%Y-%m-%d')}" in str(task)
    assert str(task).endswith(minimal_text(created_at, description))


@given(
    created_at=dates(),
    description=text(min_size=1, alphabet=ALPHABET),
    projects=lists(text(min_size=1)),
    contexts=lists(text(min_size=1)),
    tags=dictionaries(keys=text(min_size=1), values=text(min_size=1)),
)
def test_projects_string(created_at, description, projects, contexts, tags):
    task = Task(
        created_at=created_at,
        description=description,
        projects=projects,
        contexts=contexts,
        tags=tags,
    )
    projects_text = ""
    for project in projects:
        projects_text += f" +{project}"

    assert str(task).startswith(minimal_text(created_at, description))
    assert projects_text in str(task)


@given(
    created_at=dates(),
    description=text(min_size=1, alphabet=ALPHABET),
    projects=lists(text()),
    contexts=lists(text(min_size=1)),
    tags=dictionaries(keys=text(min_size=1), values=text(min_size=1)),
)
def test_contexts_string(created_at, description, projects, contexts, tags):
    task = Task(
        created_at=created_at,
        description=description,
        projects=projects,
        contexts=contexts,
        tags=tags,
    )
    contexts_text = ""
    for context in contexts:
        contexts_text += f" @{context}"

    assert str(task).startswith(minimal_text(created_at, description))
    assert contexts_text in str(task)


@given(
    created_at=dates(),
    description=text(min_size=1, alphabet=ALPHABET),
    projects=lists(text()),
    contexts=lists(text()),
    tags=dictionaries(keys=text(min_size=1), values=text(min_size=1)),
)
def test_tags_string(created_at, description, projects, contexts, tags):
    task = Task(
        created_at=created_at,
        description=description,
        projects=projects,
        contexts=contexts,
        tags=tags,
    )
    tags_text = ""
    for key, value in tags.items():
        tags_text += f" {key}:{value}"

    assert str(task).startswith(minimal_text(created_at, description))
    assert tags_text in str(task)
