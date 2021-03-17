from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras
from blog.forms import NewPostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView




# Blog home where we can desplay all the posts....
def blogHome(request): 
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)

# alternate option to display all post using class base views...
class PostListView(ListView):
    model = Post
    template_name = 'blog/blogHome.html'      # App / <model>_<viewtype>.html
    context_object_name = 'allPosts'
    # ordering = ['-timeStamp']
    paginate_by = 5
    def get_queryset(self):
        # user = get_object_or_404(User,username=request.user)
        return Post.objects.filter(author=self.request.user).order_by('-timeStamp')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/userBlog.html'      # App / <model>_<viewtype>.html
    context_object_name = 'allPosts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-timeStamp')
    


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'




# Not working.... alternative to create new blog post with class base views...
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.auther = self.request.user
        form.instance.slug = form.cleaned_data.get("title")
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.auther = self.request.user
        form.instance.slug = form.cleaned_data.get("title")
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = "/blog/my-blog"
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False




@login_required()
def newBlog(request):
    form = NewPostForm() 
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            print(request.user, " and ")
            print(form.cleaned_data.get('author'))
            if form.cleaned_data.get('author') == request.user:
                form.save()
                messages.success(request,"Your Blog Post is uploaded successfully.")
                return redirect("blog:blogHome")
            else:
                messages.error(request,"Author's username should be the same through which you are logged in.")
                return render(request,"blog/post_form.html",{"form":form})
        else:
            messages.error(request,"There is some error please check and resubmit.")
            return render(request,"blog/post_form.html",{"form":form})
    else:
        return render(request,"blog/post_form.html",{"form":form})
        # return HttpResponse("Write your blog here")



def blogPost(request, slug): 
    # print(slug)
    post=Post.objects.filter(title=slug).first()
    post.views= post.views + 1
    # print(post)
    post.save()
    
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)



def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.title}")

