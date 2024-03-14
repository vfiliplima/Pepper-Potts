from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

# Create your views here.


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "pk"


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "task_list.html", {"tasks": tasks})


def task_detail(request, task_id):
    # Retrieve the task object from the database using its ID
    task = get_object_or_404(Task, id=task_id)

    # Pass the task object to the template for rendering
    return render(request, "task_detail.html", {"task": task})


def index(request):
    return render(request, "index.html")
