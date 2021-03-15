from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
from users.forms import UserRegisterForm
# Create your views here.

from home.models import Contact
from django.contrib.auth.decorators import login_required




def contact(request):
    # messages.info(request,"This is a test 3 message")
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly.")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,"Form has been submitted successfully.")
    return render(request, "home/contact.html")


def home(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    
    return render(request,'home/home.html',context)


# classbased view of home fuction.... required to uncomment certains things in urls.py
from django.views.generic import ListView  # , DetailView, CreateView # other views....
class PostListView(ListView):
    model = Post
    template_name = 'home/home.html'      # App / <model>_<viewtype>.html
    context_object_name = 'allPosts'
    ordering = ['-timeStamp']
    paginate_by = 5
    

def about(request):
    return render(request,'home/about.html')

def search(request):
    # posts = Post.objects.all()
    query = request.GET.get('query')
    if len(query)>=78 :
        posts = Post.objects.none()
    else:
        postsContent = Post.objects.filter(content__icontains=query)
        postsTitle = Post.objects.filter(title__icontains=query)
        postsAuthor = Post.objects.filter(author__icontains=query)
        posts = postsTitle.union(postsContent,postsAuthor)
    return render(request,'home/search.html',{"allPosts":posts,'query': query})


# def handleSignup(request):
#     if request.method == "POST":
#         username=request.POST['username']
#         email=request.POST['email']
#         fname=request.POST['fname']
#         lname=request.POST['lname']
#         pass1 =request.POST['pass1']
#         pass2 =request.POST['pass2']

#         #Check for errors in input fields.... 
#         if len(username)>10:
#             messages.error(request,"Username must be under 10 character.")
#             return redirect("home:home")
#         if pass1 != pass2 :
#             messages.error(request,"Passwords do no match.")
#             return redirect("home:home")
#         if username.isalnum():
#             messages.error(request,"Username must contain only alphabets and numbers only.")
#             return redirect("home:home")
#         myuser = User.objects.create_user(username = username, email=email, password=pass1)
#         myuser.first_name=fname
#         myuser.last_name = lname
#         myuser.save()
#         messages.success(request,"Your ICoder account has been created successfully")
#         return redirect("home:home")

#     else:
#         return HttpResponse('404 - Not found')




# @login_required
# def logout(request):
#     logout(request)
#     messages.error(request,"Successfully Loged out....")
#     return redirect("home:home")
#     # return HttpResponse('LOGout SUCCESSFULLY')