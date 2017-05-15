from datetime import date


class Roadmap:

    def __init__(self, tasks=None):
        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    @property
    def today(self):
        return [task for task in self.tasks if task.estimate == date.today()]

    def filter(self, state):
        return [task for task in self.tasks if task.state == state]
