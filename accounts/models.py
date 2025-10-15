from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

class UserProfile(AbstractUser):
    # different skill levels available for users
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    timezone = models.CharField(max_length=50, default='UTC')
    daily_goal_hours = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    email_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
    def get_total_hours(self):
        """Get total hours practiced by user"""
        from tracker.models import ProgressEntry
        total = ProgressEntry.objects.filter(user=self).aggregate(Sum('hours_spent'))['hours_spent__sum']
        return total or 0
    
    def get_total_goals_completed(self):
        """Get total completed goals"""
        from tracker.models import Goal
        return Goal.objects.filter(user=self, completed=True).count()
    
    def get_current_streak(self):
        """Calculate current learning streak in days"""
        from tracker.models import ProgressEntry
        today = timezone.now().date()
        streak = 0
        
        # check each day starting from today going backwards
        for i in range(365):
            check_date = today - timedelta(days=i)
            has_progress = ProgressEntry.objects.filter(user=self, date=check_date).exists()
            
            if has_progress:
                streak += 1
            else:
                break
                
        return streak
    
    def get_weekly_hours(self):
        """Get hours practiced this week"""
        from tracker.models import ProgressEntry
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        weekly_hours = ProgressEntry.objects.filter(
            user=self,
            date__gte=week_start,
            date__lte=today
        ).aggregate(Sum('hours_spent'))['hours_spent__sum']
        
        return weekly_hours or 0
    
    def get_skill_distribution(self):
        """Get hours distribution by skill category"""
        from tracker.models import ProgressEntry
        
        progress_entries = ProgressEntry.objects.filter(user=self)
        distribution = {}
        
        for entry in progress_entries:
            category = entry.skill.get_category_display()
            if category in distribution:
                distribution[category] += float(entry.hours_spent)
            else:
                distribution[category] = float(entry.hours_spent)
        
        return distribution
    
    def get_progress_level(self):
        """Calculate user progress level based on activity"""
        total_hours = self.get_total_hours()
        
        if total_hours >= 100:
            return 'Expert'
        elif total_hours >= 50:
            return 'Advanced'
        elif total_hours >= 20:
            return 'Intermediate'
        else:
            return 'Beginner'