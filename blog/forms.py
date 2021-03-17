from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from blog.models import Post 
from tinymce.widgets import TinyMCE 
  
  
class TinyMCEWidget(TinyMCE): 
    def use_required_attribute(self, *args): 
        return False

class NewPostForm(forms.ModelForm): 
    content = forms.CharField( 
        widget=TinyMCEWidget( 
            attrs={'required': False, 'cols': 30, 'rows': 10} 
        ) 
    ) 

    class Meta: 
        model = Post 
        fields = ['title','author','content']
        labels = {
            'author': ('Choose Your own username'),
        }
    

