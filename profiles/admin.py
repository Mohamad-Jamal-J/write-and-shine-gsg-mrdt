from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'bio', 'profile_picture', 'education')
    search_fields = ('user__email', 'user__name')
