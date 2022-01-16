from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from recipe.models import Recipe, RecipeComment
from django.contrib import messages
from django.contrib.auth.models import User
from recipe.templatetags import extras
from recipe.forms import NewRecipeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView




# Blog home where we can desplay all the posts....
def recipeHome(request): 
    allPosts= Recipe.objects.all()
    context={'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)

# alternate option to display all post using class base views...
class PostListView(ListView):
    model = Recipe
    template_name = 'blog/blogHome.html'      # App / <model>_<viewtype>.html
    context_object_name = 'allPosts'
    # ordering = ['-timeStamp']
    paginate_by = 5
    def get_queryset(self):
        # user = get_object_or_404(User,username=request.user)
        return Recipe.objects.filter(author=self.request.user).order_by('-timeStamp')


class UserPostListView(ListView):
    model = Recipe
    template_name = 'blog/userBlog.html'      # App / <model>_<viewtype>.html
    context_object_name = 'allPosts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Recipe.objects.filter(author=user).order_by('-timeStamp')
    


class PostDetailView(DetailView):
    model = Recipe
    context_object_name = 'post'




# Not working.... alternative to create new blog post with class base views...
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Recipe
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.auther = self.request.user
        form.instance.slug = form.cleaned_data.get("title")
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Recipe
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
    model = Recipe
    success_url = "/recipe/my-recipe"
    template_name = 'blog/recipe_confirm_delete.html' 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False




@login_required()
def newRecipe(request):
    form = NewRecipeForm() 
    if request.method == "POST":
        form = NewRecipeForm(request.POST)
        if form.is_valid():
            print(request.user, " and ")
            print(form.cleaned_data.get('author'))
            if form.cleaned_data.get('author') == request.user:
                form.save()
                messages.success(request,"Your Recipe is uploaded successfully.")
                return redirect("recipe:recipeHome")
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
    post=Recipe.objects.filter(title=slug).first()
    post.views= post.views + 1
    # print(post)
    post.save()
    
    comments= RecipeComment.objects.filter(recipe=post, parent=None)
    replies= RecipeComment.objects.filter(recipe=post).exclude(parent=None)
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
        post= Recipe.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=RecipeComment(comment= comment, user=user, recipe=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= RecipeComment.objects.get(sno=parentSno)
            comment=RecipeComment(comment= comment, user=user, recipe=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/recipe/recipe/{post.title}")

