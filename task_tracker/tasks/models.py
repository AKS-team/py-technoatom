from datetime import date
from django.urls import reverse
from django.db import models
from django.db.models import F, Max, ExpressionWrapper

# Create your models here.
class Task(models.Model):
    IN_PROGRESS = 'INP'
    READY = 'RDY'
    STATE_CHOICES = (
        (IN_PROGRESS, 'in_progress'),
        (READY, 'ready'),
    )
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    creation_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    estimate = models.DateField(verbose_name="Срок выполнения")
    state = models.CharField(
        max_length=3,
        choices=STATE_CHOICES,
        default=IN_PROGRESS,
        verbose_name="Статус выполнения",
    )
    roadmap = models.ForeignKey('Roadmap',
                                blank=True,
                                null=True,
                                verbose_name="Дорожная карта",
                                on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    @property
    def remaining(self):
        return self.estimate - date.today()

    @property
    def is_failed(self):
        return self.state == self.IN_PROGRESS and self.estimate < date.today()

    @property
    def is_critical(self):
        return self.is_failed or (self.state == self.IN_PROGRESS and self.remaining.days < 3)

    @property
    def is_ready(self):
        return self.state == self.READY

    def ready(self):
        self.state = self.READY

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def get_fields(self):
        exclude = ('id',)
        return [
            (field.name, field.verbose_name, self._get_FIELD_display(field))
            for field in self.__class__._meta.fields
            if field.name not in exclude
        ]

class Roadmap(models.Model):


    def __str__(self):
        return f'Дорожная карта №{self.pk}'

    def get_absolute_url(self):
        return reverse('roadmap-detail', kwargs={'pk': self.pk})

    def get_tasks(self):
        return Task.objects.filter(roadmap__id=self.id)

    @property
    def today(self):
        return [task for task in self.get_tasks().filter(estimate=date.today())]

    def filter(self, state):
        return self.get_tasks().filter(state=state)

class Score(models.Model):
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Задача"
    )
    date = models.DateField(verbose_name="Дата зачисления")
    points = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Количество зачистенных очков")

    def set_score(self, task):
        self.task = task
        self.date = date.today()
        diff_dict = Task.objects.annotate(diff=ExpressionWrapper(F('estimate') - F('creation_date'),
                                                                 output_field=models.DurationField()
                                                                )
                                         ).aggregate(Max('diff'))
        self.points = ((self.date - self.task.creation_date).days /
                       (self.task.estimate - self.task.creation_date).days) \
                        + ((self.task.estimate - self.task.creation_date).days / diff_dict['diff__max'].days)
        return self
