from parse import get_dataset
from Task import Task


def tasks_gen(filename):
    '''
    Iterator for Tasks exemplars with data from yml file

    :param filename: Path to dataset's yml file
    :type filename: str

    :return: Tasks's items

    :raises OSError: if has problem with file
    :raises yaml.YAMLError: if has problem with format
    :raises ValueError: if has problem with content
    '''
    for data in get_dataset(filename):
        title, state, estimate = data
        new_task = Task(title, estimate)
        if state == 'ready':
            new_task.ready()
        yield new_task
