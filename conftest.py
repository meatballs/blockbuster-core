import pytest
from pathlib import Path


@pytest.fixture
def test_tasks():
    return [
        "x 2019-01-01 Task One +Project1 @Context1",
        "2019-01-02 Task Two +Project2 @Context2",
        "2019-03-05 Task Three +Project1 +Project2 @Context1",
    ]


@pytest.fixture
def test_tasks_hash():
    return "4ef27c088837256efa400ddf45ba934a2f62125b2ecb83a4cdc468696c1208f8"


@pytest.fixture(name="test_file")
def _test_file(tmp_path, test_tasks):
    test_file = Path(tmp_path, "test_file")
    with test_file.open("w") as file:
        file.write("\n".join(test_tasks))
    return test_file


@pytest.fixture
def additions():
    return ["task four", "task five"]


@pytest.fixture
def updates():
    return {
        1: "2019-01-02 Task Two Updated +Project2 @Context2",
        2: "2019-03-05 Task Three +ProjectUpdated +Project2 @Context1",
    }
@pytest.fixture
def deletions():
    return [0, 2]
