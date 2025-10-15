from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Skill, ProgressEntry, Goal, LearningResource
from .serializers import SkillSerializer, ProgressEntrySerializer, GoalSerializer, LearningResourceSerializer

class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Skill.objects.all()

class ProgressEntryViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProgressEntry.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        goal = self.get_object()
        goal.completed = not goal.completed
        if goal.completed:
            goal.completed_date = timezone.now().date()
        else:
            goal.completed_date = None
        goal.save()
        return Response({'status': 'completed toggled'})

class LearningResourceViewSet(viewsets.ModelViewSet):
    serializer_class = LearningResourceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LearningResource.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        resource = self.get_object()
        resource.is_completed = not resource.is_completed
        resource.save()
        return Response({'status': 'completion toggled'})

class DashboardAPIView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        today = timezone.now().date()
        
        total_skills = Skill.objects.count()
        user_progress_entries = ProgressEntry.objects.filter(user=user)
        total_hours = user_progress_entries.aggregate(Sum('hours_spent'))['hours_spent__sum'] or 0
        
        goals = Goal.objects.filter(user=user)
        completed_goals = goals.filter(completed=True).count()
        pending_goals = goals.filter(completed=False).count()
        
        week_ago = today - timedelta(days=7)
        recent_progress = user_progress_entries.filter(date__gte=week_ago).order_by('-date')[:5]
        
        upcoming_deadlines = goals.filter(
            completed=False, 
            deadline__gte=today
        ).order_by('deadline')[:5]
        
        data = {
            'total_skills': total_skills,
            'total_hours': float(total_hours),
            'completed_goals': completed_goals,
            'pending_goals': pending_goals,
            'recent_progress': ProgressEntrySerializer(recent_progress, many=True).data,
            'upcoming_deadlines': GoalSerializer(upcoming_deadlines, many=True).data,
        }
        return Response(data)
