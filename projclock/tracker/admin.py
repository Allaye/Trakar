from django.contrib import admin
from .models import Project, ProjectActivity, Employee


# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectActivity)
admin.site.register(Employee)