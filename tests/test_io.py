import blockbuster.core.io as io


def test_add_tasks(additions, test_file, test_tasks):
    new_tasks = io.add_tasks(additions, test_file)
    assert len(new_tasks) == len(test_tasks) + len(additions)
    for task in additions:
        assert task in new_tasks


def test_delete_tasks(deletions, test_file, test_tasks):
    tasks = io.delete_tasks(deletions, test_file)
    assert len(tasks) == len(test_tasks) - len(deletions)
    for idx in deletions:
        assert test_tasks[idx] not in tasks


def test_update_tasks(updates, test_file, test_tasks):
    tasks = io.update_tasks(updates, test_file)
    assert len(tasks) == len(test_tasks)
    for key, value in updates.items():
        assert tasks[key].strip() == value
