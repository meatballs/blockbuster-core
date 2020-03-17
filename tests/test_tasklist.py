# pylint: disable=protected-access, redefined-outer-name
from hashlib import sha256
from pathlib import Path

import blockbuster.core.model as model
from blockbuster.core import TASKS_ADDED, TASKS_DELETED, TASKS_UPDATED
from blockbuster.core.model import Event, Task, TaskList


def test_tasks_hash(test_tasks, test_tasks_hash):
    assert model._tasks_hash(test_tasks) == test_tasks_hash


def test_from_existing_file(test_file, test_tasks, test_tasks_hash):
    task_list = TaskList.from_file(test_file)
    assert len(task_list.tasks) == len(test_tasks)
    for task in task_list.tasks:
        assert isinstance(task, Task)
    assert task_list.tasks_hash == test_tasks_hash


def test_from_new_file(tmp_path):
    test_file = Path(tmp_path, "new_test_file")
    task_list = TaskList.from_file(test_file)
    assert test_file.exists()
    assert task_list.tasks == []
    assert task_list.tasks_hash == sha256("".encode("UTF-8")).hexdigest()


def test_add_tasks(additions, test_file, test_tasks):
    task_list = TaskList.from_file(test_file)
    event = task_list.add_tasks(additions)
    assert len(task_list.tasks) == len(test_tasks) + len(additions)
    for task in additions:
        assert task in [task.description for task in task_list.tasks]
    assert event in task_list.log  # pylint: disable=unsupported-membership-test
    assert isinstance(event, Event)
    assert event.event_type == TASKS_ADDED


def test_delete_tasks(deletions, test_file, test_tasks):
    task_list = TaskList.from_file(test_file)
    event = task_list.delete_tasks(deletions)
    assert len(task_list.tasks) == len(test_tasks) - len(deletions)
    for idx in deletions:
        assert test_tasks[idx] not in task_list.tasks
    assert event in task_list.log  # pylint: disable=unsupported-membership-test
    assert isinstance(event, Event)
    assert event.event_type == TASKS_DELETED


def test_update_tasks(updates, test_file, test_tasks):
    task_list = TaskList.from_file(test_file)
    event = task_list.update_tasks(updates)
    assert len(task_list.tasks) == len(test_tasks)
    for key, value in updates.items():
        assert str(task_list.tasks[key]) == value
    assert event in task_list.log  # pylint: disable=unsupported-membership-test
    assert isinstance(event, Event)
    assert event.event_type == TASKS_UPDATED
