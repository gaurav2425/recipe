from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    user_id = forms.CharField(label='User Id', required = True)
    password = forms.CharField(label='Password' , max_length=32, widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    f_name = forms.CharField(label='First name', max_length=100)
    l_name = forms.CharField(label='Last name', max_length=100)

    class Meta:
        model = User
        fields = ['f_name','l_name',"username",'email','password1','password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required = True)
    # f_name = forms.CharField(label='First name', max_length=100)
    # l_name = forms.CharField(label='Last name', max_length=100)

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
