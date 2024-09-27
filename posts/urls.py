from django.urls import path

from posts import views

urlpatterns = [
    path('posts/', views.index, name='posts_index'),
    path('posts/create/', views.create_post, name='create_post')
]