from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from task_manager.forms import TaskForm
from task_manager.models import Task


def index(request) -> HttpResponse:
    current_user = request.user

    total_tasks = current_user.tasks.count()
    pending_tasks = current_user.tasks.filter(is_completed=False).count()
    completed_tasks = current_user.tasks.filter(is_completed=True).count()

    urgent_tasks = current_user.tasks.filter(priority='Urgent').count()
    high_tasks = current_user.tasks.filter(priority='High').count()
    medium_tasks = current_user.tasks.filter(priority='Medium').count()
    low_tasks = current_user.tasks.filter(priority='Low').count()

    task_priority_counts = {
        "Urgent": urgent_tasks,
        "High": high_tasks,
        "Medium": medium_tasks,
        "Low": low_tasks,
    }

    upcoming_deadlines = current_user.tasks.filter(deadline__lte=timezone.now() + timedelta(days=3), is_completed=False).order_by("deadline")

    today = timezone.now().date()
    start_of_the_week = today - timedelta(days=today.weekday())
    end_of_the_week = start_of_the_week + timedelta(days=6)

    weekly_total_tasks = current_user.tasks.filter(deadline__range=[start_of_the_week, end_of_the_week]).count()
    weekly_completed_tasks = current_user.tasks.filter(deadline__range=[start_of_the_week, end_of_the_week], is_completed=True).count()
    weekly_completion_percentage = round(weekly_completed_tasks / weekly_total_tasks * 100 if weekly_total_tasks else 0)

    context = {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "upcoming_deadlines": upcoming_deadlines,
        "task_priority_counts": task_priority_counts,
        "weekly_total_tasks": weekly_total_tasks,
        "weekly_completed_tasks": weekly_completed_tasks,
        "weekly_completion_percentage": weekly_completion_percentage,
    }

    return render(request, "task_manager/index.html", context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 3


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task_manager:task-detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task_manager:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.is_completed = True
    task.save()
    return redirect("task_manager:task-list")