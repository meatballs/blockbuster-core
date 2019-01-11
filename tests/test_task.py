# pylint: disable=C0111
from hypothesis import given
from hypothesis.strategies import dates, text

from blockbuster_core.model import Task


@given(created_at=dates(), description=text())
def test_str(created_at, description):
    task = Task(created_at=created_at, description=description)
    assert str(task) == f"{created_at.strftime('%Y-%m-%d')} {description}"
