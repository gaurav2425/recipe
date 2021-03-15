from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView,PostDetailView,PostCreateView,UserPostListView,PostUpdateView,PostDeleteView


app_name = "blog" 

urlpatterns = [
    path('my-blogs', PostListView.as_view(), name="blogHome"),
    path('user/<str:username>',UserPostListView.as_view(),name='user-post'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('new_post', views.newBlog, name="new_blog"),
    path('postComment', views.postComment, name="postComment"),
    path('<str:slug>', views.blogPost, name="blogPost")
    # path('<str:slug>', PostDetailView.as_view(), name="blogPost"),
    # path('', views.blogHome, name="blogHome"),
    # path('new_post', PostCreateView.as_view(), name="new_blog"),
]


