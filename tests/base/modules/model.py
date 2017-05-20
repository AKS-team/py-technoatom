from tasks.models import Task

class ModelModule:
    def create_task(self, title, estimate, **kwargs):
        params = {
            'title': title,
            'estimate': estimate
        }
        params.update(kwargs)
        return Task.objects.create(**params)
