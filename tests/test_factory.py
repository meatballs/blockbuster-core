from datetime import date, datetime

import blockbuster.core.factory as factory
from blockbuster.core.model import Task
from hypothesis import given
from hypothesis.strategies import (
    characters,
    dates,
    dictionaries,
    lists,
    sampled_from,
    text,
)

ALPHABET = characters(whitelist_categories=("L", "N"))


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
def test_done(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    test_text = todotxt(
        description, done, priority, completed_at, created_at, projects, contexts, tags
    )
    result_done, result_text = factory._done(test_text)
    assert result_done == (done == "x")
    assert not result_text.startswith("x")


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
def test_dates(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    test_text = todotxt(
        description, done, priority, completed_at, created_at, projects, contexts, tags
    )
    result_dates, result_text = factory._dates(test_text)
    assert result_dates["completed_at"] == completed_at.strftime("%Y-%m-%d")
    assert result_dates["created_at"] == created_at.strftime("%Y-%m-%d")
    assert completed_at.strftime("%Y-%m-%d") not in result_text
    assert created_at.strftime("%Y-%m-%d") not in result_text


def test_dates_in_tags():
    test_text = "(A) Test Task 2019-01-01 due:2019-02-01"
    result_dates, result_text = factory._dates(test_text)
    assert result_dates["created_at"] == "2019-01-01"
    assert result_dates["completed_at"] is None
    assert result_text == "(A) Test Task  due:2019-02-01"


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
def test_projects(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    test_text = todotxt(
        description, done, priority, completed_at, created_at, projects, contexts, tags
    )
    result_projects, result_text = factory._projects(test_text)
    if projects:
        assert result_projects == projects
        for project in projects:
            assert f"+{project}" not in result_text
    else:
        assert result_projects is None
        assert result_text == test_text


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
def test_contexts(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    test_text = todotxt(
        description, done, priority, completed_at, created_at, projects, contexts, tags
    )
    result_contexts, result_text = factory._contexts(test_text)
    if contexts:
        assert result_contexts == contexts
        for context in contexts:
            assert f"@{context}" not in result_text
    else:
        assert result_contexts is None
        assert result_text == test_text


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
def test_tags(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    test_text = todotxt(
        description, done, priority, completed_at, created_at, projects, contexts, tags
    )
    tags_text = "".join(f" {key}:{value}" for key, value in tags.items())
    result_tags, result_text = factory._tags(test_text)
    if tags:
        assert result_tags == tags
        assert tags_text not in result_tags
    else:
        assert result_tags is None
        assert result_text == test_text


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
def test_create(
    description, done, priority, completed_at, created_at, projects, contexts, tags
):
    test_text = todotxt(
        description, done, priority, completed_at, created_at, projects, contexts, tags
    )
    task = factory.create_task(test_text)
    assert isinstance(task, Task)
    assert task.done == (done == "x")
    assert task.priority == priority
    assert task.completed_at == completed_at.strftime("%Y-%m-%d")
    if created_at is None:
        assert task.created_at == datetime.now().date.strftime("%Y-%m-%d")
    else:
        assert task.created_at == created_at.strftime("%Y-%m-%d")
    assert task.description == description
    assert task.projects == projects
    assert task.contexts == contexts
