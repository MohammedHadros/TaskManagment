from django import forms  
from task_app.models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ["user","task" ]