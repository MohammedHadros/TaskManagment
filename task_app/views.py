from genericpath import isfile
from os import listdir
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from networkx import join
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from task_app.forms import CommentForm, UserLoginForm
from task_app.models import Chaange_request, Task,Task_Files,Comment
from django.views.generic import (CreateView , UpdateView ,TemplateView)
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from pathlib import Path
from django.contrib.auth import authenticate, logout
# Create your views here.

@login_required(login_url='/login')
def View_tasks(request):
    tasks=Task.objects.all().order_by("-created_at")
    context={
        "tasks":tasks,
    }
    return render (request , "task_app/Task_list.html" ,context )

class CreateTask(CreateView):
    model=Task
    template_name="task_app/task_form.html"
    fields=["title","decription" , "assigned_to"  ,"difficulty" ]
    success_url= reverse_lazy("all-tasks")
    # def get_success_url(self):
    #     return reverse("task", args=[self.object.pk])
    def get_context_data(self):
        context = super(CreateTask, self).get_context_data()
        context["title"] = "✨ Cteate New Task"
        context["btn_text"] = "Cteate Task"
        return context

@login_required(login_url='/login')
def TaskView(request, pk):
    task = Task.objects.get(pk=pk)
    form=CommentForm(request.POST or None)
    has_req=Chaange_request.objects.filter(task=pk)

    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.task=task
            comment.save()
            return redirect("task-view",pk)
    comments = Comment.objects.filter(task=task).order_by("-created_at")

    context = {
        'task': task,
        "form":form,
        "comments":comments,
    }
    if len(comments)==0:
        context|={"noComment":True}
    if len(has_req)>0:
        context|={"has_req":has_req[0]}

    return render(request, "task_app/task_view.html", context)



class UpdateTaskView(CreateTask,UpdateView):
    fields=["title","decription"   ,"difficulty" ]
    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs["pk"])
    
    def get_context_data(self):
        context = super(UpdateTaskView, self).get_context_data()
        print(context)
        context["title"] = "✨ Update  Task"
        context["btn_text"] = "Update Task"
        context['update']='true'
        return context
    
    def get_success_url(self):
        return reverse("task-view", args=[self.object.pk])
    
    def form_valid(self, form):
        messages.success(self.request, "The Task was updated successfully.")
        return super(UpdateTaskView, self).form_valid(form)

@login_required(login_url='/login')
def delete_Task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {
        'task':task
    }
    # fetch the object related to passed id
    if request.method == "POST":
        # delete object
        task.delete()
        messages.success(request, "The Task was Deleted successfully.")
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")

    return render(request, "task_app/Task_confirm_delete.html", context)


@login_required(login_url='/login')
def View_Task_Fiels(request ,pk):
    task_file=Task_Files.objects.filter(task=pk)
    task=Task.objects.get(pk=pk)
    
    if len(task_file)>0:
        context={
            "task_files":task_file,
            "task":task
        }
    else:
        context={
            "no_file":True,
            "task":task
        }
    return render(request , "task_app/task_files.html" , context)

@login_required(login_url='/login')
def download_file(request,download_file):
    file=Task_Files.objects.get(pk=download_file)
    file_name=str(file.file)[5:]
    file_path=str(file.file)
    BASE_DIR = Path(__file__).resolve().parent.parent
    # the_file=BASE_DIR +"media/" + file_path
    the_file = os.path.join(BASE_DIR, "task_app/media/",file_path)
    cunk_size=8192
    response=StreamingHttpResponse(FileWrapper(open(the_file , 'rb'),cunk_size ),
            content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length']=os.path.getsize(the_file)
    response["Content-Disposition"]="Attachment;filename=%s" %file_name
    print(response)
    return response


class CreateTaskFile(CreateView):
    model=Task_Files
    template_name="task_app/task_file_form.html"
    fields=["file" ]

    def get_success_url(self):
        return reverse("task-fiels", args=[self.kwargs["pk"]])
    
    def get_context_data(self):
        context = super(CreateTaskFile, self).get_context_data()
        context["title"] = "➕ Add New File"
        context["btn_text"] = "Add File"
        context["task"] = Task.objects.get(id=self.kwargs["pk"])
        return context
    
    def form_valid(self, form):
        tutor_validator = form.save(commit=False)
        task = Task.objects.get(id=self.kwargs["pk"])
        tutor_validator.task = task
        tutor_validator.save()
        return HttpResponseRedirect(self.get_success_url())
    
    
class UpdateTaskLink(CreateTaskFile,UpdateView):
    def get_success_url(self):
        return reverse("task-fiels", args=[self.kwargs["task_pk"]])
    
    def get_queryset(self):
        return Task_Files.objects.filter(pk=self.kwargs["pk"])
    
    def get_context_data(self):
        context= super().get_context_data()
        context["task"]=Task.objects.get(pk=self.kwargs["task_pk"])
        context["task_file"]=Task_Files.objects.get(pk=self.kwargs["pk"])
        context["title"] = "✨ Update  Task Link"
        context["btn_text"] = "Update Link"
        return context
    def form_valid(self, form):
        tutor_validator = form.save(commit=False)
        task = Task.objects.get(id=self.kwargs["task_pk"])
        tutor_validator.task = task
        tutor_validator.save()
        return HttpResponseRedirect(self.get_success_url())
    

def register(request):
    if request.method == "GET":
        return render(request, "task_app/register.html")
    if request.method == "POST":
        first_name = request.POST['first_Name']
        last_name = request.POST['last_Name']
        email = request.POST['email']
        username = request.POST['username']
        Password = request.POST['Password']
        confirm_password = request.POST['confirm_password']

        if Password != confirm_password:
            passnotmatch = True
            return render(request, "task_app/register.html", {'passnotmatch': passnotmatch})
        if User.objects.filter(username=username):
            UserNameExist=True
            return render(request, "task_app/register.html" ,{"UserNameExist":UserNameExist})
        else:
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                            password=Password)
            user.save()
            login(request, user)
            return redirect("/")
            # return render(request, "register.html")
    return render(request, "task_app/register.html")


def Login_view(request):
    if request.method == "POST":
        usernam = request.POST['user-name']
        passwor = request.POST['Password']
        user = authenticate(username=usernam, password=passwor)
        print("User",usernam)
        print("password", passwor)
        if user is not None:

            login(request, user)
            if request.user.is_superuser:
                return redirect("/")
            return redirect("all-user-tasks" ,user.pk)
        return redirect("/")
    return render(request, "task_app/login.html")


def Logout(request):
    logout(request)
    return redirect("/")

# para User 
@login_required(login_url='/login')
def User_View_tasks(request,pk):
    tasks=Task.objects.filter(assigned_to=pk).order_by("-created_at")
    context={
        "tasks":tasks,
    }
    if len(tasks)==0:
        context|={
            "no_tasks":True
        }
        
    return render (request , "task_app/Task_list.html" ,context )


class CreateTaskUser(CreateView):
    model=Task
    template_name="task_app/task_form.html"
    fields=["title","decription"  ,"difficulty" ]
    # success_url= reverse_lazy("all-tasks")
    def get_success_url(self):
        return reverse("all-user-tasks", args=[self.request.user.id])
    def get_context_data(self):
        context = super(CreateTaskUser, self).get_context_data()
        context["title"] = "✨ Cteate New Task"
        context["btn_text"] = "Cteate Task"
        return context
    
    def form_valid(self, form):
        tutor_validator = form.save(commit=False)
        user = User.objects.get(id=self.request.user.id)
        tutor_validator.assigned_to = user
        tutor_validator.save()
        return HttpResponseRedirect(self.get_success_url())


class ChangeUserReq(CreateView):
    model=Chaange_request
    template_name="task_app/req_form.html"
    fields=["new_user" ]
    # success_url= reverse_lazy("all-tasks")
    def get_success_url(self):
        return reverse("task-view", args=[self.kwargs["task_pk"]])
    def get_context_data(self):
        context = super(ChangeUserReq, self).get_context_data()
        context["title"] = "✨ Request change"
        context["btn_text"] = "Change Task Responsibility "
        return context
    
    def form_valid(self, form):
        tutor_validator = form.save(commit=False)
        creator = User.objects.get(id=self.request.user.id)
        old_user = User.objects.get(pk=self.kwargs["pk"])
        task = Task.objects.get(pk=self.kwargs["task_pk"])
        tutor_validator.creator = creator
        tutor_validator.old_user = old_user
        tutor_validator.task = task
        tutor_validator.save()
        return HttpResponseRedirect(self.get_success_url())
    

class UpdateUserReq(ChangeUserReq,UpdateView):
    # fields=["task","old_user","creator","new_user" ]
    # non_changing_field =["task","old_user","creator"]
    def get_success_url(self):
        return reverse("task-view", args=[self.kwargs["task_pk"]])
    
    def get_queryset(self):
        return Chaange_request.objects.filter(pk=self.kwargs["pk"])
    
    def get_context_data(self):
        context = super(UpdateUserReq, self).get_context_data()
        context["title"] = "✨Updaate Request change"
        context["btn_text"] = "Change Task Responsibility "
        context["req"] = Chaange_request.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        tutor_validator = form.save(commit=False)
        creator = User.objects.get(id=self.request.user.id)
        old_user = User.objects.get(pk=self.kwargs["pk"])
        task = Task.objects.get(pk=self.kwargs["task_pk"])
        tutor_validator.creator = creator
        tutor_validator.old_user = old_user
        tutor_validator.task = task
        tutor_validator.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required(login_url='/login')
def View_Requests(request , pk):
    requests=Chaange_request.objects.filter(new_user=pk , status=1).order_by("-created_at")
    context={
        "requests":requests,
    }
    if len(requests)==0:
        context|={
        "noreq":True,
    }
    return render (request , "task_app/req_list.html" ,context )

@login_required(login_url='/login')
def View_Admin_Requests(request , pk):
    requests=Chaange_request.objects.filter(creator=pk).order_by("-created_at")
    context={
        "requests":requests,
    }
    if len(requests)==0:
        context|={
        "noreq":True,
    }
    return render (request , "task_app/req_list.html" ,context )

class UserReq_Response(UpdateView):
    model=Chaange_request
    template_name="task_app/req_form.html"
    fields=["status" ]
    def get_success_url(self):
        return reverse("user-request", args=[self.kwargs["user_pk"]])
    
    def get_queryset(self):
        return Chaange_request.objects.filter(pk=self.kwargs["pk"])
    
    def get_context_data(self):
        context = super(UserReq_Response, self).get_context_data()
        context["title"] = "✨Updaate Request change"
        context["btn_text"] = "Change Task Responsibility "
        context["req"] = Chaange_request.objects.get(pk=self.kwargs["pk"])
        return context    

    def form_valid(self, form):
        req = form.save(commit=False)
        # status=tutor_validator["status"]
        print(req)
        print(req.status)
        task=Task.objects.get(pk=req.task.pk)
        task.assigned_to=req.new_user
        print(task.assigned_to)
        print("old:  " +str(req.old_user) )
        task.save()
        return HttpResponseRedirect(self.get_success_url())
