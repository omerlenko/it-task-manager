from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import When, Case, Value, IntegerField, Q, Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from task_manager.forms import (
    TaskForm,
    TaskSearchForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    TeamForm,
    ProjectForm,
)
from task_manager.models import Task, Worker, Team, Project


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("task_manager:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@login_required
def profile(request):
    user = request.user
    context = {"worker": user}

    return render(request, "task_manager/worker_detail.html", context)


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("task_manager:profile")

    def get_object(self):
        return self.request.user


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers"


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "task_manager/worker_detail.html"
    context_object_name = "worker"


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task_manager/index.html"

    def get_selected_user(self):
        user_id = self.request.GET.get("user_id")
        if user_id:
            return get_object_or_404(Worker, id=user_id)
        return self.request.user

    def get_selected_project(self):
        project_id = self.request.GET.get("project_id")
        if project_id:
            return Project.objects.get(id=project_id)
        return None

    def get_project_completion(self, projects):
        projects_list = list(projects)
        for project in projects_list:
            total = project.tasks.count()
            if total > 0:
                completed = project.tasks.filter(is_completed=True).count()
                project.completion_percentage = round((completed / total) * 100)
            else:
                project.completion_percentage = 0
        return projects_list

    def get_task_statistics(self, tasks):
        return {
            "total_tasks": tasks.count(),
            "pending_tasks": tasks.filter(is_completed=False).count(),
            "completed_tasks": tasks.filter(is_completed=True).count(),
            "urgent_tasks": tasks.filter(priority="1").count(),
            "high_tasks": tasks.filter(priority="2").count(),
            "medium_tasks": tasks.filter(priority="3").count(),
            "low_tasks": tasks.filter(priority="4").count(),
        }

    def get_weekly_statistics(self, tasks):
        today = timezone.now().date()
        start_of_the_week = today - timedelta(days=today.weekday())
        end_of_the_week = start_of_the_week + timedelta(days=6)

        weekly_total_tasks = tasks.filter(
            deadline__range=[start_of_the_week, end_of_the_week]
        ).count()
        weekly_completed_tasks = tasks.filter(
            deadline__range=[start_of_the_week, end_of_the_week], is_completed=True
        ).count()
        percentage = round(
            weekly_completed_tasks / weekly_total_tasks * 100 if weekly_total_tasks else 0
        )
        return weekly_total_tasks, weekly_completed_tasks, percentage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_selected_user()
        selected_project = self.get_selected_project()
        teams = user.teams.all()
        context["selected_user"] = user
        context["users"] = Worker.objects.all()
        context["teams"] = teams

        projects = Project.objects.filter(teams__in=teams).distinct()
        context["projects"] = self.get_project_completion(projects)
        context["selected_project"] = selected_project if selected_project else ""

        tasks = user.tasks.all()
        if selected_project:
            tasks = tasks.filter(project=selected_project)
        context.update(self.get_task_statistics(tasks))
        context["upcoming_deadlines"] = tasks.filter(
            deadline__lte=timezone.now() + timedelta(days=3), is_completed=False
        ).order_by("deadline")

        weekly_total, weekly_completed, weekly_percentage = (
            self.get_weekly_statistics(tasks))
        context["weekly_total_tasks"] = weekly_total
        context["weekly_completed_tasks"] = weekly_completed
        context["weekly_completion_percentage"] = weekly_percentage

        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 8

    def get_queryset(self):
        queryset = Task.objects.all()

        # Filtering
        is_completed = self.request.GET.get("is_completed")
        priority = self.request.GET.get("priority")
        assignees = [a for a in self.request.GET.getlist("assignees") if a]
        project = self.request.GET.get("project")

        if is_completed:
            queryset = queryset.filter(is_completed=is_completed)
        if priority:
            queryset = queryset.filter(priority=priority)
        if assignees:
            queryset = queryset.filter(assignees__id__in=assignees).distinct()
        if project:
            queryset = queryset.filter(project=project)

        # Search
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data["search"]
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query)
                    | Q(description__icontains=search_query)
                )

        # Sorting
        sort_option = self.request.GET.get("sort")
        today = timezone.now().date()

        sort_mapping = {
            "priority_desc": "priority",
            "priority_asc": "-priority",
            "status_desc": "-is_completed",
            "status_asc": "is_completed",
            "deadline_desc": "-deadline",
        }
        if sort_option == "deadline_asc":
            queryset = queryset.annotate(
                expired=Case(
                    When(
                        deadline__lt=today,
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by("expired", "deadline")

        elif sort_option in sort_mapping:
            queryset = queryset.order_by(sort_mapping[sort_option])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["selected_is_completed"] = self.request.GET.get("is_completed", "")
        context["selected_priority"] = self.request.GET.get("priority", "")
        context["selected_assignees"] = self.request.GET.getlist("assignees", "")
        context["selected_project"] = self.request.GET.get("project", "")

        search = self.request.GET.get("search", "")
        context["search_form"] = TaskSearchForm(initial={"search": search})
        context["search_query"] = search

        context["users"] = Worker.objects.all()
        context["selected_sort"] = self.request.GET.get("sort", "")

        context["projects"] = Project.objects.all()

        return context

    def request_get(self):
        rq = self.request.GET.copy()
        rq.pop(self.page_kwarg, None)
        return rq.urlencode()


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


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "teams"


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    context_object_name = "team"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(assignees__in=self.object.members.all()).distinct()
        completed_tasks = tasks.filter(is_completed=True)
        pending_tasks = tasks.filter(is_completed=False)

        context["tasks"] = tasks
        context["completed_tasks"] = completed_tasks
        context["pending_tasks"] = pending_tasks
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("task_manager:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("task_manager:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "projects"
    template_name = "task_manager/project_list.html"


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completed_tasks = Project.objects.get(id=self.object.id).tasks.filter(
            is_completed=True
        )
        context["completed_tasks"] = completed_tasks
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy("task_manager:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:project-detail", kwargs={"pk": self.object.pk}
        )


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:project-list")
