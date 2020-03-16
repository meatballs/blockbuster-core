import blockbuster.core.io as io

def test_add_tasks(test_file, test_tasks):
    tasks = ["task four", "task five"]
    new_tasks = io.add_tasks(tasks, test_file)
    assert len(new_tasks) == len(test_tasks) + len(tasks)
    tasks = [item.strip() for item in new_tasks]
    for task in tasks:
        assert task in tasks


def test_delete_tasks(test_file, test_tasks):
    to_delete = [0, 2]
    tasks = io.delete_tasks(to_delete, test_file)
    assert len(tasks) == len(test_tasks) - len(to_delete)
    for idx in to_delete:
        assert test_tasks[idx] not in tasks


def test_update_tasks(test_file, test_tasks):
    to_update = {
        1: "2019-01-02 Task Two Updated +Project2 @Context2",
        2: "2019-03-05 Task Three +ProjectUpdated +Project2 @Context1",
    }
    tasks = io.update_tasks(to_update, test_file)
    assert len(tasks) == len(test_tasks)
    for key, value in to_update.items():
        assert tasks[key].strip() == value
