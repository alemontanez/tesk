from django.forms import ModelForm
from .models import Task, Project

class CreateTask(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class CreateProject(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']