from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Skill, ProgressEntry, Goal, LearningResource

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
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
        
        context = {
            'total_skills': total_skills,
            'total_hours': total_hours,
            'completed_goals': completed_goals,
            'pending_goals': pending_goals,
            'recent_progress': recent_progress,
            'upcoming_deadlines': upcoming_deadlines,
            'today': today,
        }
        return render(request, 'tracker/dashboard.html', context)

class SkillListView(LoginRequiredMixin, ListView):
    model = Skill
    template_name = 'tracker/skill_list.html'
    context_object_name = 'skills'
    paginate_by = 20

class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    fields = ['name', 'category', 'difficulty', 'description']
    template_name = 'tracker/skill_form.html'
    success_url = reverse_lazy('tracker:skill_list')

class ProgressListView(LoginRequiredMixin, ListView):
    model = ProgressEntry
    template_name = 'tracker/progress_list.html'
    context_object_name = 'progress_entries'
    paginate_by = 20
    
    def get_queryset(self):
        return ProgressEntry.objects.filter(user=self.request.user)

class ProgressCreateView(LoginRequiredMixin, CreateView):
    model = ProgressEntry
    fields = ['skill', 'date', 'description', 'hours_spent']
    template_name = 'tracker/progress_form.html'
    success_url = reverse_lazy('tracker:progress_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial['date'] = timezone.now().date()
        initial['hours_spent'] = 1.0
        return initial

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'tracker/goal_list.html'
    context_object_name = 'goals'
    paginate_by = 20
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    fields = ['skill', 'title', 'description', 'deadline']
    template_name = 'tracker/goal_form.html'
    success_url = reverse_lazy('tracker:goal_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk, user=request.user)
        goal.completed = not goal.completed
        if goal.completed:
            goal.completed_date = timezone.now().date()
        else:
            goal.completed_date = None
        goal.save()
        return redirect('tracker:goal_list')

class ResourceListView(LoginRequiredMixin, ListView):
    model = LearningResource
    template_name = 'tracker/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 20
    
    def get_queryset(self):
        return LearningResource.objects.filter(user=self.request.user)

class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = LearningResource
    fields = ['skill', 'title', 'url', 'resource_type', 'notes']
    template_name = 'tracker/resource_form.html'
    success_url = reverse_lazy('tracker:resource_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ResourceToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk, user=request.user)
        resource.is_completed = not resource.is_completed
        resource.save()
        return redirect('tracker:resource_list')
