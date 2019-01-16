from hashlib import sha256

from blockbuster.core.factory import create_task
from blockbuster.core.model import TasksAdded, TasksDeleted, TasksUpdated


def read_tasks(file):
    with file.open("r") as f:
        tasks_raw = f.readlines()

    return [create_task(todotxt) for todotxt in tasks_raw]


def add_tasks(tasks, file):
    with file.open("r+") as f:
        prior_hash = sha256(f.read().encode(encoding="UTF-8")).hexdigest()
        for task in tasks:
            f.write(f"{task}\n")
        f.seek(0)
        new_hash = sha256(f.read().encode(encoding="UTF-8")).hexdigest()

    return TasksAdded(tasks=tasks, file=file, prior_hash=prior_hash, new_hash=new_hash)


def delete_tasks(tasks, file):
    with file.open("r+") as f:
        prior_hash = sha256(f.read().encode(encoding="UTF-8")).hexdigest()

        file.seek(0)
        new_hash = sha256(f.read().encode(encoding="UTF-8")).hexdigest()

    return TasksDeleted(
        tasks=tasks, file=file, prior_hash=prior_hash, new_hash=new_hash
    )


def update_tasks(tasks, file):
    with file.open("r+") as f:
        prior_hash = sha256(f.read().encode(encoding="UTF-8")).hexdigest()

        file.seek(0)
        new_hash = sha256(f.read().encode(encoding="UTF-8")).hexdigest()

    return TasksUpdated(
        tasks=tasks, file=file, prior_hash=prior_hash, new_hash=new_hash
    )
