from asyncio import tasks

from django.urls import path

from task_manager.views import index, TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, \
    complete_task

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/complete/", complete_task, name="task-complete"),
]

app_name = "task_manager"