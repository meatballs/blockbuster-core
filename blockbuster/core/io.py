def add_tasks(additions, file):
    """Add tasks to a todo.txt file

    Parameters
    ----------
    additions
        A list or tuple of strings in todo.txt format
    file
        A Path instance

    Returns
    -------
    list
        of the tasks in the file after the addition has been made
    """
    with file.open("a+") as read_writer:
        read_writer.write("\n" + "\n".join(list(additions)))
        read_writer.seek(0)
        tasks = read_writer.readlines()
    return [task.strip() for task in tasks]


def delete_tasks(deletions, file):
    """Delete lines from a todo.txt file

    Parameters
    ----------
    deletions
        A list or tuple of index numbers indicating which tasks to delete by
        their position in the file
    file
        A Path instance

    Returns
    -------
    list
        of the tasks in the file after the addition has been made
    """
    with file.open("r+") as read_writer:
        tasks = read_writer.readlines()
        keep_ids = [i for i in range(len(tasks)) if i not in deletions]
        read_writer.seek(0)
        for task in [tasks[i] for i in keep_ids]:
            read_writer.write(task)
        read_writer.truncate()
        read_writer.seek(0)
        tasks = read_writer.readlines()
    return [task.strip() for task in tasks]


def update_tasks(updates, file):
    """Update lines in a todo.txt file

    Parameters
    ----------
    updates
        A dictionary mapping the index number of the task within the file to
        a string of its updated content
    file
        A Path instance

    Returns
    -------
    list
        of the tasks in the file after the addition has been made
    """
    with file.open("r+") as read_writer:
        tasks = read_writer.readlines()
        new_tasks = [
            updates[item[0]] if item[0] in updates else tasks[item[0]]
            for item in enumerate(tasks)
        ]
        read_writer.seek(0)
        read_writer.seek(0)
        read_writer.write("\n".join([task.strip() for task in new_tasks]))
        read_writer.truncate()
        read_writer.seek(0)
        tasks = read_writer.readlines()
    return [task.strip() for task in tasks]
