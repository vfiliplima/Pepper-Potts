from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm


# from django.urls import reverse


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "pk"


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "login"
            )  # Redirect to the login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def task_list(request):
    priority = request.GET.get(
        "priority", None
    )  # Get the priority from the request query parameters
    tasks = Task.objects.all()

    # Filter tasks based on priority if a priority is selected
    if priority:
        tasks = tasks.filter(priority=priority)

    context = {
        "tasks": tasks,
    }
    return render(request, "task_list.html", context)


@login_required
def task_detail(request, pk):
    # Retrieve the task object from the database using its ID
    task = get_object_or_404(Task, pk=pk)

    # Check if the logged-in user matches the user assigned to the task
    if task.user != request.user:
        # If the logged-in user is not the assigned user, return a 403 Forbidden response
        return HttpResponseForbidden("You don't have permission to view this task.")

    # Pass the task object to the template for rendering
    return render(request, "task_detail.html", {"task": task})


@login_required
def task_delete(request, pk):
    print("")
    print("---")
    print(request.method)
    token = request.user
    print(token)
    print("---")
    print("")
    # Retrieve the task object from the database using its ID
    task = get_object_or_404(Task, pk=pk)

    # Check if the request method is POST (delete confirmation)
    if request.method == "POST":
        # Delete the task object
        task.delete()
        # Redirect to the task list page
        return redirect("view-tasks")
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


def task_update(request, pk):
    # Retrieve the task object from the database using its ID
    task = get_object_or_404(Task, pk=pk)

    print("")
    print("")
    print(request.method)
    print("")
    print("")

    if request.method == "PUT":
        # Process the form submission data
        task.title = request.POST.get("editTitle")
        task.description = request.POST.get("editDescription")
        task.due_date = request.POST.get("editDueDate")
        task.priority = request.POST.get("editPriority")
        task.save()

        # Redirect to the task detail page or any other appropriate page
        return redirect("task-detail-page", pk=pk)

    # If the request method is not POST, render the same page with the form
    return render(request, "task_detail.html", {"task": task})
