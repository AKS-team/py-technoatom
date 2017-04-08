from datetime import date


class Task:

    def __init__(self, title, estimate):
        self.title = title
        self.estimate = estimate
        self.state = 'in_progress'

    @property
    def remaining(self):
        return self.estimate - date.today()

    @property
    def is_failed(self):
        return self.state == 'in_progress' and self.estimate < date.today()

    def ready(self):
        if self.state == 'in_progress':
            self.state = 'ready'

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.estimate, self.state)
