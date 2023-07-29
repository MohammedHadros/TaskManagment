from genericpath import isfile
from os import listdir
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from networkx import join
import os
from task_app.forms import CommentForm
from task_app.models import Task,Task_Files,Comment
from django.views.generic import (CreateView , UpdateView ,TemplateView)
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from pathlib import Path
# Create your views here.


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

def TaskView(request, pk):
    task = Task.objects.get(pk=pk)
    form=CommentForm(request.POST or None)
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