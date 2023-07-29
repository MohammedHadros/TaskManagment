from django.contrib import admin
from task_app.models import Task,Task_Files,Comment
# Register your models here.

admin.site.register(Task)
admin.site.register(Task_Files)
admin.site.register(Comment)