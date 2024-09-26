from django.urls import path

from accounts import views

urlpatterns = [
    path('accounts/', views.index, name='accounts_index')
]