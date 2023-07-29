from django.urls import path

from .views import *


urlpatterns = [
    path("" , View_tasks , name="all-tasks"),
    path("new" , CreateTask.as_view() , name="task-create"),
    path("task/<int:pk>" , TaskView , name="task-view"),
    path("task/<int:pk>/update" , UpdateTaskView.as_view() , name="task-update"),
    path("task/<int:pk>/delete" , delete_Task_view , name="task-delete"),
    path("task/<int:pk>/files" , View_Task_Fiels , name="task-fiels"),
    path("download/<int:download_file>" , download_file , name="download-file"),
    path("task/<int:pk>/files/new" , CreateTaskFile.as_view() , name="upload-file"),
    path("task/<int:task_pk>/files/update/<int:pk>" , UpdateTaskLink.as_view() , name="update-file"),

]