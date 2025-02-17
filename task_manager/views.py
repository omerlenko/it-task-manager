from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from task_manager.forms import TaskForm
from task_manager.models import Task, Worker


def index(request) -> HttpResponse:
    user_id = request.GET.get("user_id")
    if user_id:
        user = get_object_or_404(Worker, id=user_id)
    else:
        user = request.user

    users = Worker.objects.all()
    total_tasks = user.tasks.count()
    pending_tasks = user.tasks.filter(is_completed=False).count()
    completed_tasks = user.tasks.filter(is_completed=True).count()

    urgent_tasks = user.tasks.filter(priority='Urgent').count()
    high_tasks = user.tasks.filter(priority='High').count()
    medium_tasks = user.tasks.filter(priority='Medium').count()
    low_tasks = user.tasks.filter(priority='Low').count()

    task_priority_counts = {
        "Urgent": urgent_tasks,
        "High": high_tasks,
        "Medium": medium_tasks,
        "Low": low_tasks,
    }

    upcoming_deadlines = user.tasks.filter(deadline__lte=timezone.now() + timedelta(days=3), is_completed=False).order_by("deadline")

    today = timezone.now().date()
    start_of_the_week = today - timedelta(days=today.weekday())
    end_of_the_week = start_of_the_week + timedelta(days=6)

    weekly_total_tasks = user.tasks.filter(deadline__range=[start_of_the_week, end_of_the_week]).count()
    weekly_completed_tasks = user.tasks.filter(deadline__range=[start_of_the_week, end_of_the_week], is_completed=True).count()
    weekly_completion_percentage = round(weekly_completed_tasks / weekly_total_tasks * 100 if weekly_total_tasks else 0)

    context = {
        "selected_user": user,
        "users": users,
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
    paginate_by = 8

    def get_queryset(self):
        queryset = Task.objects.all()

        is_completed = self.request.GET.get("is_completed")
        priority = self.request.GET.get("priority")
        assignees = [a for a in self.request.GET.getlist("assignees") if a]

        if is_completed:
            queryset = queryset.filter(is_completed=is_completed)
        if priority:
            queryset = queryset.filter(priority=priority)
        if assignees:
            queryset = queryset.filter(assignees__id__in=assignees).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["selected_is_completed"] = self.request.GET.get("is_completed", "")
        context["selected_priority"] = self.request.GET.get("priority", "")
        context["selected_assignees"] = self.request.GET.getlist("assignees", "")

        context["users"] = Worker.objects.all()

        return context


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