from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from tasks.models import Task, Roadmap
from tasks.forms import TaskCreateForm, TaskUpdateForm, RoadmapCreateForm

# Create your views here.
class TaskDetailed(DetailView):
    model = Task

class TasksList(ListView):
    ordering = ('state', 'estimate')
    model = Task


    def get_queryset(self):
        new_context = Task.objects.order_by(*self.ordering)
        return new_context

class TaskCreate(CreateView):
    form_class = TaskCreateForm
    model = Task

class TaskUpdate(UpdateView):
    form_class = TaskUpdateForm
    model = Task

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks-list')

class RoadmapCreate(CreateView):
    model = Roadmap
    form_class = RoadmapCreateForm

class RoadmapView(DetailView):
    model = Roadmap

    def get_context_data(self, **kwargs):
        context = super(RoadmapView, self).get_context_data(**kwargs)
        context['object_list'] = Task.objects.filter(roadmap__id=self.kwargs['pk'])
        return context

class RoadmapList(ListView):
    model = Roadmap

class RoadmapDelete(DeleteView):
    model = Roadmap
    success_url = reverse_lazy('roadmap-list')
