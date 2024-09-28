from django.urls import path

from posts import views

urlpatterns = [
    # path('posts/', views.index, name='posts_index'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.delete_edit_post, name='delete_edit_post'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]