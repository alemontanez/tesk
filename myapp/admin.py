from django.contrib import admin
from .models import Priority, Project, Task, TaskCondition

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ("description", )

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Priority)
admin.site.register(TaskCondition)