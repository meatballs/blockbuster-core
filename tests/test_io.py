# pylint: disable=protected-access
from pathlib import Path

import blockbuster.core.model as model
import pytest
from blockbuster.core.model import Task

TEST_TASKS = [
    "x 2019-01-01 Task One +Project1 @Context1",
    "2019-01-02 Task Two +Project2 @Context2",
    "2019-03-05 Task Three +Project1 +Project2 @Context1",
]

TEST_TASKS_HASH = "4ef27c088837256efa400ddf45ba934a2f62125b2ecb83a4cdc468696c1208f8"

@pytest.fixture(name="test_file")
def _test_file(tmp_path):
    test_file = Path(tmp_path, "test_file")
    with test_file.open("w") as file:
        file.write("\n".join(TEST_TASKS))
    return test_file


def test_read_tasks(test_file):
    tasks = model._read_tasks(test_file)
    assert len(tasks) == len(TEST_TASKS)
    for task in tasks:
        assert isinstance(task, Task)


def test_add_tasks(test_file):
    expected_hash = "697547c610e44cb34a18e239a223d0a0d2aa4137eb7fb9dac5016cdcf39c1403"
    tasks = ["task four", "task five"]
    event = model._add_tasks(tasks, test_file)
    with test_file.open("r") as file:
        data = file.readlines()
    assert len(data) == len(TEST_TASKS) + len(tasks)
    assert event.prior_hash == TEST_TASKS_HASH
    assert event.new_hash == expected_hash
    tasks = [item.strip() for item in data]
    for task in tasks:
        assert task in tasks


def test_delete_tasks(test_file):
    expected_hash = "949076372ee15f1b7ff7c6ec36a258b5a1b494f543ebf4b34eb3d5aa64d27f0b"
    to_delete = [0, 2]
    event = model._delete_tasks(to_delete, test_file)
    with test_file.open("r") as file:
        data = file.readlines()
    assert len(data) == len(TEST_TASKS) - len(to_delete)
    assert event.prior_hash == TEST_TASKS_HASH
    assert event.new_hash == expected_hash
    tasks = [item.strip() for item in data]
    for idx in to_delete:
        assert TEST_TASKS[idx] not in tasks


def test_update_tasks(test_file):
    expected_hash = "b19ccf6c81f9b9fd3335f8b27d5e2e6fa80c691fbe7d0a1cf1d1d04ca5e96b53"
    to_update = {
        1: "2019-01-02 Task Two Updated +Project2 @Context2",
        2: "2019-03-05 Task Three +ProjectUpdated +Project2 @Context1",
    }
    event = model._update_tasks(to_update, test_file)
    with test_file.open("r") as file:
        data = file.readlines()
    assert len(data) == len(TEST_TASKS)
    assert event.prior_hash == TEST_TASKS_HASH
    assert event.new_hash == expected_hash
    tasks = [item.strip() for item in data]
    for key, value in to_update.items():
        assert tasks[key] == value
