from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from tasks.models import Task
from tasks.forms import TaskCreateForm, TaskUpdateForm

# Create your views here.
class TaskCreate(CreateView):
    form_class = TaskCreateForm
    model = Task

class TaskDetailed(DetailView):
    model = Task

class TaskUpdate(UpdateView):
    form_class = TaskUpdateForm
    model = Task
