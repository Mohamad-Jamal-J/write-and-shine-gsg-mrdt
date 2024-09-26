from django.urls import path

from search import views

urlpatterns = [
    path('search/', views.index, name='search_index')
]