from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from custom_auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'phone',
            'first_name',
            'last_name',
            'age',
            'region'
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Сохранить'))

    def save(self, *args, **kwargs):
        new_user = self.instance
        new_user.set_password(new_user.password)
        instance = super(UserForm, self).save(*args, **kwargs)
        return instance

class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Войти'))
        self.helper.add_input(Button('regist', "Зарегестрировать",
                                     href=reverse_lazy('create-user'),
                                     css_class='btn btn-success'))
