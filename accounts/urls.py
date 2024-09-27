from django.urls import path
from .views import index, signup_api, login_api, logout_api

urlpatterns = [
    path('', index, name='accounts_index'),
    path('signup', signup_api, name='signup_api'),
    path('login', login_api, name='login_api'),
    path('logout', logout_api, name='logout_api')
]
