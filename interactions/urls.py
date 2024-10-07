from django.urls import path

from interactions import views

urlpatterns = [

    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:post_id>/has-liked/', views.has_user_liked_post, name='has_user_liked_post'),

]