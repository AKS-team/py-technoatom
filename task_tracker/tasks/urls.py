"""task_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tasks.views import TaskCreate, TaskDetailed, TaskUpdate, TasksList,\
TaskDelete, RoadmapView, RoadmapCreate, RoadmapList, RoadmapDelete, \
RoadmapStatisticJson, RoadmapStatistic

urlpatterns = [
    url(r'^task/all/$', TasksList.as_view(), name='tasks-list'),
    url(r'^task/(?P<pk>[0-9]+)/$', TaskDetailed.as_view(), name='task-detail'),
    url(r'^task/update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update'),
    url(r'^task/create/', TaskCreate.as_view(), name='task-create'),
    url(r'^task/delete/(?P<pk>[0-9]+)/$', TaskDelete.as_view(), name='task-delete'),

    url(r'^roadmap/create/', RoadmapCreate.as_view(), name='roadmap-create'),
    url(r'^roadmap/(?P<pk>[0-9]+)/$', RoadmapView.as_view(), name='roadmap-detail'),
    url(r'^roadmap/all/$', RoadmapList.as_view(), name='roadmap-list'),
    url(r'^roadmap/delete/(?P<pk>[0-9]+)$', RoadmapDelete.as_view(), name='roadmap-delete'),
    url(r'^roadmap/statistic(?:\/(?P<year>[0-9]{4}))?/(?P<pk>[0-9]+)\.json/$',
        RoadmapStatisticJson.as_view(), name='roadmap-statistic-json'),
    url(r'^roadmap/statistic(?:\/(?P<year>[0-9]{4}))?/(?P<pk>[0-9]+)/$',
        RoadmapStatistic.as_view(), name='roadmap-statistic'),
]
