from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        input_formats=[
            "%Y-%m-%d %H:%M:%S"
        ],  # Specify the input format for date and time
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "placeholder": "YYYY-MM-DD HH:MM:SS"}
        ),
    )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority"]
