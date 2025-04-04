# Generated by Django 5.1.5 on 2025-03-17 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0006_project_task_project_team_project_teams"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="task_manager.project",
            ),
        ),
    ]
