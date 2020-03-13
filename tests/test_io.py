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

TEST_TASKS_HASH = "399a33976715eaacaa62f2d3ccd6b06882f64e69f4cd1eb946690c2a4d6c7b0e"


@pytest.fixture(name="test_file")
def _test_file(tmp_path):
    with Path(tmp_path, "test_file").open("w") as file:
        for task in TEST_TASKS:
            file.write(f"{task}\n")
    return file


def test_read_tasks(test_file):
    tasks = model._read_tasks(test_file)
    assert len(tasks) == len(TEST_TASKS)
    for task in tasks:
        assert isinstance(task, Task)


def test_add_tasks(test_file):
    expected_hash = "7c39ee8e93e03a4249a11cc6b28de4d6da9f66e648115a2a7db78e3b3b9bd7b6"
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
    expected_hash = "f624df388a8e77dd16dc597c028062fb718ef29840948e7a241a1311a57aa521"
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
