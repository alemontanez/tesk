from django.forms import ModelForm
from .models import Task

class CreateTask(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']