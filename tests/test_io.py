from pathlib import Path

import pytest
from blockbuster.core.io import add_tasks, delete_tasks, read_tasks, update_tasks
from blockbuster.core.model import Task


@pytest.fixture
def test_tasks():
    return [
        "x 2019-01-01 Task One +Project1 @Context1",
        "2019-01-02 Task Two +Project2 @Context2",
    ]


@pytest.fixture
def test_file(test_tasks, tmp_path):
    file = Path(tmp_path, "test_file")
    with file.open("w") as f:
        for task in test_tasks:
            f.write(f"{task}\n")
    return file


def test_read_tasks(test_tasks, test_file):
    tasks = read_tasks(test_file)
    assert len(tasks) == len(test_tasks)
    for task in tasks:
        assert isinstance(task, Task)


def test_add_tasks(test_tasks, test_file):
    tasks = ["task four", "task five"]
    event = add_tasks(tasks, test_file)
    with test_file.open("r") as f:
        data = f.readlines()
    assert len(data) == len(test_tasks) + len(tasks)
    assert (
        event.prior_hash
        == "4dde8028492a6f464b63ab6ccd7e7417c90db473e7ded57be09efb87f76bb2eb"
    )
    assert (
        event.new_hash
        == "7428633cbfc14a8b0ce734cb53221ce78c9790f27938725f7feff6cc8b87d607"
    )
