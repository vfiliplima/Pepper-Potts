from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskForm
from django.contrib.auth.decorators import login_required


# from django.urls import reverse


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


@login_required
def task_detail(request, pk):
    # Retrieve the task object from the database using its ID
    task = get_object_or_404(Task, pk=pk)

    # Pass the task object to the template for rendering
    return render(request, "task_detail.html", {"task": task})


@login_required
def task_delete(request, pk):
    # Retrieve the task object from the database using its ID
    task = get_object_or_404(Task, pk=pk)

    # Check if the request method is POST (delete confirmation)
    if request.method == "POST":
        # Delete the task object
        task.delete()
        # Redirect to a success URL (e.g., task list page)
        return redirect("task-list")
    else:
        # If the request method is not POST, render a confirmation page
        return render(request, "task_delete_confirm.html", {"task": task})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user.id
            form.save()
            return redirect("view-tasks")
    else:
        form = TaskForm()
    return render(request, "create_task.html", {"form": form})
