from django.db import models
from django.contrib.auth.models import User

# Create your models here.
difficulty_MAX = 5
dif_Index = range(1, difficulty_MAX + 1)
dif_text=("very easy" , "easy" , "Middle" , "difficult" , "very difficult")

class Task(models.Model):
    title=models.CharField(max_length=50)
    decription=models.TextField()
    assigned_to=models.ForeignKey(User , on_delete=models.DO_NOTHING)
    difficulty=models.IntegerField(choices=zip(dif_Index,dif_text) , default=0)#
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " , "+ str(self.assigned_to) 
    

class Comment(models.Model):
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    task=models.ForeignKey(Task , on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.user)} : {self.comment} "
    

class Task_Files(models.Model):
    task= models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to=f"file", blank=True )

    def __str__(self):
        return str(self.task.title)
