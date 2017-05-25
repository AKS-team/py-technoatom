from django.shortcuts import render
from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from custom_auth.models import User

from custom_auth.forms import UserForm


class CreateUser(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserForm
    success_url = reverse_lazy('tasks-list')
    model = User
