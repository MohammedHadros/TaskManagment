from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path("" , View_tasks , name="all-tasks"),
    path("new" , login_required(CreateTask.as_view()) , name="task-create"),
    path("task/<int:pk>" , TaskView , name="task-view"),
    path("task/<int:pk>/update" , login_required(UpdateTaskView.as_view()) , name="task-update"),
    path("task/<int:pk>/delete" , delete_Task_view , name="task-delete"),
    path("task/<int:pk>/files" , View_Task_Fiels , name="task-fiels"),
    path("download/<int:download_file>" , download_file , name="download-file"),
    path("task/<int:pk>/files/new" , login_required(CreateTaskFile.as_view()) , name="upload-file"),
    path("task/<int:task_pk>/files/update/<int:pk>" , 
         login_required(UpdateTaskLink.as_view()) ,
           name="update-file"),
    path("register" , register , name="register"),
    path("login" , Login_view , name="Login"),
    path("logout" , Logout , name="Logout"),
    path("activate-user/<uidb64>/<token>" ,activate_user , name="activate"),
#     path("activate-user" ,activate_user , name="activate"),
    path("tasks/<int:pk>" , User_View_tasks , name="all-user-tasks"),
    path("tasks/new" , login_required(CreateTaskUser.as_view()) 
         , name="create-user-tasks"),
    path("task/<int:task_pk>/req/<int:pk>" , 
         login_required(ChangeUserReq.as_view()) ,
           name="change-user-request"),
    path("task/<int:task_pk>/req/<int:pk>/up" ,
          login_required(UpdateUserReq.as_view()) , 
          name="change-user-request-up"),
    path("request/user/<int:pk>" , View_Requests , name="user-request"),
    path("request/admin/<int:pk>" , View_Admin_Requests , name="admin-request"),
    path("request/user/<int:user_pk>/req/<int:pk>" ,
          login_required(UserReq_Response.as_view()) ,
            name="user-response"),



]