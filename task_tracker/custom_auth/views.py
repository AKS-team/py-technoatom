from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from custom_auth.models import User
from custom_auth.forms import UserForm
from custom_auth.forms import UserUpdateForm


class CreateUser(CreateView):
    template_name = 'login.html'
    form_class = UserForm
    success_url = reverse_lazy('tasks-list')
    model = User

class UpdateUser(LoginRequiredMixin, UpdateView):
    template_name = 'login.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('tasks-list')

    def get_object(self, queryset=None):
        return self.request.user

class ProfileUser(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    model = User

    def get_object(self, queryset=None):
        return self.request.user
