from datetime import date, timedelta
import pytest
import mock
from tasks.models import Task
from tests.base.modules.model import ModelModule
from django.utils import formats, html
# from tests.base.utils import authenticate

# py.test --cov=task_tracker # see coverage
class TestTaskList:

    @pytest.fixture(params=[
        'task1',
        'task2'
    ])
    def task1(self, request, db):
        return ModelModule().create_task(title=request.param, estimate=date.today())

    @pytest.fixture(params=[
        'task1\'',
        'task2<',
        'task3>',
        'task4\"',
        'task5&'
    ])
    def task_with_special_symbol(self, request, db):
        return ModelModule().create_task(title=request.param, estimate=date.today())

    def test_escaping(self, http, task_with_special_symbol):
        response = http.get('/task/all/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert html.escape(task_with_special_symbol.title) in content

    def test_existing(self, http, task1):
        response = http.get('/task/all/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert task1.title in content
        assert formats.date_format(task1.estimate) in content
        assert task1.get_state_display() in content

class TestTaskCreate:
    url = '/task/create/'


    @pytest.yield_fixture(params=[
        'task1',
        'task1\'',
        'task2'
    ])
    def task_title(self, request):
        yield request.param

    @pytest.fixture()
    def today(self):
        return date.today()

    @pytest.fixture()
    def prev_day(self, today):
        return today - timedelta(days=1)

    def test_success_create(self, db, http, task_title, today):
        response = http.post(self.url, data={'title': task_title, 'estimate': today})
        assert response.status_code == 302
        assert Task.objects.filter(title=task_title, estimate=today).exists()

    def test_with_wrong_estimate_create(self, db, http, task_title, prev_day):
        response = http.post(self.url, data={'title': task_title, 'estimate': prev_day})
        assert response.status_code == 200
        assert not Task.objects.filter(title=task_title, estimate=prev_day).exists()

    def test_with_empty_title(self, db, http, today):
        response = http.post(self.url, data={'title': '', 'estimate': today})
        assert response.status_code == 200
        assert not Task.objects.filter(title='', estimate=today).exists()

    def test_with_empty_estimate(self, db, http):
        response = http.post(self.url, data={'title': ''})
        assert response.status_code == 200
        assert not Task.objects.filter(title='').exists()
