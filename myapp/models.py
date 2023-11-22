from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank=True)
    users = models.ForeignKey(User, on_delete = models.DO_NOTHING)

class Task(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    users = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.title + ' - by ' + self.user.username
