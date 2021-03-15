from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from blog.models import Post 


class NewPostForm(forms.ModelForm): 
    class Meta: 
        model = Post 
        fields = ['title','author','content']
        labels = {
            'author': ('Choose Your own username'),
        }
    

