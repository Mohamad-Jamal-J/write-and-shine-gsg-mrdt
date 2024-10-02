from django.urls import path

from profiles.views import index, get_profile, create_or_update_profile

urlpatterns = [
    path('profiles/', index, name='profiles_index'),
    path('profiles/<int:user_id>', get_profile, name='get_profile'),
    path('profiles/update', create_or_update_profile, name='update_profile')

]