import pytest
from ..models import Task
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User  # Import the User model


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_task_list_view(client):
    response = client.get(reverse("view-tasks"))
    assert response.status_code == 200
    assert "Task List" in response.content.decode("utf-8")


def test_create_task(client):
    response = client.post(
        reverse("task-create"),
        data={
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2024-03-31",
            "priority": "high",
        },
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_task_detail(client):
    # Create a user object
    user = User.objects.create(username="test_user")
    # Create a task associated with the user
    task = Task.objects.create(
        title="Test Task",
        description="Test Description",
        due_date="2024-03-31",
        priority="high",
        user=user,  # Associate the task with the user
    )
    # Test the task detail view
    response = client.get(reverse("task-detail-page", kwargs={"pk": task.pk}))
    assert response.status_code == 200
    # Add more assertions as needed
