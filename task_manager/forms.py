from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task_manager.models import Task, Tag, Worker, Position, Team, Project


class WorkerCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=True,
        empty_label="Select your job position.",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position"
        )


class WorkerUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position"
        )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        required=True,
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas.",
        widget=forms.TextInput(attrs={"placeholder": "e.g. bug, UI, backend"}),
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            tag_names = [tag.name for tag in self.instance.tags.all()]
            self.initial["tags"] = ", ".join(tag_names)

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", "")
        tag_names = [tag.strip().replace(" ", "-").lower() for tag in tags.split(",") if tag.strip()]
        return tag_names

    def save(self, commit=True):
        task = super().save(commit=False)
        tag_names = self.cleaned_data["tags"]

        if commit:
            task.save()
            task.assignees.set(self.cleaned_data["assignees"])

            tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
            task.tags.set(tags)

        return task

class TaskSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search tasks...", "class": "form-control"}),
    )


class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        required=True,
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = "__all__"


class ProjectForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = "__all__"