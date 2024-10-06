from django.urls import path

from profiles.views import get_profile, create_or_update_profile

urlpatterns = [
    path('profiles/<int:user_id>', get_profile, name='get_profile'),
    path('profiles/update', create_or_update_profile, name='update_profile')

]