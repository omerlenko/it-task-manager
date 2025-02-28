from asyncio import tasks

from django.urls import path

from task_manager.views import index, TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, \
    complete_task, WorkerCreateView, WorkerUpdateView, WorkerDetailView, profile, WorkerListView

urlpatterns = [
    path("", index, name="index"),
    path("register/", WorkerCreateView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path("profile/update/", WorkerUpdateView.as_view(), name="profile-update"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/complete/", complete_task, name="task-complete"),
]

app_name = "task_manager"