from django.urls import path

from posts import views

urlpatterns = [
    # path('posts/', views.index, name='posts_index'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.delete_edit_post, name='delete_edit_post'),
]