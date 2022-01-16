from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from recipe.models import Recipe 
from tinymce.widgets import TinyMCE 
  
  
class TinyMCEWidget(TinyMCE): 
    def use_required_attribute(self, *args): 
        return False

class NewRecipeForm(forms.ModelForm): 
    content = forms.CharField( 
        widget=TinyMCEWidget( 
            attrs={'required': False, 'cols': 30, 'rows': 10} 
        ) 
    ) 
    ingredients = forms.CharField( 
        widget=TinyMCEWidget( 
            attrs={'required': False, 'cols': 30, 'rows': 10} 
        ) 
    ) 

    class Meta: 
        model = Recipe 
        fields = ['title','author','pic','ingredients','content']
        labels = {
            'author': ('Choose Your own username'),
        }
    

