from django import forms

from task_manager.models import Task


class TaskForm(forms.ModelForm):


    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "date", "class": "form-control"}),
        }
