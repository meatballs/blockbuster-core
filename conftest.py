import pytest

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
