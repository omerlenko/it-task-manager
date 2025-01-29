from django.contrib import admin

from task_manager.models import Task, TaskType, Position, Worker

admin.site.register(TaskType)
admin.site.register(Position)
admin.site.register(Task)
admin.site.register(Worker)
