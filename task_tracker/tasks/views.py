from datetime import date

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy, reverse
from django.db import connection
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.models import Task, Roadmap, Score
from tasks.forms import TaskCreateForm, TaskUpdateForm, RoadmapCreateForm

# Create your views here.
def order(queryset, ordering=('state', 'estimate')):
    return queryset.order_by(*ordering)

class UserFilterMixin:
    def get_queryset(self):
        queryset = super(UserFilterMixin, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

class CreteWithOwnerMixin:
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return http.HttpResponseRedirect(obj.get_absolute_url())


class TaskDetailed(LoginRequiredMixin, UserFilterMixin, DetailView):
    model = Task

class TasksList(LoginRequiredMixin, UserFilterMixin, ListView):
    ordering = ('state', 'estimate')
    model = Task


    def get_queryset(self):
        new_context = order(super(TasksList, self).get_queryset())
        return new_context

class TaskCreate(LoginRequiredMixin, CreteWithOwnerMixin, CreateView):
    form_class = TaskCreateForm
    model = Task

class TaskUpdate(LoginRequiredMixin, UserFilterMixin, UpdateView):
    form_class = TaskUpdateForm
    model = Task


    def post(self, *args, **kwargs):
        super(TaskUpdate, self).post(*args, **kwargs)
        return redirect(reverse('tasks-list'))

class TaskDelete(LoginRequiredMixin, UserFilterMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks-list')

class RoadmapCreate(LoginRequiredMixin, CreateView):
    model = Roadmap
    form_class = RoadmapCreateForm


    def get_form_kwargs(self):
        kwargs = super(RoadmapCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class RoadmapView(LoginRequiredMixin, UserFilterMixin, DetailView):
    model = Roadmap

    def get_context_data(self, **kwargs):
        context = super(RoadmapView, self).get_context_data(**kwargs)
        context['object_list'] = order(Task.objects.filter(roadmap__id=self.kwargs['pk']))
        return context

class RoadmapList(LoginRequiredMixin, UserFilterMixin, ListView):
    model = Roadmap

class RoadmapDelete(LoginRequiredMixin, UserFilterMixin, DeleteView):
    model = Roadmap
    success_url = reverse_lazy('roadmap-list')

class RoadmapStatisticJson(LoginRequiredMixin, View):
    sql_query = "SELECT WEEK(creation_date, 1) AS creation_week, COUNT(id) AS create_count, solved_count \
                    FROM tasks_task AS task_stat \
                    LEFT JOIN  \
                    (   SELECT WEEK(date, 1) AS solve_week, COUNT(id) AS solved_count \
                        FROM tasks_score \
                        WHERE task_id IN \
                        (   SELECT id FROM tasks_task \
                            WHERE roadmap_id = %s and state=%s \
                                  and owner_id = %s \
                        ) AND YEAR(date) = %s \
                        GROUP BY solve_week ) AS score_stat \
                    ON WEEK(creation_date, 1) = solve_week \
                    WHERE roadmap_id = %s and YEAR(creation_date) = %s \
                          and owner_id = %s \
                    GROUP BY creation_week"

    def get(self, request, pk, year):
        if year is None:
            year = date.today().year
        else: year = int(year)
        pk = int(pk)
        context = {}
        context['year'] = year
        context['object_list'] = self.get_statistic_query(pk, year)
        return JsonResponse(context)

    def get_statistic_query(self, pk, year):
        with connection.cursor() as cursor:
            cursor.execute(self.sql_query, [pk, Task.READY, self.request.user.pk,
                                            year, pk, year, self.request.user.pk])
            rows = cursor.fetchall()
        return rows

class ScoreStatisticJson(LoginRequiredMixin, View):
    model = Score


    def get(self, request, pk, year):
        if year is None:
            year = date.today().year
        else: year = int(year)
        pk = int(pk)
        context = {}
        context['year'] = year
        queryset = self.model.objects \
                        .filter(date__year=year, task__roadmap=pk, task__owner=request.user) \
                        .annotate(month_first_day=TruncMonth('date'))\
                        .values_list('month_first_day') \
                        .annotate(sum_points=Sum('points'))
        context['object_list'] = list(queryset)
        return JsonResponse(context)

class RoadmapStatistic(LoginRequiredMixin, View):
    template_name = 'tasks/roadmap_statistic.html'


    def get(self, request, pk, year):
        if year is None:
            year = date.today().year
        context = {}
        context['pk'] = pk
        context['year'] = year
        context['user'] = request.user
        return render_to_response(self.template_name, context)
