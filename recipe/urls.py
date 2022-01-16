from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView,PostDetailView,PostCreateView,UserPostListView,PostUpdateView,PostDeleteView


app_name = "recipe" 

urlpatterns = [
    path('my-recipe', PostListView.as_view(), name="recipeHome"),
    path('user/<str:username>',UserPostListView.as_view(),name='user-post'),
    path('recipe/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('recipe/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('new_recipe', views.newRecipe, name="new_recipe"),
    path('postComment', views.postComment, name="postComment"),
    path('recipe/<str:slug>', views.blogPost, name="recipePost")
    # path('<str:slug>', PostDetailView.as_view(), name="blogPost"),
    # path('', views.blogHome, name="blogHome"),
    # path('new_post', PostCreateView.as_view(), name="new_blog"),
]


