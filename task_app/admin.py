from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_app.models import Task,Task_Files,Comment,Chaange_request,User
# Register your models here.

admin.site.register(Task)
admin.site.register(Task_Files)
admin.site.register(Comment)
admin.site.register(Chaange_request)
# admin.site.register(User)

class CustomUserAdmin(UserAdmin):
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff',
    'is_email_varivied'
    )

admin.site.register(User, CustomUserAdmin)