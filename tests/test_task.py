from datetime import date, datetime

import blockbuster.core.model as model
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

ALPHABET = characters(
    blacklist_characters=('"', "+", "@", " "), blacklist_categories=("Cc", "Cs")
)


def todotxt(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    projects_txt = "".join([f" +{project}" for project in projects])
    contexts_txt = "".join([f" @{context}" for context in contexts])
    tags_txt = "".join(f" {key}:{value}" for key, value in tags.items())
    result = f"{done} ({priority})"
    result += f" {completed_at.strftime('%Y-%m-%d')}"
    result += f" {created_at.strftime('%Y-%m-%d')}"
    result += f" {description.strip()}"
    result += f"{projects_txt}{contexts_txt}{tags_txt}"
    return result


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


@given(
    description=text(min_size=1, alphabet=ALPHABET),
    done=sampled_from(("", "x")),
    priority=characters(whitelist_categories=("Lu",)),
    completed_at=dates(min_value=date(1111, 1, 1)),
    created_at=dates(min_value=date(1111, 1, 1)),
    projects=lists(text(min_size=1, alphabet=ALPHABET)),
    contexts=lists(text(min_size=1, alphabet=ALPHABET)),
    tags=dictionaries(
        keys=text(min_size=1, alphabet=ALPHABET),
        values=text(min_size=1, alphabet=ALPHABET),
    ),
)
def test_from_todotxt(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    task = Task.from_todotxt(
        todotxt(
            description,
            done,
            priority,
            completed_at,
            created_at,
            projects,
            contexts,
            tags,
        )
    )
    assert task.done == (done == "x")
    assert task.priority == priority
    assert task.completed_at == completed_at
    if created_at is None:
        assert task.created_at == datetime.now().date()
    else:
        assert task.created_at == created_at
    assert task.description == description
    assert task.projects == projects
    assert task.contexts == contexts
    assert task.tags == tags


def test_from_todotxt_with_date_tags():
    test_text = "2019-01-01 Test Task +Project1 due:2019-02-01"
    task = Task.from_todotxt(test_text)
    assert task.created_at == datetime(2019, 1, 1).date()
    assert task.completed_at is None
    assert task.tags == {"due": datetime(2019, 2, 1).date()}
