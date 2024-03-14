from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "priority", "username"]

    def get_username(self, obj):
        return obj.user.username
