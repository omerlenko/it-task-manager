from asyncio import tasks

from django.urls import path

from task_manager.views import index, TaskListView, TaskDetailView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]

app_name = "task_manager"