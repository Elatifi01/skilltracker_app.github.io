from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import timedelta, date
from .models import Skill, ProgressEntry, Goal, LearningResource
from .forms import SkillForm, ProgressEntryForm, GoalForm, LearningResourceForm
import json

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        today = timezone.now().date()
        
        # get basic stats for dashboard
        total_skills = Skill.objects.count()
        user_progress_entries = ProgressEntry.objects.filter(user=user)
        total_hours = user_progress_entries.aggregate(Sum('hours_spent'))['hours_spent__sum']
        if total_hours is None:
            total_hours = 0
        
        # calculate goal statistics
        goals = Goal.objects.filter(user=user)
        completed_goals = goals.filter(completed=True).count()
        pending_goals = goals.filter(completed=False).count()
        
        # get recent activity for dashboard
        week_ago = today - timedelta(days=7)
        recent_progress = user_progress_entries.filter(date__gte=week_ago).order_by('-date')[:5]
        
        upcoming_deadlines = goals.filter(completed=False, deadline__gte=today).order_by('deadline')[:5]
        
        # prepare data for charts
        month_ago = today - timedelta(days=30)
        monthly_progress = user_progress_entries.filter(date__gte=month_ago)
        
        # organize progress by category
        category_data = {}
        for entry in monthly_progress:
            category = entry.skill.get_category_display()
            if category in category_data:
                category_data[category] += float(entry.hours_spent)
            else:
                category_data[category] = float(entry.hours_spent)
        
        # get daily progress for chart
        daily_data = []
        for i in range(14):
            check_date = today - timedelta(days=i)
            daily_hours = user_progress_entries.filter(date=check_date).aggregate(Sum('hours_spent'))['hours_spent__sum'] or 0
            daily_data.append({
                'date': check_date.strftime('%m/%d'),
                'hours': float(daily_hours)
            })
        daily_data.reverse()
        
        skills_progress = []
        for skill in Skill.objects.all()[:5]:
            skill_hours = user_progress_entries.filter(skill=skill).aggregate(Sum('hours_spent'))['hours_spent__sum'] or 0
            skills_progress.append({
                'name': skill.name,
                'hours': float(skill_hours),
                'category': skill.get_category_display()
            })
        
        context = {
            'total_skills': total_skills,
            'total_hours': total_hours,
            'completed_goals': completed_goals,
            'pending_goals': pending_goals,
            'recent_progress': recent_progress,
            'upcoming_deadlines': upcoming_deadlines,
            'today': today,
            'category_data': json.dumps(category_data),
            'daily_data': json.dumps(daily_data),
            'skills_progress': skills_progress,
        }
        return render(request, 'tracker/dashboard.html', context)


class SkillListView(LoginRequiredMixin, ListView):
    model = Skill
    template_name = 'tracker/skill_list.html'
    context_object_name = 'skills'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Skill.objects.all()
        
        # search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # filter by category if selected
        category_filter = self.request.GET.get('category')
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        
        # filter by difficulty level
        difficulty_filter = self.request.GET.get('difficulty')
        if difficulty_filter:
            queryset = queryset.filter(difficulty=difficulty_filter)
            
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Skill.CATEGORIES
        context['difficulty_levels'] = Skill.DIFFICULTY_LEVELS
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        return context

class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'tracker/skill_form.html'
    success_url = reverse_lazy('tracker:skill_list')

class ProgressListView(LoginRequiredMixin, ListView):
    model = ProgressEntry
    template_name = 'tracker/progress_list.html'
    context_object_name = 'progress_entries'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ProgressEntry.objects.filter(user=self.request.user)
        
        # filter progress by date range
        date_filter = self.request.GET.get('date_filter')
        today = date.today()
        
        if date_filter == 'today':
            queryset = queryset.filter(date=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            queryset = queryset.filter(date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            queryset = queryset.filter(date__gte=month_ago)
        
        # filter by specific skill
        skill_filter = self.request.GET.get('skill')
        if skill_filter:
            queryset = queryset.filter(skill_id=skill_filter)
            
        return queryset.order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()
        context['selected_date_filter'] = self.request.GET.get('date_filter', '')
        context['selected_skill'] = self.request.GET.get('skill', '')
        
        user_progress = ProgressEntry.objects.filter(user=self.request.user)
        context['total_entries'] = user_progress.count()
        context['total_hours'] = user_progress.aggregate(Sum('hours_spent'))['hours_spent__sum'] or 0
        context['avg_hours'] = context['total_hours'] / context['total_entries'] if context['total_entries'] > 0 else 0
        
        return context

class ProgressCreateView(LoginRequiredMixin, CreateView):
    model = ProgressEntry
    form_class = ProgressEntryForm
    template_name = 'tracker/progress_form.html'
    success_url = reverse_lazy('tracker:progress_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # set the current user as owner of progress entry
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        # set default values for new progress entry
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
    form_class = GoalForm
    template_name = 'tracker/goal_form.html'
    success_url = reverse_lazy('tracker:goal_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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
    form_class = LearningResourceForm
    template_name = 'tracker/resource_form.html'
    success_url = reverse_lazy('tracker:resource_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ResourceToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        resource = get_object_or_404(LearningResource, pk=pk, user=request.user)
        resource.is_completed = not resource.is_completed
        resource.save()
        return redirect('tracker:resource_list')

class ProgressChartDataView(LoginRequiredMixin, View):
    def get(self, request):
        """Return JSON data for progress charts"""
        user = request.user
        days = int(request.GET.get('days', 30))
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        progress_data = ProgressEntry.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        daily_progress = {}
        for entry in progress_data:
            date_str = entry.date.strftime('%Y-%m-%d')
            if date_str in daily_progress:
                daily_progress[date_str] += float(entry.hours_spent)
            else:
                daily_progress[date_str] = float(entry.hours_spent)
        
        category_breakdown = {}
        for entry in progress_data:
            category = entry.skill.get_category_display()
            if category in category_breakdown:
                category_breakdown[category] += float(entry.hours_spent)
            else:
                category_breakdown[category] = float(entry.hours_spent)
        
        return JsonResponse({
            'daily_progress': daily_progress,
            'category_breakdown': category_breakdown,
            'total_hours': sum(daily_progress.values()),
            'total_days': len(daily_progress)
        })

class SkillStatsView(LoginRequiredMixin, View):
    def get(self, request, skill_id):
        """Return detailed stats for a specific skill"""
        skill = get_object_or_404(Skill, id=skill_id)
        user = request.user
        
        progress_entries = ProgressEntry.objects.filter(user=user, skill=skill)
        goals = Goal.objects.filter(user=user, skill=skill)
        resources = LearningResource.objects.filter(user=user, skill=skill)
        
        total_hours = progress_entries.aggregate(Sum('hours_spent'))['hours_spent__sum'] or 0
        total_sessions = progress_entries.count()
        completed_goals = goals.filter(completed=True).count()
        total_goals = goals.count()
        completed_resources = resources.filter(is_completed=True).count()
        total_resources = resources.count()
        
        recent_progress = list(progress_entries.order_by('-date')[:5].values(
            'date', 'hours_spent', 'description'
        ))
        
        return JsonResponse({
            'skill_name': skill.name,
            'total_hours': float(total_hours),
            'total_sessions': total_sessions,
            'avg_hours_per_session': float(total_hours / total_sessions) if total_sessions > 0 else 0,
            'completed_goals': completed_goals,
            'total_goals': total_goals,
            'completed_resources': completed_resources,
            'total_resources': total_resources,
            'recent_progress': recent_progress
        })
