from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from task_manager.models import Worker, Task


def index(request) -> HttpResponse:
    current_user = request.user
    pending_tasks = current_user.tasks.filter(is_completed=False)
    completed_tasks = current_user.tasks.filter(is_completed=True)

    context = {
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
    }

    return render(request, "task_manager/index.html", context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    # paginate_by = 10


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
