# Generated by Django 5.1.5 on 2025-02-19 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0002_alter_worker_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[("1", "Urgent"), ("2", "High"), ("3", "Medium"), ("4", "Low")],
                default="3",
                max_length=1,
            ),
        ),
    ]
