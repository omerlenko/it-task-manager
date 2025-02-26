from django.contrib import admin

from task_manager.models import Task, TaskType, Position, Worker, Tag

admin.site.register(TaskType)
admin.site.register(Position)
admin.site.register(Task)
admin.site.register(Worker)
admin.site.register(Tag)
