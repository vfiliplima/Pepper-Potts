from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [("high", "High"), ("medium", "Medium"), ("low", "Low")]

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
