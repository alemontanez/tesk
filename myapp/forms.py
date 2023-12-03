from django.forms import ModelForm
from .models import Task, Project

# Formulario para crear tareas
class CreateTask(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'user', 'project', 'priority', 'condition']

# Formulario para crear proyectos
class CreateProject(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

