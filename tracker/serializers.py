from rest_framework import serializers
from .models import Skill, ProgressEntry, Goal, LearningResource

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'difficulty', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProgressEntrySerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    
    class Meta:
        model = ProgressEntry
        fields = ['id', 'skill', 'skill_name', 'date', 'description', 'hours_spent', 'created_at']
        read_only_fields = ['id', 'created_at']

class GoalSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    
    class Meta:
        model = Goal
        fields = ['id', 'skill', 'skill_name', 'title', 'description', 'deadline', 'completed', 'completed_date', 'created_at']
        read_only_fields = ['id', 'created_at', 'completed_date']

class LearningResourceSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    
    class Meta:
        model = LearningResource
        fields = ['id', 'skill', 'skill_name', 'title', 'url', 'resource_type', 'notes', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']
