from django.contrib import admin
from .models import Skill, ProgressEntry, Goal, LearningResource

# register models for admin interface
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin configuration for Skill model"""
    
    list_display = ('name', 'category', 'difficulty', 'created_at')
    list_filter = ('category', 'difficulty', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(ProgressEntry)
class ProgressEntryAdmin(admin.ModelAdmin):
    """Admin configuration for ProgressEntry model"""
    
    list_display = ('user', 'skill', 'date', 'hours_spent', 'created_at')
    list_filter = ('skill__category', 'date', 'created_at')
    search_fields = ('user__username', 'skill__name', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """Admin configuration for Goal model"""
    
    list_display = ('title', 'user', 'skill', 'deadline', 'completed', 'completed_date')
    list_filter = ('completed', 'skill__category', 'deadline', 'created_at')
    search_fields = ('title', 'user__username', 'skill__name')
    date_hierarchy = 'deadline'
    ordering = ('deadline', '-created_at')
    
    actions = ['mark_completed', 'mark_incomplete']
    
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(completed=True, completed_date=timezone.now().date())
        self.message_user(request, f'{updated} goals marked as completed.')
    mark_completed.short_description = "Mark selected goals as completed"
    
    def mark_incomplete(self, request, queryset):
        updated = queryset.update(completed=False, completed_date=None)
        self.message_user(request, f'{updated} goals marked as incomplete.')
    mark_incomplete.short_description = "Mark selected goals as incomplete"

@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    """Admin configuration for LearningResource model"""
    
    list_display = ('title', 'user', 'skill', 'resource_type', 'is_completed', 'created_at')
    list_filter = ('resource_type', 'is_completed', 'skill__category', 'created_at')
    search_fields = ('title', 'user__username', 'skill__name', 'url')
    ordering = ('-created_at',)
