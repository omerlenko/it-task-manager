from django import forms

from task_manager.models import Task


class TaskForm(forms.ModelForm):


    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "date", "class": "form-control"}),
        }

class TaskSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search tasks...", "class": "form-control"}),
    )
