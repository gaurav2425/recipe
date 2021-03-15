from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required()
def updateProfile(request):

    if request.method == "POST":    
        u_form = UserUpdateForm(request.POST,instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Your Profile has been updated successfully!")
            return redirect("users:profile")
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    context = {
        "u_form":u_form,
        "p_form":p_form
    }
    return render(request,"users/updateprofile.html",context)


@login_required()
def profile(request):
    return render(request,"users/profile.html")   


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            f_name = form.cleaned_data.get('f_name')
            l_name = form.cleaned_data.get('l_name')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username = username,password = password,email = email,first_name = f_name,last_name = l_name)
            user.save()
            messages.success(request,f"Account has been created for { username }!")
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{"form":form})
    # return render(request,'home/home1.html',{"form":form})


def userlogin(request):
    if request.method == "POST":
        # loginusername=request.POST['loginusername']
        # loginpassword =request.POST['loginpassword']
        form = LoginForm(request.POST) 
        if form.is_valid():
            loginusername=form.cleaned_data.get('user_id')
            loginpassword=form.cleaned_data.get('password')
            print(loginusername,loginpassword)
            user = authenticate(username=loginusername , password= loginpassword)
            if user is not None :
                login(request,user)
                messages.success(request,"Successfully Logged In")
                return redirect("home:home")
                # return render(request,"home/home.html")
            else:
                messages.error(request,"Unsuccessfull Logged In. Invalid credentials")
                return redirect("users:login")
        else: 
            return render(request,"users/login.html",{"form":form})
    return render(request,"users/login.html",{"form":LoginForm()})


@login_required()
def HandleLogout(request):
    logout(request)
    messages.success(request,"Successfully Loged out....")
    return redirect("home:home")

