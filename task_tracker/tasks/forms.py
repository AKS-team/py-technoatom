from datetime import date
from django import forms
from tasks.models import Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TaskCreateForm(forms.ModelForm):
    INVALID_ESTIMATE = 'invalid_estimate'
    error_messages = {
        INVALID_ESTIMATE: "Срок выполнения должен быть больше или равен сегодняшнему дню.",
    }
    class Meta:
        model = Task
        fields = [
            'title',
            'estimate',
        ]


    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Сохранить'))

    def clean_estimate(self):
        data = self.cleaned_data['estimate']
        if data < date.today():
            raise forms.ValidationError(self.error_messages[self.INVALID_ESTIMATE],
                                        code=self.INVALID_ESTIMATE)
        return data

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = [
            'id',
        ]


    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Сохранить'))
