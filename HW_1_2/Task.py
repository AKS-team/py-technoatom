from datetime import date


class Task:

    IN_PROGRESS = 'in_progress'
    READY = 'ready'
    
    def __init__(self, title, estimate):
        self.title = title
        self.estimate = estimate
        self.state = self.IN_PROGRESS

    @property
    def remaining(self):
        return self.estimate - date.today()

    @property
    def is_failed(self):
        return self.state == self.IN_PROGRESS and self.estimate < date.today()

    @property
    def is_critical(self):
        return self.is_failed or (self.state == self.IN_PROGRESS and self.remaining.days < 3)

    def ready(self):
        self.state = self.READY

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.estimate, self.state)
