from datetime import date
from django.urls import reverse
from django.db import models

# Create your models here.
class Task(models.Model):
    IN_PROGRESS = 'INP'
    READY = 'RDY'
    STATE_CHOICES = (
        (IN_PROGRESS, 'in_progress'),
        (READY, 'ready'),
    )
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    estimate = models.DateField(verbose_name="Срок выполнения")
    state = models.CharField(
        max_length=3,
        choices=STATE_CHOICES,
        default=IN_PROGRESS,
        verbose_name="Статус выполнения",
    )


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

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def get_fields(self):
        return [
            (field.name, field.verbose_name, self._get_FIELD_display(field))
            for field in self.__class__._meta.fields
            if field.name != 'id'
        ]
