from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    """Admin configuration for custom user model"""
    
    list_display = ('username', 'email', 'skill_level', 'date_joined', 'is_staff')
    list_filter = ('skill_level', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('profile_picture', 'skill_level', 'bio')
        }),
    )
