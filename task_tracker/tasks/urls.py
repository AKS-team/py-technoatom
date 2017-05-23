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
RoadmapStatisticJson, ScoreStatisticJson, RoadmapStatistic

urlpatterns = [
    # Страница со всеми созданными заданиями
    url(r'^task/all/$', TasksList.as_view(), name='tasks-list'),
    # Страница с информацией о конкретной задаче
    url(r'^task/(?P<pk>[0-9]+)/$', TaskDetailed.as_view(), name='task-detail'),
    # Страница изменения задачи (при установке того, что задача выполнена проставляется балл)
    url(r'^task/update/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='task-update'),
    # Страница создания задачи
    url(r'^task/create/', TaskCreate.as_view(), name='task-create'),
    # Страница подтверждения удаления задачи (удаляется и балл)
    url(r'^task/delete/(?P<pk>[0-9]+)/$', TaskDelete.as_view(), name='task-delete'),

    # Страница создания дорожной карты
    url(r'^roadmap/create/', RoadmapCreate.as_view(), name='roadmap-create'),
    # Страница с заданиями, входящими в дорожную карту и возможностью удалить и просмотреть
    # её статистику
    url(r'^roadmap/(?P<pk>[0-9]+)/$', RoadmapView.as_view(), name='roadmap-detail'),
    # Страница со всеми дорожными картами, ссылками на просмотр входящих в неё заданий,
    # её статистики, удаления
    url(r'^roadmap/all/$', RoadmapList.as_view(), name='roadmap-list'),
    # Страница подтверждения удаления дорожной карты (удаляется и все связанные задачи)
    url(r'^roadmap/delete/(?P<pk>[0-9]+)$', RoadmapDelete.as_view(), name='roadmap-delete'),
    # URL для отдачи json статистических данных о количестве созданных и завершённых задач
    # за каждую неделю в произвольном году у конкретной дорожной карты
    url(r'^roadmap/statistic(?:\/(?P<year>[0-9]{4}))?/(?P<pk>[0-9]+)\.json/$',
        RoadmapStatisticJson.as_view(), name='roadmap-statistic-json'),
    # URL для отдачи json статистических данных о количестве суммарных очков, зачисленных
    # за каждый месяц в произвольном году у конкретной дорожной карты
    url(r'^roadmap/statistic/score(?:\/(?P<year>[0-9]{4}))?/(?P<pk>[0-9]+)\.json/$',
        ScoreStatisticJson.as_view(), name='roadmap-statistic-score-json'),
    # Страница с графическим представлением json статистических данных средствами библиотеки d3,
    # полученных с roadmap-statistic-json и roadmap-statistic-score-json
    url(r'^roadmap/statistic(?:\/(?P<year>[0-9]{4}))?/(?P<pk>[0-9]+)/$',
        RoadmapStatistic.as_view(), name='roadmap-statistic'),
]
