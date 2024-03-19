import pytest
from ..models import Task
from django.urls import reverse
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(
        username="test_user", password="test_password"
    )
    return user


def test_with_authenticated_client(client, user):
    client.force_login(user)

    assert user.is_authenticated


@pytest.fixture
def task(user):
    return Task.objects.create(
        title="Test Task",
        description="Test Description",
        due_date="2024-03-31",
        priority="high",
        user=user,
    )


@pytest.mark.django_db
def test_task_list_view(client):
    response = client.get(reverse("view-tasks"))
    assert response.status_code == 200
    assert "Task List" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_create_task(client, user):
    initial_task_count = Task.objects.count()
    print(f"Initial Task Count: {initial_task_count}")
    client.force_login(user)

    response = client.post(
        reverse("task-create"),
        data={
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2024-03-17 22:57:00",
            "priority": "high",
        },
    )

    assert response.status_code == 302

    # Check if the task count has changed
    updated_task_count = Task.objects.count()
    print(f"Updated Task Count: {updated_task_count}")

    # Check that a new task has been created
    assert updated_task_count == initial_task_count + 1

    # Check that task was created correctly
    new_task = Task.objects.get(title="Test Task")
    assert new_task.description == "Test Description"
    assert new_task.priority == "high"


@pytest.mark.django_db
def test_task_detail(client, user):
    client.force_login(user)

    task = Task.objects.create(
        title="Test Task Two",
        description="my second task description",
        due_date="2024-03-31",
        priority="medium",
        user=user,
    )
    # Test the task detail view
    response = client.get(reverse("task-detail-page", kwargs={"pk": task.pk}))
    assert response.status_code == 200
    assert task.title.encode() in response.content
    assert task.description.encode() in response.content
    assert task.priority.encode() in response.content
    assert task.user.username.encode() in response.content


@pytest.mark.django_db
def test_task_delete_view(client, user, task):
    client.force_login(user)
    response = client.delete(reverse("task-delete", kwargs={"pk": task.pk}))
    assert response.status_code == 302  # Redirects after successful deletion
    assert not Task.objects.filter(pk=task.pk).exists()


def test_task_status_update_view(client, user, task):
    pass


def test_task_update_view(client, user, task):
    pass


def test_priority_filter(client, user, task):
    pass


def test_see_only_my_tasks_filter(client, user):
    pass
