from django.db import models
from django.contrib.auth.models import User

# Modelo para proyectos
class Project(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)

    def __str__(self):
        return self.title

# Modelo para prioridades de las tareas
class Priority(models.Model):
    prio = models.CharField(max_length = 25)

    def __str__(self):
        return self.prio

# Modelo para las condiciones o estados de las tareas
class TaskCondition(models.Model):
    condition = models.CharField(max_length = 25)

    def __str__(self):
        return self.condition

# Modelo para las tareas
class Task(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add = True)
    completed = models.BooleanField(default = False)
    datecompleted = models.DateTimeField(null = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete = models.CASCADE, default = None)
    priority = models.ForeignKey(Priority, on_delete = models.DO_NOTHING, default = None)
    condition = models.ForeignKey(TaskCondition, on_delete = models.DO_NOTHING, default = None)

    def __str__(self):
        return self.title + ' - by ' + self.user.username
