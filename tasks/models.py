from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [("high", "High"), ("medium", "Medium"), ("low", "Low")]
    TASK_STATUS_CHOICES = [
        ("queued", "Queued"),
        ("in progress", "In progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS_CHOICES,
        default="queued",
    )

    def __str__(self):
        return self.title
