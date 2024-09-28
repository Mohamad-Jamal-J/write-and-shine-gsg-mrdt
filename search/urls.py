from django.urls import path
from search import views

urlpatterns = [
    path('search/', views.index, name='search_index'),
    path('posts/search/', views.search_post, name='search_post'),
    path('posts/', views.get_posts, name='get_posts'),
]