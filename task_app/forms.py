from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms  
from task_app.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["user","task" ]



class UserLoginForm(forms.ModelForm):
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
        }
        ))
