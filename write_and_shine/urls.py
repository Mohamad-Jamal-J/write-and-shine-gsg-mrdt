"""
URL configuration for write_and_shine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='posts/', permanent=False), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('accounts/', include('accounts.urls')),
    path('', include('profiles.urls')),
    path('posts/', include('posts.urls')),
    path('', include('search.urls')),
    path('', include('interactions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
