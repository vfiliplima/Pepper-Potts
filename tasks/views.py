from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import (
    HttpResponseForbidden,
    HttpResponseRedirect,
    QueryDict,
)
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.core.paginator import Paginator


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
    priority = request.GET.get("priority")
    see_only_self_tasks = request.GET.get("my_tasks")
    search_query = request.GET.get("search", "")
    page_number = request.GET.get("page")

    tasks = Task.objects.all()
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    if see_only_self_tasks == "true":
        tasks = Task.objects.filter(user=request.user)

    if priority:
        tasks = tasks.filter(priority=priority)

    paginator = Paginator(tasks, 5)
    page_obj = paginator.get_page(page_number)

    return render(request, "task_list.html", {"page_obj": page_obj})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Check if the logged-in user matches the user assigned to the task
    if task.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this task.")

    return render(request, "task_detail.html", {"task": task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "DELETE":
        task.delete()
        # Redirect to the task list page
        return HttpResponseRedirect(reverse("view-tasks"))
    else:
        # If the request method is not DELETE, render a confirmation page
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


@login_required
def task_update(request, pk):
    # Retrieve the task object from the database using its ID
    task = get_object_or_404(Task, pk=pk)

    if request.method == "PUT":
        # Parse the request body into a QueryDict object
        put_data = QueryDict(request.body)

        task.title = put_data.get("editTitle")
        task.description = put_data.get("editDescription")
        task.due_date = put_data.get("editDueDate")
        task.priority = put_data.get("editPriority")
        task.save()

        return HttpResponseRedirect(reverse("view-tasks"))

    # If the request method is not PUT, render the task edit form
    return render(request, "task_detail.html", {"task": task})


@login_required
@require_http_methods(["PATCH"])
def task_status_update(request, pk):   
    task = get_object_or_404(Task, pk=pk)

    task.status = QueryDict(request.body).get("newStatus")
    task.save()
    return HttpResponseRedirect(reverse("view-tasks"))
