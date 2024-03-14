"""
URL configuration for task_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from tasks.views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    task_list,
    task_detail,
    index,
    task_delete,
    create_task,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path(
        "tasks/<int:pk>/",
        TaskRetrieveUpdateDestroyView.as_view(),
        name="task-update-destroy",
    ),
    path("", index, name="home-page"),
    path("task-list/", task_list, name="view-tasks"),
    path("task/<int:pk>/detail/", task_detail, name="task-detail-page"),
    path("task/<int:pk>/delete/", task_delete, name="task-delete"),
    path("task/create/", create_task, name="task-create"),
]
