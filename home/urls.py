from django.urls import path
from . import views
from .views import PostListView

app_name = "home" 

urlpatterns = [
    # path('', views.home,name='home'),
    path('', PostListView.as_view(), name="home"),
    path('home', views.home,name='Home'),
    path('contact', views.contact,name='contact'),
    path('about', views.about,name='about'),
    path('search', views.search,name='search'),
]
