from django.urls import path

from posts import views

urlpatterns = [
    # path('posts/', views.index, name='posts_index'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/', views.get_all_posts, name='get_all_posts'),
    path('post/<int:post_id>/', views.delete_edit_post, name='delete_edit_post'),
    path('posts/search/', views.search_post, name='search_post'),
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
]