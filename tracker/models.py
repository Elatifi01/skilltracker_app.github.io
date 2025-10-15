from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Skill(models.Model):
    # different categories to organize skills
    CATEGORIES = [
        ('frontend', 'Frontend Development'),
        ('backend', 'Backend Development'),
        ('mobile', 'Mobile Development'),
        ('data', 'Data Science'),
        ('devops', 'DevOps'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        # display skill name with category
        skill_name = self.name + ' (' + self.get_category_display() + ')'
        return skill_name

class ProgressEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']  # show newest first
        unique_together = ['user', 'skill', 'date']  # one entry per user/skill/date
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.date})"

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['deadline', '-created_at']  # order by deadline first
    
    def __str__(self):
        # show status with checkmark or circle
        status = "✓" if self.completed else "○"
        return f"{status} {self.title} ({self.skill.name})"

class LearningResource(models.Model):
    # different types of learning resources
    RESOURCE_TYPES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('course', 'Course'),
        ('documentation', 'Documentation'),
        ('book', 'Book'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.skill.name})"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('goal_deadline', 'Goal Deadline Approaching'),
        ('achievement', 'Achievement Unlocked'),
        ('milestone', 'Milestone Reached'),
        ('reminder', 'Practice Reminder'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    related_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    related_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('first_progress', 'First Progress Entry'),
        ('week_streak', '7 Day Streak'),
        ('month_streak', '30 Day Streak'),
        ('hours_milestone', 'Hours Milestone'),
        ('goals_completed', 'Goals Completed'),
        ('skills_mastered', 'Skills Mastered'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fas fa-trophy')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    required_value = models.IntegerField(default=1)
    current_value = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-earned_at']
        unique_together = ['user', 'achievement_type', 'required_value']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    @property
    def is_earned(self):
        return self.current_value >= self.required_value
