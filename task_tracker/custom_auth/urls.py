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
from django.conf.urls import url, include
from django.urls import reverse_lazy
from django.contrib.auth.views import login, logout

from custom_auth.views import CreateUser, UpdateUser, ProfileUser
from custom_auth.forms import AuthForm

urlpatterns = [
    url(r'^registration', CreateUser.as_view(), name='create-user'),
    url(r'^login', login, {'authentication_form': AuthForm,
                           'template_name': 'login.html'}, name='login'),
    url(r'^logout', logout, {'next_page': reverse_lazy('login')}, name='logout_pg'),
    url(r'^update$', UpdateUser.as_view(), name='update-user'),
    url(r'^profile$', ProfileUser.as_view(), name='profile-user'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
